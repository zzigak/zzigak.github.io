import pandas as pd
import numpy as np
from scipy.optimize import minimize, approx_fprime
from scipy import stats
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Set publication style for paper
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.dpi'] = 300

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
            'ci_upper': ci_upper,
            'significant': ci_lower > 0.5 or ci_upper < 0.5
        })

    return results, len(comparisons_df[comparisons_df['Actual_Choice'] != 'EG'])

def create_consensus_plot(threshold, output_filename):
    """Create a single consensus threshold plot for paper"""

    # Load and process data from results.csv (same as bradley_terry_from_results.py)
    assignments_df = pd.read_csv('user_study_final_shuffled_assignments.csv')
    results_df = pd.read_csv('results.csv')

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

    print(f"\nProcessing {threshold*100:.0f}% consensus threshold...")

    # Calculate consensus for full dataset
    tuple_stats = merged_df.groupby(['TupleID', 'Pair Type']).agg({
        'Actual_Choice': [
            lambda x: x.value_counts(normalize=True).iloc[0] if len(x) > 0 else 0,
            lambda x: x.value_counts().index[0] if len(x) > 0 else None,
            'count'
        ]
    }).reset_index()
    tuple_stats.columns = ['TupleID', 'Pair Type', 'Consensus_Rate', 'Majority_Choice', 'Total_Votes']

    merged_df_with_consensus = merged_df.merge(
        tuple_stats[['TupleID', 'Pair Type', 'Consensus_Rate', 'Majority_Choice']],
        on=['TupleID', 'Pair Type'], how='left')

    # Get baseline results
    baseline_results, baseline_n = fit_bradley_terry_with_ci(merged_df)

    # Apply consensus filtering
    mask = (merged_df_with_consensus['Consensus_Rate'] < threshold) | \
           (merged_df_with_consensus['Actual_Choice'] == merged_df_with_consensus['Majority_Choice'])
    filtered_df = merged_df_with_consensus[mask].copy()

    # Get filtered results
    filtered_results, filtered_n = fit_bradley_terry_with_ci(filtered_df)

    # Print statistics
    n_removed = baseline_n - filtered_n
    pct_removed = (n_removed / baseline_n) * 100
    print(f"Responses removed: {n_removed}/{baseline_n} ({pct_removed:.1f}%)")
    print(f"Responses kept: {filtered_n}/{baseline_n} ({100-pct_removed:.1f}%)")

    # Create figure (compact for paper)
    fig, ax = plt.subplots(1, 1, figsize=(5, 3.5))

    comparisons = ['LOGPROB\nvs MI', 'TOKENS\nvs MI', 'LOGPROB\nvs TOKENS']
    x = np.arange(len(comparisons))
    width = 0.35

    # Determine colors based on significance
    baseline_colors = []
    filtered_colors = []

    for i, (b_res, f_res) in enumerate(zip(baseline_results, filtered_results)):
        # Baseline color
        if b_res['significant']:
            if 'LOGPROB' in b_res['pair'] and b_res['prob'] > 0.5:
                baseline_colors.append('#2ecc71')  # Green for logprob
            elif 'TOKENS' in b_res['pair'] and 'MI' in b_res['pair'] and b_res['prob'] > 0.5:
                baseline_colors.append('#3498db')  # Blue for tokens
            else:
                baseline_colors.append('#e74c3c')  # Red for other
        else:
            baseline_colors.append('#95a5a6')  # Gray for non-significant

        # Filtered color
        if f_res['significant']:
            if 'LOGPROB' in f_res['pair'] and f_res['prob'] > 0.5:
                filtered_colors.append('#2ecc71')  # Green for logprob
            elif 'TOKENS' in f_res['pair'] and 'MI' in f_res['pair'] and f_res['prob'] > 0.5:
                filtered_colors.append('#3498db')  # Blue for tokens
            else:
                filtered_colors.append('#e74c3c')  # Red for other
        else:
            filtered_colors.append('#95a5a6')  # Gray for non-significant

    # Plot baseline
    baseline_probs = [r['prob'] for r in baseline_results]
    baseline_errors = [[r['prob'] - r['ci_lower'] for r in baseline_results],
                       [r['ci_upper'] - r['prob'] for r in baseline_results]]

    bars1 = ax.bar(x - width/2, baseline_probs, width,
                   yerr=baseline_errors, capsize=4,
                   color=baseline_colors, alpha=0.6,
                   label='Baseline', edgecolor='black', linewidth=1,
                   error_kw={'linewidth': 1.5, 'ecolor': 'black'})

    # Plot filtered
    filtered_probs = [r['prob'] for r in filtered_results]
    filtered_errors = [[r['prob'] - r['ci_lower'] for r in filtered_results],
                       [r['ci_upper'] - r['prob'] for r in filtered_results]]

    bars2 = ax.bar(x + width/2, filtered_probs, width,
                   yerr=filtered_errors, capsize=4,
                   color=filtered_colors, alpha=0.9,
                   label=f'{threshold*100:.0f}% consensus', edgecolor='black', linewidth=1,
                   error_kw={'linewidth': 1.5, 'ecolor': 'black'})

    # Add value labels
    for i, (b_val, f_val) in enumerate(zip(baseline_probs, filtered_probs)):
        # Baseline label
        ax.text(i - width/2, b_val + baseline_errors[1][i] + 0.02,
                f'{b_val:.2f}', ha='center', fontsize=8)
        # Filtered label
        ax.text(i + width/2, f_val + filtered_errors[1][i] + 0.02,
                f'{f_val:.2f}', ha='center', fontsize=8, fontweight='bold')

        # Add significance stars
        if baseline_results[i]['significant']:
            ax.text(i - width/2, baseline_results[i]['ci_upper'] + 0.08, '*',
                   ha='center', fontsize=12)
        if filtered_results[i]['significant']:
            ax.text(i + width/2, filtered_results[i]['ci_upper'] + 0.08, '*',
                   ha='center', fontsize=12, fontweight='bold')

    # Reference line
    ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.4, linewidth=1)

    # Labels and formatting
    ax.set_ylabel('P(First metric preferred)', fontsize=11)
    ax.set_title(f'Effect of {threshold*100:.0f}% Consensus Filtering (n={filtered_n}/{baseline_n})',
                fontsize=12, pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(comparisons, fontsize=10)
    ax.set_ylim([0, 0.9])
    ax.set_yticks([0, 0.25, 0.5, 0.75])
    ax.set_yticklabels(['0%', '25%', '50%', '75%'])

    # Simplified legend
    ax.legend(loc='upper left', frameon=True, fancybox=False, edgecolor='black', framealpha=1)

    # Grid
    ax.grid(True, alpha=0.2, axis='y', linestyle=':')
    ax.set_axisbelow(True)

    # Add note about significance
    ax.text(0.99, 0.02, '* p < 0.05', transform=ax.transAxes,
            fontsize=8, ha='right', va='bottom')

    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_filename}")

    return filtered_results, filtered_n, baseline_n

# Create both plots
print("="*60)
print("Creating paper-ready consensus filtering plots")
print("="*60)

# 65% threshold plot
results_65, n_65, n_total = create_consensus_plot(0.65, 'consensus_65_paper.png')

# 75% threshold plot
results_75, n_75, _ = create_consensus_plot(0.75, 'consensus_75_paper.png')

# Print summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"\n65% Consensus Threshold:")
print(f"  - Kept {n_65}/{n_total} responses ({n_65/n_total*100:.1f}%)")
for r in results_65:
    sig = "✓" if r['significant'] else "✗"
    print(f"  - {r['pair']}: {r['prob']:.3f} [{r['ci_lower']:.3f}, {r['ci_upper']:.3f}] {sig}")

print(f"\n75% Consensus Threshold:")
print(f"  - Kept {n_75}/{n_total} responses ({n_75/n_total*100:.1f}%)")
for r in results_75:
    sig = "✓" if r['significant'] else "✗"
    print(f"  - {r['pair']}: {r['prob']:.3f} [{r['ci_lower']:.3f}, {r['ci_upper']:.3f}] {sig}")

print("\nBoth plots saved for paper use.")
print("Recommended: Use 75% threshold (more conservative, less data loss)")