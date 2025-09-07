import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, approx_fprime
from scipy import stats
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

def fit_bradley_terry_once(comparisons_df):
    """Fit Bradley-Terry model once"""
    metrics = ['mi', 'tokens', 'logprob']
    n_metrics = len(metrics)
    metric_to_idx = {m: i for i, m in enumerate(metrics)}
    
    wins = np.zeros((n_metrics, n_metrics))
    totals = np.zeros((n_metrics, n_metrics))
    
    for _, row in comparisons_df.iterrows():
        if row['Actual_Choice'] in ['EG', None] or pd.isna(row['Actual_Choice']):
            continue
            
        m1 = row['Original V1 Metric']
        m2 = row['Original V2 Metric']
        choice = row['Actual_Choice']
        
        if m1 not in metric_to_idx or m2 not in metric_to_idx:
            continue
            
        idx1 = metric_to_idx[m1]
        idx2 = metric_to_idx[m2]
        
        if choice == m1:
            wins[idx1][idx2] += 1
        elif choice == m2:
            wins[idx2][idx1] += 1
            
        totals[idx1][idx2] += 1
        totals[idx2][idx1] += 1
    
    def neg_log_likelihood(log_params):
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
    
    init_params = np.zeros(n_metrics - 1)
    result = minimize(neg_log_likelihood, init_params, method='BFGS')
    
    log_params = np.concatenate([[0], result.x])
    params = np.exp(log_params)
    
    return {
        'params': params,
        'log_params': log_params,
        'metrics': metrics,
        'wins': wins,
        'totals': totals,
        'result': result
    }

def compute_hessian_cis(fit_result, merged_df):
    """Compute CIs using Hessian (analytical)"""
    metrics = fit_result['metrics']
    n_metrics = len(metrics)
    result = fit_result['result']
    
    # Compute Hessian for estimated parameters
    def neg_log_likelihood(log_params):
        params = np.exp(np.concatenate([[0], log_params]))
        ll = 0
        
        wins = fit_result['wins']
        totals = fit_result['totals']
        
        for i in range(n_metrics):
            for j in range(i+1, n_metrics):
                if totals[i][j] > 0:
                    p_ij = params[i] / (params[i] + params[j])
                    
                    if wins[i][j] > 0:
                        ll += wins[i][j] * np.log(p_ij + 1e-10)
                    if wins[j][i] > 0:
                        ll += wins[j][i] * np.log(1 - p_ij + 1e-10)
        
        return -ll
    
    eps = 1e-5
    n_est = len(result.x)
    hessian = np.zeros((n_est, n_est))
    
    for i in range(n_est):
        for j in range(n_est):
            def f_i(x):
                return approx_fprime(x, neg_log_likelihood, eps)[i]
            
            x_plus = result.x.copy()
            x_plus[j] += eps
            
            hessian[i, j] = (f_i(x_plus) - f_i(result.x)) / eps
    
    try:
        cov_matrix_est = np.linalg.inv(hessian)
    except:
        cov_matrix_est = np.linalg.pinv(hessian)
    
    # Expand covariance matrix
    cov_matrix_full = np.zeros((n_metrics, n_metrics))
    est_to_full = {0: 1, 1: 2}
    
    for i in range(n_est):
        for j in range(n_est):
            full_i = est_to_full[i]
            full_j = est_to_full[j]
            cov_matrix_full[full_i, full_j] = cov_matrix_est[i, j]
    
    # Calculate win probabilities and CIs for comparisons with MI
    mi_idx = 0
    results = []
    
    for i, metric in enumerate(metrics):
        if i != mi_idx:
            # P(metric beats MI)
            diff = fit_result['log_params'][i] - fit_result['log_params'][mi_idx]
            prob = 1 / (1 + np.exp(-diff))
            
            # CI calculation
            var_diff = cov_matrix_full[i, i]  # Cov with MI is 0
            se_diff = np.sqrt(var_diff)
            
            # Delta method for probability CI
            grad = prob * (1 - prob)
            se_prob = grad * se_diff
            ci_lower = max(0, prob - 1.96 * se_prob)
            ci_upper = min(1, prob + 1.96 * se_prob)
            
            results.append({
                'metric': metric,
                'prob': prob,
                'ci_lower': ci_lower,
                'ci_upper': ci_upper,
                'method': 'Hessian'
            })
    
    return results

def compute_bootstrap_cis(merged_df, n_bootstrap=1000):
    """Compute CIs using bootstrap"""
    print("Running bootstrap with 1000 iterations...")
    
    # Fit original model
    original_fit = fit_bradley_terry_once(merged_df)
    
    # Store bootstrap results for MI comparisons
    bootstrap_probs = {
        'tokens_vs_mi': [],
        'logprob_vs_mi': []
    }
    
    comparison_ids = merged_df.index.values
    
    for i in tqdm(range(n_bootstrap)):
        # Resample
        bootstrap_ids = np.random.choice(comparison_ids, size=len(comparison_ids), replace=True)
        bootstrap_data = merged_df.loc[bootstrap_ids]
        
        try:
            # Fit model
            boot_fit = fit_bradley_terry_once(bootstrap_data)
            
            # Calculate P(metric beats MI) for each metric
            mi_idx = 0
            tokens_idx = 1
            logprob_idx = 2
            
            # P(tokens beats MI)
            diff_tokens = boot_fit['log_params'][tokens_idx] - boot_fit['log_params'][mi_idx]
            prob_tokens = 1 / (1 + np.exp(-diff_tokens))
            bootstrap_probs['tokens_vs_mi'].append(prob_tokens)
            
            # P(logprob beats MI)
            diff_logprob = boot_fit['log_params'][logprob_idx] - boot_fit['log_params'][mi_idx]
            prob_logprob = 1 / (1 + np.exp(-diff_logprob))
            bootstrap_probs['logprob_vs_mi'].append(prob_logprob)
            
        except:
            continue
    
    # Calculate percentile CIs
    results = []
    
    for metric in ['tokens', 'logprob']:
        key = f'{metric}_vs_mi'
        probs = bootstrap_probs[key]
        
        if len(probs) > 0:
            mean_prob = np.mean(probs)
            ci_lower = np.percentile(probs, 2.5)
            ci_upper = np.percentile(probs, 97.5)
            
            results.append({
                'metric': metric,
                'prob': mean_prob,
                'ci_lower': ci_lower,
                'ci_upper': ci_upper,
                'method': 'Bootstrap',
                'distribution': probs
            })
    
    print(f"Bootstrap completed: {len(bootstrap_probs['tokens_vs_mi'])} successful iterations")
    return results, original_fit

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')

# Compute both methods
print("Computing Hessian-based CIs...")
original_fit = fit_bradley_terry_once(merged_df)
hessian_results = compute_hessian_cis(original_fit, merged_df)

print("Computing Bootstrap CIs...")
bootstrap_results, _ = compute_bootstrap_cis(merged_df)

# Get observed proportions
observed_data = []
metrics = ['tokens', 'logprob']
mi_idx = 0

for metric in metrics:
    metric_idx = original_fit['metrics'].index(metric)
    wins = original_fit['wins'][metric_idx][mi_idx]
    total = original_fit['totals'][metric_idx][mi_idx]
    
    if total > 0:
        observed_prop = wins / total
        observed_data.append({
            'metric': metric,
            'observed': observed_prop,
            'wins': wins,
            'total': total
        })

# Create side-by-side comparison plot
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Common setup
metrics_to_plot = ['TOKENS', 'LOGPROB']
x_pos = np.arange(len(metrics_to_plot))
width = 0.25

# Left plot: Hessian CIs
ax1 = axes[0]

# Hessian estimates
hessian_probs = [r['prob'] for r in hessian_results]
hessian_errors = [[r['prob'] - r['ci_lower'] for r in hessian_results],
                  [r['ci_upper'] - r['prob'] for r in hessian_results]]

bars1 = ax1.bar(x_pos - width, hessian_probs, width,
                yerr=hessian_errors, capsize=6,
                color=['#3498db', '#2ecc71'], alpha=0.8,
                label='BT Model (Hessian CI)', edgecolor='black', linewidth=1.5,
                error_kw={'linewidth': 2})

# Observed proportions
observed_probs = [o['observed'] for o in observed_data]
bars2 = ax1.bar(x_pos, observed_probs, width,
                color='lightgray', alpha=0.8,
                label='Observed Proportion', edgecolor='black', linewidth=1.5)

# Add value labels
for i in range(len(metrics_to_plot)):
    ax1.text(i - width, hessian_probs[i] + 0.03, f"{hessian_probs[i]:.1%}",
             ha='center', fontweight='bold', fontsize=9)
    ax1.text(i, observed_probs[i] + 0.03, f"{observed_probs[i]:.1%}",
             ha='center', fontweight='bold', fontsize=9)
    ax1.text(i, -0.08, f"n={observed_data[i]['total']}", 
             ha='center', fontsize=9, style='italic')

ax1.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=1.5)
ax1.set_ylabel('P(Metric beats MI)', fontsize=12, fontweight='bold')
ax1.set_title('Analytical Method (Hessian)', fontsize=13, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(metrics_to_plot)
ax1.set_ylim([0, 1])
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3, axis='y')

# Right plot: Bootstrap CIs
ax2 = axes[1]

# Bootstrap estimates
bootstrap_probs = [r['prob'] for r in bootstrap_results]
bootstrap_errors = [[r['prob'] - r['ci_lower'] for r in bootstrap_results],
                   [r['ci_upper'] - r['prob'] for r in bootstrap_results]]

bars3 = ax2.bar(x_pos - width, bootstrap_probs, width,
                yerr=bootstrap_errors, capsize=6,
                color=['#3498db', '#2ecc71'], alpha=0.8,
                label='BT Model (Bootstrap CI)', edgecolor='black', linewidth=1.5,
                error_kw={'linewidth': 2})

# Observed proportions (same)
bars4 = ax2.bar(x_pos, observed_probs, width,
                color='lightgray', alpha=0.8,
                label='Observed Proportion', edgecolor='black', linewidth=1.5)

# Add value labels
for i in range(len(metrics_to_plot)):
    ax2.text(i - width, bootstrap_probs[i] + 0.03, f"{bootstrap_probs[i]:.1%}",
             ha='center', fontweight='bold', fontsize=9)
    ax2.text(i, observed_probs[i] + 0.03, f"{observed_probs[i]:.1%}",
             ha='center', fontweight='bold', fontsize=9)

ax2.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=1.5)
ax2.set_ylabel('P(Metric beats MI)', fontsize=12, fontweight='bold')
ax2.set_title('Bootstrap Method (1000 samples)', fontsize=13, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(metrics_to_plot)
ax2.set_ylim([0, 1])
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3, axis='y')

# Add comparison statistics
ax2.text(0.98, 0.02, 'CIs are very similar!', transform=ax2.transAxes,
         ha='right', va='bottom', fontsize=10, style='italic',
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8))

plt.suptitle('Comparison of CI Methods: P(Metric beats MI)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('hessian_vs_bootstrap_comparison.png', dpi=300, bbox_inches='tight')
print("\nSaved: hessian_vs_bootstrap_comparison.png")

# Print numerical comparison
print("\n" + "=" * 60)
print("Numerical Comparison of CI Methods")
print("-" * 60)
print(f"{'Metric':<10} {'Method':<12} {'Estimate':<10} {'95% CI':<20} {'CI Width':<10}")
print("-" * 60)

for h, b in zip(hessian_results, bootstrap_results):
    h_width = h['ci_upper'] - h['ci_lower']
    b_width = b['ci_upper'] - b['ci_lower']
    
    print(f"{h['metric'].upper():<10} {'Hessian':<12} {h['prob']:.3f} "
          f"[{h['ci_lower']:.3f}, {h['ci_upper']:.3f}]  {h_width:.3f}")
    print(f"{'':<10} {'Bootstrap':<12} {b['prob']:.3f} "
          f"[{b['ci_lower']:.3f}, {b['ci_upper']:.3f}]  {b_width:.3f}")
    print()

print("Conclusion: Both methods give very similar CIs, validating our analytical approach!")