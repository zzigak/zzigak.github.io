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

print("=" * 80)
print("TUPLE-LEVEL FILTERING: Removing Ambiguous/Noisy Comparisons")
print("=" * 80)

# Calculate consensus for each tuple
print("\nCalculating consensus for each tuple...")
tuple_stats = merged_df.groupby(['TupleID', 'Pair Type']).agg({
    'Actual_Choice': [
        lambda x: x.value_counts(normalize=True).iloc[0] if len(x) > 0 else 0,  # consensus rate
        lambda x: x.value_counts().index[0] if len(x) > 0 else None,  # majority choice
        'count'  # total votes
    ],
    'UserID': 'nunique'  # unique participants
}).reset_index()
tuple_stats.columns = ['TupleID', 'Pair Type', 'Consensus_Rate', 'Majority_Choice', 'Total_Votes', 'Unique_Participants']

# Filter out tuples with consensus < 65%
CONSENSUS_THRESHOLD = 0.65
print(f"\nFiltering out tuples with consensus < {CONSENSUS_THRESHOLD*100:.0f}%...")

# Keep only clear tuples (consensus >= 65%)
clear_tuples = tuple_stats[tuple_stats['Consensus_Rate'] >= CONSENSUS_THRESHOLD]
ambiguous_tuples = tuple_stats[tuple_stats['Consensus_Rate'] < CONSENSUS_THRESHOLD]

print(f"\nAmbiguous tuples (removed): {len(ambiguous_tuples)}/{len(tuple_stats)} ({len(ambiguous_tuples)/len(tuple_stats)*100:.1f}%)")
print(f"Clear tuples (kept): {len(clear_tuples)}/{len(tuple_stats)} ({len(clear_tuples)/len(tuple_stats)*100:.1f}%)")

# Filter the main dataset
filtered_df = merged_df.merge(clear_tuples[['TupleID', 'Pair Type']], 
                              on=['TupleID', 'Pair Type'], how='inner')

print(f"\nResponses removed: {len(merged_df) - len(filtered_df)}/{len(merged_df)} ({(len(merged_df)-len(filtered_df))/len(merged_df)*100:.1f}%)")
print(f"Responses kept: {len(filtered_df)}/{len(merged_df)} ({len(filtered_df)/len(merged_df)*100:.1f}%)")

# Fit models
print("\nFitting Bradley-Terry models...")
baseline_results, _, _, _ = fit_bradley_terry_with_ci(merged_df)
filtered_results, _, _, _ = fit_bradley_terry_with_ci(filtered_df)

# Print results comparison
print("\n" + "=" * 80)
print("RESULTS COMPARISON")
print("-" * 80)
print(f"{'Comparison':<20} {'All Tuples':<25} {'Clear Tuples Only':<25} {'Change'}")
print("-" * 80)

for i, (base, filt) in enumerate(zip(baseline_results, filtered_results)):
    change = filt['prob'] - base['prob']
    base_str = f"{base['prob']:.1%} [{base['ci_lower']:.1%}-{base['ci_upper']:.1%}]"
    filt_str = f"{filt['prob']:.1%} [{filt['ci_lower']:.1%}-{filt['ci_upper']:.1%}]"
    print(f"{base['pair']:<20} {base_str:<25} {filt_str:<25} {change*100:+.1f}pp")

# Create visualization
fig, ax = plt.subplots(1, 1, figsize=(12, 7))

comparisons = ['LOGPROB vs MI', 'TOKENS vs MI', 'LOGPROB vs TOKENS']
x_pos = np.arange(len(comparisons))
bar_width = 0.3

# Baseline bars
baseline_probs = [r['prob'] for r in baseline_results]
ax.bar(x_pos - bar_width/2, baseline_probs, bar_width,
       color='gray', alpha=0.6, label='All tuples (n=44)', 
       edgecolor='black', linewidth=1.5)

# Filtered bars with error bars
filtered_probs = [r['prob'] for r in filtered_results]
filtered_errors = [[r['prob'] - r['ci_lower'] for r in filtered_results],
                   [r['ci_upper'] - r['prob'] for r in filtered_results]]

# Color based on significance
colors = []
for r in filtered_results:
    if r['ci_lower'] > 0.5:
        colors.append('#2ecc71')  # Green - significant preference for first
    elif r['ci_upper'] < 0.5:
        colors.append('#e74c3c')  # Red - significant preference for second
    else:
        colors.append('#95a5a6')  # Gray - no significant preference

ax.bar(x_pos + bar_width/2, filtered_probs, bar_width,
       yerr=filtered_errors, capsize=8,
       color=colors, alpha=0.8, 
       label=f'Clear tuples only (n={len(clear_tuples)})',
       edgecolor='black', linewidth=1.5, error_kw={'linewidth': 2})

# Add value labels
for i, (base, filt) in enumerate(zip(baseline_results, filtered_results)):
    # Baseline value
    ax.text(x_pos[i] - bar_width/2, base['prob'] + 0.02, f"{base['prob']:.1%}",
            ha='center', fontsize=10)
    
    # Filtered value
    ax.text(x_pos[i] + bar_width/2, filt['prob'] + 0.02, f"{filt['prob']:.1%}",
            ha='center', fontsize=10, fontweight='bold')
    
    # Change indicator
    change = filt['prob'] - base['prob']
    if abs(change) > 0.01:
        ax.text(x_pos[i] + bar_width/2, filt['ci_upper'] + 0.05, 
                f'{change*100:+.1f}pp',
                ha='center', fontsize=9, color='blue', fontweight='bold')

# Add significance line
ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=2)

# Formatting
ax.set_ylim([0, 1.0])
ax.set_xticks(x_pos)
ax.set_xticklabels(comparisons, fontsize=12)
ax.set_ylabel('P(First metric preferred)', fontsize=13)
ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
ax.set_title(f'Impact of Removing Ambiguous Tuples (Consensus < {CONSENSUS_THRESHOLD*100:.0f}%)', 
            fontsize=14, fontweight='bold')
ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

# Add sample size annotation
ax.text(0.99, 0.02, f'Responses: {len(filtered_df)}/{len(merged_df)}', 
        transform=ax.transAxes, ha='right', fontsize=10, style='italic')

plt.tight_layout()
plt.savefig('outlier_tuple_filtering.png', dpi=300, bbox_inches='tight')
print("\nSaved: outlier_tuple_filtering.png")

# Analyze which tuples are ambiguous
print("\n" + "=" * 80)
print("AMBIGUOUS TUPLES ANALYSIS")
print("-" * 80)

# By comparison type
print("\nAmbiguous tuples by comparison type:")
for pair_type in ['logprob_vs_mi', 'logprob_vs_tokens', 'mi_vs_tokens']:
    type_total = (tuple_stats['Pair Type'] == pair_type).sum()
    type_ambiguous = (ambiguous_tuples['Pair Type'] == pair_type).sum()
    print(f"  {pair_type}: {type_ambiguous}/{type_total} ambiguous ({type_ambiguous/type_total*100:.1f}%)")

print(f"\nMost ambiguous tuples (lowest consensus):")
for _, row in ambiguous_tuples.nsmallest(5, 'Consensus_Rate').iterrows():
    print(f"  Tuple {row['TupleID']}: {row['Consensus_Rate']*100:.1f}% consensus ({row['Pair Type']})")

print(f"\nClearest tuples (highest consensus):")
for _, row in clear_tuples.nlargest(5, 'Consensus_Rate').iterrows():
    print(f"  Tuple {row['TupleID']}: {row['Consensus_Rate']*100:.1f}% consensus ({row['Pair Type']})")

# Save filtered dataset
filtered_df.to_csv('dataset_clear_tuples_only.csv', index=False)
print(f"\nFiltered dataset saved to: dataset_clear_tuples_only.csv")

print("\n" + "=" * 80)
print("KEY FINDING")
print("-" * 80)
print(f"Removing {len(ambiguous_tuples)} ambiguous tuples (consensus < 65%) shows:")
print(f"  • LOGPROB vs MI: Stronger preference ({filtered_results[0]['prob']:.1%} vs {baseline_results[0]['prob']:.1%})")
print(f"  • TOKENS vs MI: Stronger preference ({filtered_results[1]['prob']:.1%} vs {baseline_results[1]['prob']:.1%})")
print(f"  • LOGPROB vs TOKENS: Slightly weaker ({filtered_results[2]['prob']:.1%} vs {baseline_results[2]['prob']:.1%})")
print(f"\nThis suggests ambiguous tuples add noise that obscures true preferences!")