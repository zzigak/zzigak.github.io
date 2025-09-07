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

# Calculate consensus for each tuple
print("Calculating consensus for each tuple comparison...")
tuple_stats = merged_df.groupby(['TupleID', 'Pair Type']).agg({
    'Actual_Choice': [
        lambda x: x.value_counts(normalize=True).iloc[0] if len(x) > 0 else 0,  # consensus rate
        lambda x: x.value_counts().index[0] if len(x) > 0 else None,  # majority choice
        'count'  # total votes
    ],
    'UserID': 'nunique'  # unique participants
}).reset_index()

tuple_stats.columns = ['TupleID', 'Pair Type', 'Consensus_Rate', 'Majority_Choice', 'Total_Votes', 'Unique_Participants']

# Merge consensus info back to main dataframe
merged_df = merged_df.merge(tuple_stats[['TupleID', 'Pair Type', 'Consensus_Rate', 'Majority_Choice']], 
                            on=['TupleID', 'Pair Type'], how='left')

# Test extended range of thresholds for Method 1
thresholds = [0.55, 0.60, 0.65, 0.70, 0.75, 0.80]
method1_results = []

print("\n" + "=" * 80)
print("METHOD 1 WITH LOWER THRESHOLDS")
print("=" * 80)

for threshold in thresholds:
    # METHOD 1: Filter individual responses (keep tuple, remove minority votes)
    mask = (merged_df['Consensus_Rate'] < threshold) | \
           (merged_df['Actual_Choice'] == merged_df['Majority_Choice'])
    filtered_df = merged_df[mask].copy()
    
    # Fit model
    results, _, _, _ = fit_bradley_terry_with_ci(filtered_df)
    
    # Calculate statistics
    n_removed = len(merged_df) - len(filtered_df)
    pct_removed = (n_removed / len(merged_df)) * 100
    n_tuples_affected = ((merged_df['Consensus_Rate'] >= threshold) & 
                         (merged_df['Consensus_Rate'] < 1.0)).sum()
    
    print(f"\nThreshold: {threshold*100:.0f}%")
    print(f"  Responses removed: {n_removed}/{len(merged_df)} ({pct_removed:.1f}%)")
    print(f"  Responses kept: {len(filtered_df)} ({100-pct_removed:.1f}%)")
    print(f"  Tuples affected: {n_tuples_affected}")
    print(f"  Results:")
    for r in results:
        print(f"    {r['pair']}: {r['prob']:.3f} [{r['ci_lower']:.3f}-{r['ci_upper']:.3f}]")
    
    method1_results.append({
        'threshold': threshold,
        'n_responses': len(filtered_df),
        'n_removed': n_removed,
        'pct_removed': pct_removed,
        'results': results
    })

# Get baseline (no filtering)
baseline_results, _, _, _ = fit_bradley_terry_with_ci(merged_df)

# Create visualization
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

for idx, threshold in enumerate(thresholds):
    ax = axes[idx]
    
    # Get results for this threshold
    thresh_data = method1_results[idx]
    
    # Setup plot
    comparisons = [r['pair'] for r in thresh_data['results']]
    x_pos = np.arange(len(comparisons))
    width = 0.35
    
    # Baseline bars
    baseline_probs = [r['prob'] for r in baseline_results]
    ax.bar(x_pos - width/2, baseline_probs, width, 
           color='gray', alpha=0.5, label='No filter', edgecolor='black')
    
    # Filtered bars with colors based on significance
    filtered_probs = [r['prob'] for r in thresh_data['results']]
    colors = []
    for r in thresh_data['results']:
        if r['ci_lower'] > 0.5:
            colors.append('#2ecc71')
        elif r['ci_upper'] < 0.5:
            colors.append('#e74c3c')
        else:
            colors.append('#95a5a6')
    
    ax.bar(x_pos + width/2, filtered_probs, width,
           color=colors, alpha=0.8, label=f'≥{threshold*100:.0f}% consensus',
           edgecolor='black', linewidth=1.5)
    
    # Add error bars
    errors = [[r['prob'] - r['ci_lower'] for r in thresh_data['results']],
              [r['ci_upper'] - r['prob'] for r in thresh_data['results']]]
    ax.errorbar(x_pos + width/2, filtered_probs, yerr=errors,
                fmt='none', color='black', capsize=5, linewidth=1.5)
    
    # Add change labels
    for i, (baseline, filtered) in enumerate(zip(baseline_results, thresh_data['results'])):
        change = filtered['prob'] - baseline['prob']
        if abs(change) > 0.01:
            ax.text(i, max(baseline['prob'], filtered['prob']) + 0.05,
                   f'{change*100:+.1f}pp', ha='center', fontsize=9, 
                   color='blue', fontweight='bold')
    
    ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=1.5)
    ax.set_ylim([0.35, 0.85])
    ax.set_xticks(x_pos)
    ax.set_xticklabels([c.split(' vs ')[0] + '\nvs\n' + c.split(' vs ')[1] for c in comparisons], fontsize=9)
    ax.set_ylabel('P(First preferred)' if idx % 3 == 0 else '', fontsize=11)
    ax.set_title(f'Threshold: {threshold*100:.0f}%\n'
                f'({thresh_data["n_removed"]} responses removed, {thresh_data["pct_removed"]:.1f}%)', 
                fontsize=11, fontweight='bold')
    ax.legend(loc='upper left', fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')

plt.suptitle('Method 1 (Response-Level Filtering) with Lower Thresholds', 
            fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('consensus_lower_thresholds.png', dpi=300, bbox_inches='tight')
print("\nSaved: consensus_lower_thresholds.png")

# Create summary plot
fig2, axes2 = plt.subplots(1, 2, figsize=(16, 6))

# Left plot: Preference trends
ax = axes2[0]
pairs = ['LOGPROB vs MI', 'TOKENS vs MI', 'LOGPROB vs TOKENS']
colors = ['#3498db', '#e74c3c', '#2ecc71']
markers = ['o', 's', '^']

for pair_idx, (pair_name, color, marker) in enumerate(zip(pairs, colors, markers)):
    probs = [r['results'][pair_idx]['prob'] for r in method1_results]
    ci_lowers = [r['results'][pair_idx]['ci_lower'] for r in method1_results]
    ci_uppers = [r['results'][pair_idx]['ci_upper'] for r in method1_results]
    
    ax.plot([t*100 for t in thresholds], probs, 
           marker=marker, linestyle='-', linewidth=2.5,
           color=color, label=pair_name, markersize=10)
    
    # Add confidence intervals
    ax.fill_between([t*100 for t in thresholds], ci_lowers, ci_uppers,
                    alpha=0.15, color=color)

# Add baseline as horizontal lines
for pair_idx, (pair_name, color) in enumerate(zip(pairs, colors)):
    baseline_prob = baseline_results[pair_idx]['prob']
    ax.axhline(baseline_prob, color=color, linestyle=':', alpha=0.5, linewidth=1)

ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.3, linewidth=1.5)
ax.set_xlabel('Consensus Threshold (%)', fontsize=12)
ax.set_ylabel('P(First metric preferred)', fontsize=12)
ax.set_title('Preference Changes with Lower Thresholds', fontsize=13, fontweight='bold')
ax.set_ylim([0.45, 0.80])
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# Right plot: Data removal
ax = axes2[1]
removed_pcts = [r['pct_removed'] for r in method1_results]
removed_counts = [r['n_removed'] for r in method1_results]

ax.bar([t*100 for t in thresholds], removed_pcts, width=3,
       color='#e74c3c', alpha=0.7, edgecolor='black', linewidth=1.5)

# Add count labels
for i, (threshold, pct, count) in enumerate(zip(thresholds, removed_pcts, removed_counts)):
    ax.text(threshold*100, pct + 0.5, f'{count}', ha='center', fontsize=10)

ax.set_xlabel('Consensus Threshold (%)', fontsize=12)
ax.set_ylabel('% Responses Removed', fontsize=12)
ax.set_title('Data Removal at Different Thresholds', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

plt.suptitle('Impact of Lowering Consensus Threshold', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('consensus_threshold_impact.png', dpi=300, bbox_inches='tight')
print("Saved: consensus_threshold_impact.png")

# Print summary table
print("\n" + "=" * 80)
print("SUMMARY: Impact of Different Thresholds")
print("=" * 80)
print(f"{'Threshold':<12} {'Removed':<12} {'LOGPROB vs MI':<20} {'TOKENS vs MI':<20} {'LOGPROB vs TOKENS':<20}")
print("-" * 80)
for r in method1_results:
    t = f"{r['threshold']*100:.0f}%"
    removed = f"{r['n_removed']} ({r['pct_removed']:.1f}%)"
    lm = f"{r['results'][0]['prob']:.3f}"
    tm = f"{r['results'][1]['prob']:.3f}"
    lt = f"{r['results'][2]['prob']:.3f}"
    print(f"{t:<12} {removed:<12} {lm:<20} {tm:<20} {lt:<20}")

# Recommendation
print("\n" + "=" * 80)
print("RECOMMENDATION")
print("=" * 80)
max_effect_threshold = None
max_effect = 0
for r in method1_results:
    avg_change = sum(abs(r['results'][i]['prob'] - baseline_results[i]['prob']) 
                    for i in range(3)) / 3
    if avg_change > max_effect and r['pct_removed'] < 20:  # Don't remove too much
        max_effect = avg_change
        max_effect_threshold = r['threshold']

print(f"Optimal threshold: {max_effect_threshold*100:.0f}%")
print(f"  - Provides maximum effect ({max_effect*100:.1f}pp average change)")
print(f"  - While keeping data removal reasonable")

# Save best filtered dataset
best_mask = (merged_df['Consensus_Rate'] < max_effect_threshold) | \
            (merged_df['Actual_Choice'] == merged_df['Majority_Choice'])
best_filtered = merged_df[best_mask].copy()
best_filtered.to_csv(f'dataset_method1_{int(max_effect_threshold*100)}pct.csv', index=False)
print(f"\nBest filtered dataset saved to: dataset_method1_{int(max_effect_threshold*100)}pct.csv")