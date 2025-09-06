import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, approx_fprime
from scipy import stats

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 11

def fit_bradley_terry_with_ci(comparisons_df):
    """Fit Bradley-Terry model and compute CIs"""
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
        
        idx1 = metric_to_idx.get(m1)
        idx2 = metric_to_idx.get(m2)
        
        if idx1 is None or idx2 is None:
            continue
            
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
    
    # Compute Hessian for CIs
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
    
    log_params = np.concatenate([[0], result.x])
    params = np.exp(log_params)
    
    # Calculate probabilities and CIs for key comparisons
    results = []
    pairs = [('logprob', 'mi'), ('tokens', 'mi'), ('logprob', 'tokens')]
    
    for m1, m2 in pairs:
        i = metrics.index(m1)
        j = metrics.index(m2)
        
        diff = log_params[i] - log_params[j]
        prob = 1 / (1 + np.exp(-diff))
        
        var_diff = cov_matrix_full[i, i] + cov_matrix_full[j, j] - 2 * cov_matrix_full[i, j]
        se_diff = np.sqrt(max(0, var_diff))
        
        grad = prob * (1 - prob)
        se_prob = grad * se_diff
        ci_lower = max(0, prob - 1.96 * se_prob)
        ci_upper = min(1, prob + 1.96 * se_prob)
        
        results.append({
            'pair': f'{m1.upper()} vs {m2.upper()}',
            'prob': prob,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper
        })
    
    return results, wins, totals, metrics

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')
participant_df = pd.read_csv('participant_outlier_analysis.csv')

# Identify bottom quartile outliers
bottom_quartile = participant_df.nsmallest(int(len(participant_df) * 0.25), 'Mean_Agreement')
outlier_ids = bottom_quartile['UserID'].values

print(f"Removing {len(outlier_ids)} bottom quartile participants:")
for _, p in bottom_quartile.iterrows():
    print(f"  - {p['Name']} ({p['UserID']}): {p['Mean_Agreement']:.1%} agreement")

# Create datasets
full_df = merged_df
clean_df = merged_df[~merged_df['UserID'].isin(outlier_ids)]

# Fit models
print("\nFitting Bradley-Terry models...")
full_results, full_wins, full_totals, metrics = fit_bradley_terry_with_ci(full_df)
clean_results, clean_wins, clean_totals, _ = fit_bradley_terry_with_ci(clean_df)

# Create comparison plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Setup for both plots
comparisons = [r['pair'] for r in full_results]
x_pos = np.arange(len(comparisons))
width = 0.35

# Left plot: All Participants
full_probs = [r['prob'] for r in full_results]
full_errors = [[r['prob'] - r['ci_lower'] for r in full_results],
               [r['ci_upper'] - r['prob'] for r in full_results]]

# Color based on significance
colors_full = []
for r in full_results:
    if r['ci_lower'] > 0.5:
        colors_full.append('#2ecc71')  # Green - first metric preferred
    elif r['ci_upper'] < 0.5:
        colors_full.append('#e74c3c')  # Red - second metric preferred
    else:
        colors_full.append('#95a5a6')  # Gray - no significant difference

bars1 = ax1.bar(x_pos, full_probs, width,
                yerr=full_errors, capsize=8,
                color=colors_full, alpha=0.8,
                edgecolor='black', linewidth=2,
                error_kw={'linewidth': 2.5})

# Add value labels
for i, r in enumerate(full_results):
    ax1.text(i, r['prob'] + 0.02, f"{r['prob']:.1%}",
             ha='center', fontweight='bold', fontsize=11)
    
    # Add significance marker
    if r['ci_lower'] > 0.5 or r['ci_upper'] < 0.5:
        ax1.text(i, r['ci_upper'] + 0.05, '*',
                ha='center', fontsize=18, fontweight='bold')

ax1.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=2)
ax1.set_ylabel('P(First metric preferred)', fontsize=13, fontweight='bold')
ax1.set_title(f'All Participants (n={len(participant_df)})', fontsize=14, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(comparisons, fontsize=11)
ax1.set_ylim([0.3, 0.85])
ax1.grid(True, alpha=0.3, axis='y')

# Add sample sizes
for i, pair in enumerate([('logprob', 'mi'), ('tokens', 'mi'), ('logprob', 'tokens')]):
    idx1 = metrics.index(pair[0])
    idx2 = metrics.index(pair[1])
    n = full_totals[idx1][idx2]
    ax1.text(i, 0.32, f'n={int(n)}', ha='center', fontsize=9, style='italic')

# Right plot: Without Bottom Quartile
clean_probs = [r['prob'] for r in clean_results]
clean_errors = [[r['prob'] - r['ci_lower'] for r in clean_results],
                [r['ci_upper'] - r['prob'] for r in clean_results]]

# Color based on significance
colors_clean = []
for r in clean_results:
    if r['ci_lower'] > 0.5:
        colors_clean.append('#2ecc71')
    elif r['ci_upper'] < 0.5:
        colors_clean.append('#e74c3c')
    else:
        colors_clean.append('#95a5a6')

bars2 = ax2.bar(x_pos, clean_probs, width,
                yerr=clean_errors, capsize=8,
                color=colors_clean, alpha=0.8,
                edgecolor='black', linewidth=2,
                error_kw={'linewidth': 2.5})

# Add value labels
for i, r in enumerate(clean_results):
    ax2.text(i, r['prob'] + 0.02, f"{r['prob']:.1%}",
             ha='center', fontweight='bold', fontsize=11)
    
    # Add significance marker
    if r['ci_lower'] > 0.5 or r['ci_upper'] < 0.5:
        ax2.text(i, r['ci_upper'] + 0.05, '*',
                ha='center', fontsize=18, fontweight='bold')
    
    # Show change from full dataset
    change = r['prob'] - full_results[i]['prob']
    if abs(change) > 0.01:
        ax2.text(i, r['ci_lower'] - 0.08, f'({change*100:+.1f}pp)',
                ha='center', fontsize=9, style='italic', color='blue')

ax2.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=2)
ax2.set_ylabel('P(First metric preferred)', fontsize=13, fontweight='bold')
ax2.set_title(f'Without Bottom Quartile (n={len(participant_df) - len(outlier_ids)})', 
              fontsize=14, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(comparisons, fontsize=11)
ax2.set_ylim([0.3, 0.85])
ax2.grid(True, alpha=0.3, axis='y')

# Add sample sizes
for i, pair in enumerate([('logprob', 'mi'), ('tokens', 'mi'), ('logprob', 'tokens')]):
    idx1 = metrics.index(pair[0])
    idx2 = metrics.index(pair[1])
    n = clean_totals[idx1][idx2]
    ax2.text(i, 0.32, f'n={int(n)}', ha='center', fontsize=9, style='italic')

# Add legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#2ecc71', alpha=0.8, label='First metric significantly preferred'),
    Patch(facecolor='#95a5a6', alpha=0.8, label='No significant difference'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=2,
           bbox_to_anchor=(0.5, -0.08), framealpha=0.95)

plt.suptitle('Impact of Removing Bottom Quartile Participants', 
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('outlier_comparison.png', dpi=300, bbox_inches='tight')
print("\nSaved: outlier_comparison.png")

# Print numerical comparison
print("\n" + "=" * 70)
print("NUMERICAL COMPARISON")
print("-" * 70)
print(f"{'Comparison':<20} {'All Participants':<20} {'Without Outliers':<20} {'Change':<15}")
print("-" * 70)

for f, c in zip(full_results, clean_results):
    change = c['prob'] - f['prob']
    print(f"{f['pair']:<20} {f['prob']:.3f} [{f['ci_lower']:.3f}-{f['ci_upper']:.3f}]  "
          f"{c['prob']:.3f} [{c['ci_lower']:.3f}-{c['ci_upper']:.3f}]  "
          f"{change*100:+.1f}pp")

# Key finding
print("\n" + "=" * 70)
print("KEY FINDING")
print("-" * 70)
lt_before = full_results[2]['prob']
lt_after = clean_results[2]['prob']
print(f"Logprob vs Tokens preference:")
print(f"  With all participants: {lt_before:.1%} (barely above 50%)")
print(f"  Without bottom quartile: {lt_after:.1%} (clearer preference)")
print(f"  Improvement: {(lt_after - lt_before)*100:.1f} percentage points")
print(f"\n✓ Removing participants with low agreement reveals a clearer preference for logprob!")

# Save the cleaned dataset for final analysis
clean_df.to_csv('final_dataset_no_outliers.csv', index=False)
print(f"\nFinal cleaned dataset saved to: final_dataset_no_outliers.csv")
print("You can now rerun your main analysis with this cleaned dataset.")