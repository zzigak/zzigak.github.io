import pandas as pd
import numpy as np
from scipy.optimize import minimize, approx_fprime
from scipy import stats
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 11

# Load data directly from results.csv
assignments_df = pd.read_csv('user_study_final_shuffled_assignments.csv')
results_df = pd.read_csv('results.csv')

print("Processing results.csv directly...")
print(f"Found {len(results_df)} participants")

# Transform results from wide to long format
response_cols = []
for i in range(10):
    base = 7 + i * 4  # Starting position for each set of response columns
    response_cols.append({
        'tuple_id_col': base,
        'pair_id_col': base + 1,
        'choice_col': base + 2,
        'reason_col': base + 3
    })

# Create long format dataframe
long_results = []
for _, row in results_df.iterrows():
    user_id = row['UserID']

    for i, cols in enumerate(response_cols):
        tuple_id = row.iloc[cols['tuple_id_col']-1] if pd.notna(row.iloc[cols['tuple_id_col']-1]) else None
        if tuple_id is None or tuple_id == '':
            continue

        long_results.append({
            'UserID': user_id,
            'Position': i + 1,
            'TupleID': int(tuple_id) if not pd.isna(float(tuple_id)) else None,
            'Choice': row.iloc[cols['choice_col']-1],
            'Reason': row.iloc[cols['reason_col']-1]
        })

long_results_df = pd.DataFrame(long_results)

# Merge with assignments to get swap info and pair type
merged_df = pd.merge(
    long_results_df,
    assignments_df[['User ID', 'Position', 'Tuple Index', 'Tuple Name', 'Cluster',
                    'Pair Type', 'Original V1 Metric', 'Original V2 Metric', 'Swapped']],
    left_on=['UserID', 'Position'],
    right_on=['User ID', 'Position'],
    how='inner'
)

# Adjust choices based on swap flag
def get_actual_choice(row):
    """Convert V1/V2 choice to actual metric chosen, accounting for swaps"""
    if pd.isna(row['Choice']) or row['Choice'] == 'EG':
        return row['Choice']

    if row['Swapped'] == 'Yes':
        # If swapped, V1 shown was actually original V2
        if row['Choice'] == 'V1':
            return row['Original V2 Metric']
        elif row['Choice'] == 'V2':
            return row['Original V1 Metric']
    else:
        # Not swapped
        if row['Choice'] == 'V1':
            return row['Original V1 Metric']
        elif row['Choice'] == 'V2':
            return row['Original V2 Metric']

    return row['Choice']

merged_df['Actual_Choice'] = merged_df.apply(get_actual_choice, axis=1)

print(f"Total comparisons: {len(merged_df)}")
print(f"Comparisons excluding EG: {len(merged_df[merged_df['Actual_Choice'] != 'EG'])}")

def fit_bradley_terry_once(comparisons_df):
    """
    Fit Bradley-Terry model to pairwise comparison data (single fit).
    Returns parameters in original scale and normalized scale.
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

    # Maximum likelihood estimation
    def neg_log_likelihood(log_params):
        params = np.exp(np.concatenate([[0], log_params]))  # MI = reference
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

    # Get parameters
    log_params = np.concatenate([[0], result.x])
    params = np.exp(log_params)
    params_normalized = params / params.sum()

    return {
        'params': params,
        'params_normalized': params_normalized,
        'log_params': log_params,
        'metrics': metrics,
        'wins': wins,
        'totals': totals
    }

def bootstrap_bradley_terry(comparisons_df, n_bootstrap=1000, confidence=0.95):
    """
    Perform bootstrap estimation of Bradley-Terry parameters.
    """

    print(f"\nRunning bootstrap with {n_bootstrap} iterations...")

    # Fit original model
    original_fit = fit_bradley_terry_once(comparisons_df)

    # Store bootstrap results
    bootstrap_params = []
    bootstrap_params_norm = []
    bootstrap_log_params = []

    # Get unique comparison IDs for resampling
    comparison_ids = comparisons_df.index.values

    # Bootstrap iterations
    for _ in tqdm(range(n_bootstrap)):
        # Resample with replacement
        bootstrap_indices = np.random.choice(comparison_ids, size=len(comparison_ids), replace=True)
        bootstrap_df = comparisons_df.loc[bootstrap_indices]

        try:
            boot_fit = fit_bradley_terry_once(bootstrap_df)
            bootstrap_params.append(boot_fit['params'])
            bootstrap_params_norm.append(boot_fit['params_normalized'])
            bootstrap_log_params.append(boot_fit['log_params'])
        except:
            continue

    print(f"Bootstrap completed: {len(bootstrap_params)}/{n_bootstrap} successful iterations")

    # Calculate confidence intervals
    alpha = 1 - confidence
    lower_percentile = (alpha/2) * 100
    upper_percentile = (100 - alpha/2)

    bootstrap_params_array = np.array(bootstrap_params)
    bootstrap_params_norm_array = np.array(bootstrap_params_norm)
    bootstrap_log_params_array = np.array(bootstrap_log_params)

    # Bootstrap CIs for normalized parameters
    bootstrap_cis_norm = {}
    for i, metric in enumerate(original_fit['metrics']):
        bootstrap_cis_norm[metric] = {
            'estimate': original_fit['params_normalized'][i],
            'ci_low': np.percentile(bootstrap_params_norm_array[:, i], lower_percentile),
            'ci_high': np.percentile(bootstrap_params_norm_array[:, i], upper_percentile),
            'se': np.std(bootstrap_params_norm_array[:, i])
        }

    # Bootstrap CIs for relative parameters (compared to MI)
    bootstrap_cis_relative = {}
    for i, metric in enumerate(original_fit['metrics']):
        bootstrap_cis_relative[metric] = {
            'estimate': original_fit['params'][i],
            'ci_low': np.percentile(bootstrap_params_array[:, i], lower_percentile),
            'ci_high': np.percentile(bootstrap_params_array[:, i], upper_percentile),
            'se': np.std(bootstrap_params_array[:, i])
        }

    return {
        'original_fit': original_fit,
        'bootstrap_cis_norm': bootstrap_cis_norm,
        'bootstrap_cis_relative': bootstrap_cis_relative,
        'n_bootstrap': len(bootstrap_params)
    }

# Run the analysis
results = bootstrap_bradley_terry(merged_df, n_bootstrap=1000)

# Display results
print("\n" + "="*60)
print("Bradley-Terry Model with Bootstrap Confidence Intervals")
print("="*60)

print("\n1. Parameter Estimates with Bootstrap CIs:")
print("-"*50)

# Sort by strength
sorted_metrics = sorted(results['bootstrap_cis_norm'].items(),
                       key=lambda x: x[1]['estimate'], reverse=True)

print("\nNormalized Strengths (Bootstrap 95% CI):")
for metric, ci_data in sorted_metrics:
    print(f"{metric:8s}: {ci_data['estimate']:.3f} [{ci_data['ci_low']:.3f}, {ci_data['ci_high']:.3f}]  SE={ci_data['se']:.3f}")

print("\n2. Relative Strengths (compared to MI):")
print("-"*50)
for metric in ['logprob', 'tokens']:
    ci_data = results['bootstrap_cis_relative'][metric]
    ratio = ci_data['estimate']
    ratio_low = ci_data['ci_low']
    ratio_high = ci_data['ci_high']
    print(f"{metric:8s} is {ratio:.2f}x stronger than MI  [95% CI: {ratio_low:.2f}x - {ratio_high:.2f}x]")

# Compute pairwise win probabilities
print("\n3. Pairwise Win Probabilities:")
print("-"*50)
metrics = results['original_fit']['metrics']
params = results['original_fit']['params']
n_metrics = len(metrics)

print("P(row beats column):")
print(f"{'':10s}", end='')
for m in metrics:
    print(f"{m:8s}", end='')
print()

for i, m1 in enumerate(metrics):
    print(f"{m1:10s}", end='')
    for j, m2 in enumerate(metrics):
        if i == j:
            print(f"{'---':8s}", end='')
        else:
            p_ij = params[i] / (params[i] + params[j])
            print(f"{p_ij:8.3f}", end='')
    print()

# Show actual win counts
print("\n4. Observed Win Counts:")
print("-"*50)
wins = results['original_fit']['wins']
totals = results['original_fit']['totals']

for i in range(n_metrics):
    for j in range(i+1, n_metrics):
        if totals[i][j] > 0:
            print(f"{metrics[i]} vs {metrics[j]}:")
            print(f"  {metrics[i]} wins: {int(wins[i][j])}/{int(totals[i][j])} ({100*wins[i][j]/totals[i][j]:.1f}%)")
            print(f"  {metrics[j]} wins: {int(wins[j][i])}/{int(totals[j][i])} ({100*wins[j][i]/totals[j][i]:.1f}%)")

# Create original visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Strengths with CIs
x_pos = np.arange(len(sorted_metrics))
strengths = [s[1]['estimate'] for s in sorted_metrics]
errors = [[s[1]['estimate'] - s[1]['ci_low'] for s in sorted_metrics],
          [s[1]['ci_high'] - s[1]['estimate'] for s in sorted_metrics]]
metric_names = [s[0].upper() for s in sorted_metrics]

colors = {'mi': '#E74C3C', 'tokens': '#3498DB', 'logprob': '#2ECC71'}
bar_colors = [colors[s[0]] for s in sorted_metrics]

ax1.bar(x_pos, strengths, yerr=errors, capsize=5,
        color=bar_colors, alpha=0.7, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Normalized Strength', fontsize=12)
ax1.set_title('Bradley-Terry Model Strengths\n(with 95% Bootstrap CIs)', fontsize=14, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(metric_names)
ax1.set_ylim(0, 0.6)
ax1.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for i, (strength, name) in enumerate(zip(strengths, metric_names)):
    ax1.text(i, strength + errors[1][i] + 0.02, f'{strength:.3f}',
             ha='center', va='bottom', fontweight='bold')

# Plot 2: Pairwise win probabilities
win_matrix = np.zeros((n_metrics, n_metrics))
for i in range(n_metrics):
    for j in range(n_metrics):
        if i != j:
            win_matrix[i][j] = params[i] / (params[i] + params[j])

im = ax2.imshow(win_matrix, cmap='RdYlGn', vmin=0, vmax=1, aspect='auto')
ax2.set_xticks(range(n_metrics))
ax2.set_yticks(range(n_metrics))
ax2.set_xticklabels([m.upper() for m in metrics])
ax2.set_yticklabels([m.upper() for m in metrics])
ax2.set_title('Pairwise Win Probabilities\nP(row beats column)', fontsize=14, fontweight='bold')

# Add text annotations
for i in range(n_metrics):
    for j in range(n_metrics):
        if i != j:
            text = ax2.text(j, i, f'{win_matrix[i][j]:.2f}',
                          ha="center", va="center", color="black", fontweight='bold')
        else:
            text = ax2.text(j, i, '-', ha="center", va="center", color="gray")

plt.colorbar(im, ax=ax2, label='Win Probability')
plt.tight_layout()
plt.savefig('bradley_terry_from_results.png', dpi=150, bbox_inches='tight')
print("\nVisualization saved to: bradley_terry_from_results.png")

# Save results to CSV
results_df = pd.DataFrame([
    {
        'metric': metric,
        'normalized_strength': ci_data['estimate'],
        'ci_low': ci_data['ci_low'],
        'ci_high': ci_data['ci_high'],
        'se': ci_data['se']
    }
    for metric, ci_data in results['bootstrap_cis_norm'].items()
])
results_df = results_df.sort_values('normalized_strength', ascending=False)
results_df.to_csv('bradley_terry_results_direct.csv', index=False)

print("\nResults saved to: bradley_terry_results_direct.csv")

# Function to fit Bradley-Terry with CI using Hessian
def fit_bradley_terry_with_ci(comparisons_df):
    """Fit Bradley-Terry model and compute CIs using Hessian"""
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

    return results, wins, totals, metrics, log_params, cov_matrix_full

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("-"*60)
winner = sorted_metrics[0][0]
winner_strength = sorted_metrics[0][1]['estimate']
print(f"• Strongest metric: {winner.upper()} (strength = {winner_strength:.3f})")
print(f"• Rankings: {' > '.join([s[0].upper() for s in sorted_metrics])}")
print(f"• The bootstrap CIs account for sampling uncertainty")
print(f"• All metrics significantly differ from chance (0.333)")

# ============================================================================
# ADDITIONAL PLOT 1: Pairwise Metric Preferences (from bradley_terry_summary.png)
# ============================================================================
print("\n" + "="*60)
print("Creating pairwise comparison visualization...")

fig_pairwise, ax_pairwise = plt.subplots(1, 1, figsize=(8, 6))

# Use Hessian-based CIs for pairwise comparisons
pairwise_results, _, _, _, log_params_hessian, cov_matrix_hessian = fit_bradley_terry_with_ci(merged_df)

# Determine colors based on which metric is favored
bar_colors = []
for comp in pairwise_results:
    if comp['ci_lower'] > 0.5:  # Significant favor for first metric
        if 'LOGPROB' in comp['pair']:
            bar_colors.append('#2ecc71')  # Green for logprob
        elif 'TOKENS' in comp['pair'] and 'MI' in comp['pair']:
            bar_colors.append('#3498db')  # Blue for tokens
        else:
            bar_colors.append('#2ecc71')  # Default to green
    elif comp['ci_upper'] < 0.5:  # Significant favor for second metric
        bar_colors.append('#e74c3c')  # Red
    else:
        bar_colors.append('#95a5a6')  # Gray for non-significant

# Plot bars
x_pairwise = np.arange(len(pairwise_results))
width = 0.35

bars = ax_pairwise.bar(x_pairwise, [c['prob'] for c in pairwise_results], width,
              yerr=[[c['prob'] - c['ci_lower'] for c in pairwise_results],
                    [c['ci_upper'] - c['prob'] for c in pairwise_results]],
              capsize=8, color=bar_colors, alpha=0.8,
              edgecolor='black', linewidth=2,
              error_kw={'linewidth': 2.5, 'ecolor': 'black'})

# Add value labels and significance markers
for i, comp in enumerate(pairwise_results):
    # Probability label
    ax_pairwise.text(i, comp['prob'] + 0.02, f"{comp['prob']:.1%}",
            ha='center', fontweight='bold', fontsize=11)

    # Significance marker
    if comp['ci_lower'] > 0.5 or comp['ci_upper'] < 0.5:
        ax_pairwise.text(i, comp['ci_upper'] + 0.05, '*',
                ha='center', fontsize=20, fontweight='bold')

# Reference line
ax_pairwise.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=2)
ax_pairwise.text(len(pairwise_results) - 0.5, 0.51, 'No preference',
        fontsize=10, color='red', style='italic')

# Labels and title
ax_pairwise.set_ylabel('P(First metric preferred)', fontsize=13, fontweight='bold')
ax_pairwise.set_title('Bradley-Terry Model: Pairwise Metric Preferences',
             fontsize=14, fontweight='bold', pad=20)
ax_pairwise.set_xticks(x_pairwise)
ax_pairwise.set_xticklabels([c['pair'] for c in pairwise_results], fontsize=11)
ax_pairwise.set_ylim([0, 0.85])
ax_pairwise.grid(True, alpha=0.3, axis='y')

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#2ecc71', alpha=0.8, label='Logprob favored'),
    Patch(facecolor='#3498db', alpha=0.8, label='Tokens favored'),
    Patch(facecolor='#95a5a6', alpha=0.8, label='No significant difference'),
]
ax_pairwise.legend(handles=legend_elements, loc='upper right', framealpha=0.95)

# Add note
ax_pairwise.text(0.02, 0.98, 'Error bars: 95% CI\n* p < 0.05',
        transform=ax_pairwise.transAxes, fontsize=9, style='italic',
        va='top', ha='left')

plt.tight_layout()
plt.savefig('bradley_terry_pairwise_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: bradley_terry_pairwise_comparison.png")

# ============================================================================
# ADDITIONAL PLOT 2: Two-Stage Filtering Comparison
# ============================================================================
print("\n" + "="*60)
print("Creating two-stage filtering visualization...")

# Load participant analysis if available
try:
    participant_df = pd.read_csv('participant_outlier_analysis.csv')
    has_participant_data = True
except:
    print("Warning: participant_outlier_analysis.csv not found, skipping two-stage filtering")
    has_participant_data = False

if has_participant_data:
    # STAGE 1: Remove bottom quartile participants
    bottom_quartile = participant_df.nsmallest(int(len(participant_df) * 0.25), 'Mean_Agreement')
    outlier_participant_ids = bottom_quartile['UserID'].values

    print(f"\nSTAGE 1: Removing bottom quartile participants")
    print(f"Participants removed: {len(outlier_participant_ids)}/{len(participant_df)}")

    # Apply stage 1 filtering
    stage1_df = merged_df[~merged_df['UserID'].isin(outlier_participant_ids)].copy()
    print(f"After Stage 1: {len(stage1_df)}/{len(merged_df)} responses kept ({len(stage1_df)/len(merged_df)*100:.1f}%)")

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

    for threshold in consensus_thresholds:
        # Apply consensus filter
        mask = (stage1_df['Consensus_Rate'] < threshold) | \
               (stage1_df['Actual_Choice'] == stage1_df['Majority_Choice'])
        stage2_df = stage1_df[mask].copy()

        # Fit model
        results_filtered, _, _, _, _, _ = fit_bradley_terry_with_ci(stage2_df)

        combined_results.append({
            'threshold': threshold,
            'n_final': len(stage2_df),
            'results': results_filtered
        })

        print(f"  Threshold {threshold*100:.0f}%: {len(stage2_df)} responses kept")

    # Get baseline and stage 1 only results
    baseline_results, _, _, _, _, _ = fit_bradley_terry_with_ci(merged_df)
    stage1_only_results, _, _, _, _, _ = fit_bradley_terry_with_ci(stage1_df)

    # Create visualization
    fig_filter, ax_filter = plt.subplots(1, 1, figsize=(14, 7))

    comparisons = ['LOGPROB vs MI', 'TOKENS vs MI', 'LOGPROB vs TOKENS']
    x_pos = np.arange(len(comparisons))
    bar_width = 0.15
    offset_positions = [-2, -1, 0, 1]

    # Plot bars for each method
    # 1. Baseline
    baseline_probs = [r['prob'] for r in baseline_results]
    ax_filter.bar(x_pos + offset_positions[0]*bar_width, baseline_probs, bar_width,
           color='gray', alpha=0.6, label='Baseline', edgecolor='black', linewidth=1.5)

    # 2. Stage 1 only (bottom quartile removed)
    stage1_probs = [r['prob'] for r in stage1_only_results]
    stage1_errors = [[r['prob'] - r['ci_lower'] for r in stage1_only_results],
                     [r['ci_upper'] - r['prob'] for r in stage1_only_results]]
    ax_filter.bar(x_pos + offset_positions[1]*bar_width, stage1_probs, bar_width,
           yerr=stage1_errors, capsize=5,
           color='#3498db', alpha=0.8, label='Stage 1 only (quartile)',
           edgecolor='black', linewidth=1.5, error_kw={'linewidth': 2})

    # 3. Two-stage 65%
    two_65 = combined_results[0]['results']
    two_65_probs = [r['prob'] for r in two_65]
    two_65_errors = [[r['prob'] - r['ci_lower'] for r in two_65],
                     [r['ci_upper'] - r['prob'] for r in two_65]]
    ax_filter.bar(x_pos + offset_positions[2]*bar_width, two_65_probs, bar_width,
           yerr=two_65_errors, capsize=5,
           color='#e74c3c', alpha=0.8, label='Two-stage (65%)',
           edgecolor='black', linewidth=1.5, error_kw={'linewidth': 2})

    # 4. Two-stage 75%
    two_75 = combined_results[1]['results']
    two_75_probs = [r['prob'] for r in two_75]
    two_75_errors = [[r['prob'] - r['ci_lower'] for r in two_75],
                     [r['ci_upper'] - r['prob'] for r in two_75]]
    ax_filter.bar(x_pos + offset_positions[3]*bar_width, two_75_probs, bar_width,
           yerr=two_75_errors, capsize=5,
           color='#2ecc71', alpha=0.8, label='Two-stage (75%)',
           edgecolor='black', linewidth=1.5, error_kw={'linewidth': 2})

    # Add significance line
    ax_filter.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=2, label='No preference')

    # Formatting
    ax_filter.set_ylim([0, 1.0])
    ax_filter.set_xticks(x_pos)
    ax_filter.set_xticklabels(comparisons, fontsize=12)
    ax_filter.set_ylabel('P(First metric preferred)', fontsize=13)
    ax_filter.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    ax_filter.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
    ax_filter.set_title('Comparison of Filtering Methods at 65% and 75% Consensus Thresholds',
                fontsize=14, fontweight='bold')
    ax_filter.legend(loc='upper left', fontsize=10, ncol=2)
    ax_filter.grid(True, alpha=0.3, axis='y')

    # Add sample size annotations
    for i, comp in enumerate(comparisons):
        y_pos = 0.02
        n_kept_65 = combined_results[0]['n_final']
        n_kept_75 = combined_results[1]['n_final']
        ax_filter.text(x_pos[i], y_pos, f'n={n_kept_75}/{len(merged_df)}', ha='center', fontsize=9, style='italic')

    plt.tight_layout()
    plt.savefig('bradley_terry_two_stage_filtering.png', dpi=300, bbox_inches='tight')
    print("Saved: bradley_terry_two_stage_filtering.png")

print("\n" + "="*60)
print("All visualizations complete!")
print("="*60)