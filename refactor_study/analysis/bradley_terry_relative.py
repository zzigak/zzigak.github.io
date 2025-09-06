import pandas as pd
import numpy as np
from scipy.optimize import minimize, approx_fprime
from scipy import stats
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def fit_bradley_terry_with_covariance(comparisons_df):
    """
    Fit Bradley-Terry model and compute full covariance matrix.
    Returns parameters and covariance matrix for computing relative quantities.
    """
    
    # Get unique metrics
    metrics = ['mi', 'tokens', 'logprob']
    n_metrics = len(metrics)
    metric_to_idx = {m: i for i, m in enumerate(metrics)}
    
    # Build comparison matrix
    wins = np.zeros((n_metrics, n_metrics))
    totals = np.zeros((n_metrics, n_metrics))
    
    for _, row in comparisons_df.iterrows():
        if row['Actual_Choice'] in ['EG', None] or pd.isna(row['Actual_Choice']):
            continue
            
        m1 = row['Original V1 Metric']
        m2 = row['Original V2 Metric']
        choice = row['Actual_Choice']
        
        idx1 = metric_to_idx[m1]
        idx2 = metric_to_idx[m2]
        
        if choice == m1:
            wins[idx1][idx2] += 1
        elif choice == m2:
            wins[idx2][idx1] += 1
            
        totals[idx1][idx2] += 1
        totals[idx2][idx1] += 1
    
    # Maximum likelihood estimation
    def neg_log_likelihood(log_params):
        # MI is reference (θ_MI = 0)
        params = np.exp(np.concatenate([[0], log_params]))
        ll = 0
        
        for i in range(n_metrics):
            for j in range(i+1, n_metrics):
                if totals[i][j] > 0:
                    p_ij = params[i] / (params[i] + params[j])
                    
                    if wins[i][j] > 0:
                        ll += wins[i][j] * np.log(p_ij + 1e-10)
                    if wins[j][i] > 0:
                        ll += wins[j][i] * np.log(1 - p_ij + 1e-10)
        
        return -ll
    
    # Optimize
    init_params = np.zeros(n_metrics - 1)
    result = minimize(neg_log_likelihood, init_params, method='BFGS')
    
    # Compute Hessian numerically for the estimated parameters only
    eps = 1e-5
    n_est = len(result.x)  # Number of estimated parameters (excluding reference)
    hessian = np.zeros((n_est, n_est))
    
    for i in range(n_est):
        for j in range(n_est):
            # Compute second derivative numerically
            def f_i(x):
                return approx_fprime(x, neg_log_likelihood, eps)[i]
            
            x_plus = result.x.copy()
            x_plus[j] += eps
            
            hessian[i, j] = (f_i(x_plus) - f_i(result.x)) / eps
    
    # Covariance matrix for estimated parameters (inverse of Hessian)
    try:
        cov_matrix_est = np.linalg.inv(hessian)
    except:
        print("Warning: Hessian not invertible, using pseudo-inverse")
        cov_matrix_est = np.linalg.pinv(hessian)
    
    # Expand covariance matrix to include reference category (with zeros)
    # Since β_MI = 0 is fixed, Var(β_MI) = 0 and Cov(β_MI, β_j) = 0
    cov_matrix_full = np.zeros((n_metrics, n_metrics))
    
    # Map indices: MI=0 (fixed), tokens=1, logprob=2
    # In estimation: tokens=0, logprob=1
    est_to_full = {0: 1, 1: 2}  # tokens is first estimated param, logprob is second
    
    for i in range(n_est):
        for j in range(n_est):
            full_i = est_to_full[i]
            full_j = est_to_full[j]
            cov_matrix_full[full_i, full_j] = cov_matrix_est[i, j]
    
    # Get final parameters
    log_params_full = np.concatenate([[0], result.x])
    params = np.exp(log_params_full)
    
    return {
        'metrics': metrics,
        'log_params': log_params_full,
        'params': params,
        'cov_matrix': cov_matrix_full,
        'wins': wins,
        'totals': totals
    }

def compute_relative_quantities(fit_result):
    """
    Compute all pairwise differences, win probabilities, and their CIs.
    """
    
    metrics = fit_result['metrics']
    log_params = fit_result['log_params']
    cov_matrix = fit_result['cov_matrix']
    n_metrics = len(metrics)
    
    results = []
    
    for i in range(n_metrics):
        for j in range(n_metrics):
            if i >= j:
                continue
            
            # Compute difference β_i - β_j
            diff = log_params[i] - log_params[j]
            
            # Standard error for difference
            # SE(β_i - β_j) = sqrt(Var(β_i) + Var(β_j) - 2*Cov(β_i, β_j))
            var_diff = cov_matrix[i, i] + cov_matrix[j, j] - 2 * cov_matrix[i, j]
            se_diff = np.sqrt(max(0, var_diff))  # max to avoid numerical issues
            
            # 95% CI for difference
            ci_diff_lower = diff - 1.96 * se_diff
            ci_diff_upper = diff + 1.96 * se_diff
            
            # Win probability P(i > j) = sigmoid(β_i - β_j)
            prob_i_wins = 1 / (1 + np.exp(-diff))
            
            # CI for win probability (using delta method)
            # d/dx sigmoid(x) = sigmoid(x) * (1 - sigmoid(x))
            grad = prob_i_wins * (1 - prob_i_wins)
            se_prob = grad * se_diff
            ci_prob_lower = prob_i_wins - 1.96 * se_prob
            ci_prob_upper = prob_i_wins + 1.96 * se_prob
            
            # Clip to [0, 1]
            ci_prob_lower = max(0, min(1, ci_prob_lower))
            ci_prob_upper = max(0, min(1, ci_prob_upper))
            
            # Odds ratio
            odds_ratio = np.exp(diff)
            ci_or_lower = np.exp(ci_diff_lower)
            ci_or_upper = np.exp(ci_diff_upper)
            
            # Test significance
            z_score = diff / se_diff if se_diff > 0 else 0
            p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
            
            results.append({
                'metric_i': metrics[i],
                'metric_j': metrics[j],
                'comparison': f'{metrics[i]} vs {metrics[j]}',
                'log_diff': diff,
                'se_log_diff': se_diff,
                'ci_log_diff': (ci_diff_lower, ci_diff_upper),
                'win_prob': prob_i_wins,
                'se_win_prob': se_prob,
                'ci_win_prob': (ci_prob_lower, ci_prob_upper),
                'odds_ratio': odds_ratio,
                'ci_odds_ratio': (ci_or_lower, ci_or_upper),
                'z_score': z_score,
                'p_value': p_value,
                'significant': p_value < 0.05
            })
    
    return results

# Load data and fit model
merged_df = pd.read_csv('intermediate_long_format.csv')

print("=" * 70)
print("Bradley-Terry Model: Relative Quantities with Proper CIs")
print("=" * 70)

# Fit model with full covariance matrix
fit_result = fit_bradley_terry_with_covariance(merged_df)

# Compute all relative quantities
relative_results = compute_relative_quantities(fit_result)

# Display results
print("\n1. Pairwise Log-Odds Differences (β_i - β_j):")
print("-" * 60)
print(f"{'Comparison':<20} {'Estimate':<12} {'SE':<10} {'95% CI':<25} {'p-value':<10}")
print("-" * 60)

for res in relative_results:
    ci_str = f"[{res['ci_log_diff'][0]:.3f}, {res['ci_log_diff'][1]:.3f}]"
    sig = '*' if res['significant'] else ''
    print(f"{res['comparison']:<20} {res['log_diff']:>8.3f} {res['se_log_diff']:>10.3f} {ci_str:<25} {res['p_value']:<10.4f}{sig}")

print("\n2. Win Probabilities P(i beats j):")
print("-" * 60)
print(f"{'Comparison':<20} {'P(i>j)':<12} {'SE':<10} {'95% CI':<25} {'Interpretation':<30}")
print("-" * 60)

for res in relative_results:
    ci_str = f"[{res['ci_win_prob'][0]:.3f}, {res['ci_win_prob'][1]:.3f}]"
    
    # Interpretation
    if res['win_prob'] > 0.5 and res['significant']:
        interp = f"{res['metric_i']} significantly preferred"
    elif res['win_prob'] < 0.5 and res['significant']:
        interp = f"{res['metric_j']} significantly preferred"
    else:
        interp = "No significant preference"
    
    print(f"{res['comparison']:<20} {res['win_prob']:>8.3f} {res['se_win_prob']:>10.3f} {ci_str:<25} {interp:<30}")

print("\n3. Odds Ratios exp(β_i - β_j):")
print("-" * 60)
print(f"{'Comparison':<20} {'Odds Ratio':<12} {'95% CI':<25} {'Interpretation':<40}")
print("-" * 60)

for res in relative_results:
    ci_str = f"[{res['ci_odds_ratio'][0]:.2f}, {res['ci_odds_ratio'][1]:.2f}]"
    
    # Interpretation
    if res['odds_ratio'] > 1:
        times = res['odds_ratio']
        interp = f"{res['metric_i']} is {times:.2f}x more likely to be preferred"
    else:
        times = 1 / res['odds_ratio']
        interp = f"{res['metric_j']} is {times:.2f}x more likely to be preferred"
    
    print(f"{res['comparison']:<20} {res['odds_ratio']:>8.2f} {ci_str:<25} {interp:<40}")

# Special focus on comparisons with MI (reference)
print("\n4. Comparisons with Reference (MI):")
print("-" * 60)

mi_comparisons = [r for r in relative_results if 'mi' in r['comparison']]
for res in mi_comparisons:
    other_metric = res['metric_i'] if res['metric_i'] != 'mi' else res['metric_j']
    
    print(f"\n{other_metric.upper()} vs MI:")
    print(f"  Log-odds difference: {res['log_diff']:.3f} ± {res['se_log_diff']:.3f}")
    print(f"  95% CI: [{res['ci_log_diff'][0]:.3f}, {res['ci_log_diff'][1]:.3f}]")
    print(f"  P({other_metric} beats MI): {res['win_prob']:.1%} [{res['ci_win_prob'][0]:.1%}, {res['ci_win_prob'][1]:.1%}]")
    print(f"  Odds ratio: {res['odds_ratio']:.2f} [{res['ci_odds_ratio'][0]:.2f}, {res['ci_odds_ratio'][1]:.2f}]")
    print(f"  p-value: {res['p_value']:.4f} {'(significant)' if res['significant'] else '(not significant)'}")

# Create visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Win probabilities with CIs
comparisons = [r['comparison'] for r in relative_results]
win_probs = [r['win_prob'] for r in relative_results]
ci_lower = [r['ci_win_prob'][0] for r in relative_results]
ci_upper = [r['ci_win_prob'][1] for r in relative_results]
errors = [[w - l for w, l in zip(win_probs, ci_lower)],
          [u - w for u, w in zip(ci_upper, win_probs)]]

x_pos = np.arange(len(comparisons))
colors = ['green' if r['significant'] else 'gray' for r in relative_results]

ax1.bar(x_pos, win_probs, yerr=errors, capsize=5, color=colors, alpha=0.7)
ax1.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='No preference')
ax1.set_ylabel('P(row beats column)')
ax1.set_title('Win Probabilities with 95% CIs', fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(comparisons, rotation=45, ha='right')
ax1.set_ylim([0, 1])
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Log-odds differences with CIs
log_diffs = [r['log_diff'] for r in relative_results]
ci_lower = [r['ci_log_diff'][0] for r in relative_results]
ci_upper = [r['ci_log_diff'][1] for r in relative_results]
errors = [[l - c for l, c in zip(log_diffs, ci_lower)],
          [c - l for c, l in zip(ci_upper, log_diffs)]]

ax2.bar(x_pos, log_diffs, yerr=errors, capsize=5, color=colors, alpha=0.7)
ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Equal strength')
ax2.set_ylabel('Log-odds difference (β_i - β_j)')
ax2.set_title('Log-Odds Differences with 95% CIs', fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(comparisons, rotation=45, ha='right')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.suptitle('Bradley-Terry Relative Comparisons', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('bradley_terry_relative_quantities.png', dpi=300, bbox_inches='tight')
print("\nSaved: bradley_terry_relative_quantities.png")

# Save results to CSV
results_df = pd.DataFrame(relative_results)
results_df.to_csv('bradley_terry_relative_results.csv', index=False)
print("Saved: bradley_terry_relative_results.csv")

print("\n" + "=" * 70)
print("Key Findings:")
print("-" * 60)

# Find significant results
sig_results = [r for r in relative_results if r['significant']]
if sig_results:
    print("Significant preferences found:")
    for res in sig_results:
        winner = res['metric_i'] if res['win_prob'] > 0.5 else res['metric_j']
        print(f"  - {winner} significantly preferred in {res['comparison']} (p={res['p_value']:.4f})")
else:
    print("No statistically significant preferences at α=0.05 level.")

print("\nNote: All CIs computed using Fisher Information (Hessian) with proper")
print("covariance terms. No bootstrap needed for these relative quantities!")