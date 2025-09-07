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

print("=" * 80)
print("TWO-STAGE FILTERING: Participant Quartile + Response Consensus")
print("=" * 80)

# STAGE 1: Remove bottom quartile participants
bottom_quartile = participant_df.nsmallest(int(len(participant_df) * 0.25), 'Mean_Agreement')
outlier_participant_ids = bottom_quartile['UserID'].values

print(f"\nSTAGE 1: Removing bottom quartile participants")
print(f"Participants removed: {len(outlier_participant_ids)}/{len(participant_df)}")
for _, p in bottom_quartile.iterrows():
    print(f"  - {p['Name']}: {p['Mean_Agreement']:.1%} agreement")

# Apply stage 1 filtering
stage1_df = merged_df[~merged_df['UserID'].isin(outlier_participant_ids)].copy()
print(f"\nAfter Stage 1: {len(stage1_df)}/{len(merged_df)} responses kept ({len(stage1_df)/len(merged_df)*100:.1f}%)")

# Calculate consensus for remaining data
tuple_stats_stage1 = stage1_df.groupby(['TupleID', 'Pair Type']).agg({
    'Actual_Choice': [
        lambda x: x.value_counts(normalize=True).iloc[0] if len(x) > 0 else 0,  # consensus rate
        lambda x: x.value_counts().index[0] if len(x) > 0 else None,  # majority choice
        'count'  # total votes
    ]
}).reset_index()
tuple_stats_stage1.columns = ['TupleID', 'Pair Type', 'Consensus_Rate', 'Majority_Choice', 'Total_Votes']

# Merge consensus info
stage1_df = stage1_df.merge(tuple_stats_stage1[['TupleID', 'Pair Type', 'Consensus_Rate', 'Majority_Choice']], 
                            on=['TupleID', 'Pair Type'], how='left')

# STAGE 2: Apply consensus filtering at different thresholds
consensus_thresholds = [0.65, 0.75]
combined_results = []

print("\nSTAGE 2: Applying consensus filtering to cleaned data")
print("-" * 60)

for threshold in consensus_thresholds:
    # Apply consensus filter
    mask = (stage1_df['Consensus_Rate'] < threshold) | \
           (stage1_df['Actual_Choice'] == stage1_df['Majority_Choice'])
    stage2_df = stage1_df[mask].copy()
    
    # Fit model
    results, _, _, _ = fit_bradley_terry_with_ci(stage2_df)
    
    # Calculate statistics
    n_removed_stage2 = len(stage1_df) - len(stage2_df)
    total_removed = len(merged_df) - len(stage2_df)
    pct_total_removed = (total_removed / len(merged_df)) * 100
    
    print(f"\nConsensus threshold: {threshold*100:.0f}%")
    print(f"  Stage 2 removed: {n_removed_stage2} responses")
    print(f"  Total kept: {len(stage2_df)}/{len(merged_df)} ({100-pct_total_removed:.1f}%)")
    print(f"  Results:")
    for r in results:
        print(f"    {r['pair']}: {r['prob']:.3f} [{r['ci_lower']:.3f}-{r['ci_upper']:.3f}]")
    
    combined_results.append({
        'threshold': threshold,
        'n_final': len(stage2_df),
        'n_removed_stage2': n_removed_stage2,
        'total_removed': total_removed,
        'pct_removed': pct_total_removed,
        'results': results
    })

# Also run single-stage filtering for comparison
print("\n" + "=" * 80)
print("COMPARISON: Single-Stage Response Filtering (no participant removal)")
print("-" * 80)

# Calculate consensus for full data
tuple_stats_full = merged_df.groupby(['TupleID', 'Pair Type']).agg({
    'Actual_Choice': [
        lambda x: x.value_counts(normalize=True).iloc[0] if len(x) > 0 else 0,
        lambda x: x.value_counts().index[0] if len(x) > 0 else None,
        'count'
    ]
}).reset_index()
tuple_stats_full.columns = ['TupleID', 'Pair Type', 'Consensus_Rate', 'Majority_Choice', 'Total_Votes']

merged_df_with_consensus = merged_df.merge(
    tuple_stats_full[['TupleID', 'Pair Type', 'Consensus_Rate', 'Majority_Choice']], 
    on=['TupleID', 'Pair Type'], how='left')

single_stage_results = []

for threshold in consensus_thresholds:
    mask = (merged_df_with_consensus['Consensus_Rate'] < threshold) | \
           (merged_df_with_consensus['Actual_Choice'] == merged_df_with_consensus['Majority_Choice'])
    filtered_df = merged_df_with_consensus[mask].copy()
    
    results, _, _, _ = fit_bradley_terry_with_ci(filtered_df)
    
    n_removed = len(merged_df) - len(filtered_df)
    pct_removed = (n_removed / len(merged_df)) * 100
    
    print(f"\nThreshold {threshold*100:.0f}%: {n_removed} removed ({pct_removed:.1f}%)")
    for r in results:
        print(f"  {r['pair']}: {r['prob']:.3f}")
    
    single_stage_results.append({
        'threshold': threshold,
        'n_removed': n_removed,
        'pct_removed': pct_removed,
        'results': results
    })

# Get baseline
baseline_results, _, _, _ = fit_bradley_terry_with_ci(merged_df)

# Get Stage 1 only results (bottom quartile removed, no consensus filtering)
stage1_only_results, _, _, _ = fit_bradley_terry_with_ci(stage1_df)

# Create single bar graph visualization
fig, ax = plt.subplots(1, 1, figsize=(14, 7))

comparisons = ['LOGPROB vs MI', 'TOKENS vs MI', 'LOGPROB vs TOKENS']
x_pos = np.arange(len(comparisons))
bar_width = 0.15
offset_positions = [-2, -1, 0, 1, 2]  # For 5 bars

# Plot bars for each method
# 1. Baseline
baseline_probs = [r['prob'] for r in baseline_results]
ax.bar(x_pos + offset_positions[0]*bar_width, baseline_probs, bar_width,
       color='gray', alpha=0.6, label='Baseline', edgecolor='black', linewidth=1.5)

# 2. Stage 1 only (bottom quartile removed)
stage1_probs = [r['prob'] for r in stage1_only_results]
stage1_errors = [[r['prob'] - r['ci_lower'] for r in stage1_only_results],
                 [r['ci_upper'] - r['prob'] for r in stage1_only_results]]
ax.bar(x_pos + offset_positions[1]*bar_width, stage1_probs, bar_width,
       yerr=stage1_errors, capsize=5,
       color='#3498db', alpha=0.8, label='Stage 1 only (quartile)',
       edgecolor='black', linewidth=1.5, error_kw={'linewidth': 2})

# 3. Stage 2 only 65% (consensus filtering on all data)
stage2_only_65 = single_stage_results[0]['results']
stage2_only_65_probs = [r['prob'] for r in stage2_only_65]
stage2_only_65_errors = [[r['prob'] - r['ci_lower'] for r in stage2_only_65],
                         [r['ci_upper'] - r['prob'] for r in stage2_only_65]]
ax.bar(x_pos + offset_positions[2]*bar_width, stage2_only_65_probs, bar_width,
       yerr=stage2_only_65_errors, capsize=5,
       color='#9b59b6', alpha=0.8, label='Stage 2 only (65%)',
       edgecolor='black', linewidth=1.5, error_kw={'linewidth': 2})

# 4. Two-stage 65%
two_65 = combined_results[0]['results']
two_65_probs = [r['prob'] for r in two_65]
two_65_errors = [[r['prob'] - r['ci_lower'] for r in two_65],
                 [r['ci_upper'] - r['prob'] for r in two_65]]
ax.bar(x_pos + offset_positions[3]*bar_width, two_65_probs, bar_width,
       yerr=two_65_errors, capsize=5,
       color='#e74c3c', alpha=0.8, label='Two-stage (65%)',
       edgecolor='black', linewidth=1.5, error_kw={'linewidth': 2})

# 5. Two-stage 75%
two_75 = combined_results[1]['results']
two_75_probs = [r['prob'] for r in two_75]
two_75_errors = [[r['prob'] - r['ci_lower'] for r in two_75],
                 [r['ci_upper'] - r['prob'] for r in two_75]]
ax.bar(x_pos + offset_positions[4]*bar_width, two_75_probs, bar_width,
       yerr=two_75_errors, capsize=5,
       color='#2ecc71', alpha=0.8, label='Two-stage (75%)',
       edgecolor='black', linewidth=1.5, error_kw={'linewidth': 2})

# Add significance line
ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=2, label='No preference')

# Formatting
ax.set_ylim([0, 1.0])
ax.set_xticks(x_pos)
ax.set_xticklabels(comparisons, fontsize=12)
ax.set_ylabel('P(First metric preferred)', fontsize=13)
ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
ax.set_title('Comparison of Filtering Methods at 65% and 75% Consensus Thresholds', 
            fontsize=14, fontweight='bold')
ax.legend(loc='upper left', fontsize=10, ncol=2)
ax.grid(True, alpha=0.3, axis='y')

# Add sample size annotations
for i, comp in enumerate(comparisons):
    y_pos = 0.02
    # Show data retention for two-stage 65% (most aggressive)
    n_kept = combined_results[0]['n_final']
    ax.text(x_pos[i], y_pos, f'n={n_kept}/130', ha='center', fontsize=9, style='italic')
plt.tight_layout()
plt.savefig('consensus_two_stage_filtering.png', dpi=300, bbox_inches='tight')
print("\nSaved: consensus_two_stage_filtering.png")

# Save best filtered dataset (two-stage with 65% consensus)
best_two_stage = combined_results[0]  # 65% threshold
final_mask = (stage1_df['Consensus_Rate'] < 0.65) | \
             (stage1_df['Actual_Choice'] == stage1_df['Majority_Choice'])
final_filtered = stage1_df[final_mask].copy()
final_filtered.to_csv('dataset_two_stage_filtered.csv', index=False)

print("\n" + "=" * 80)
print("FINAL RECOMMENDATION")
print("=" * 80)
print("Two-stage filtering (Bottom Quartile + 65% Consensus) is optimal:")
print(f"  • Removes {best_two_stage['total_removed']} responses ({best_two_stage['pct_removed']:.1f}%)")
print(f"  • Average effect: {sum(abs(best_two_stage['results'][i]['prob'] - baseline_results[i]['prob']) for i in range(3))/3*100:.1f}pp")
print("  • Combines participant-level and response-level quality control")
print("\nFinal filtered dataset saved to: dataset_two_stage_filtered.csv")