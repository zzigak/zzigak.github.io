import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, approx_fprime
from scipy import stats
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

# Load the relative results
def load_and_compute_results():
    """Load data and compute Bradley-Terry with relative quantities"""
    merged_df = pd.read_csv('intermediate_long_format.csv')
    
    # Get unique metrics
    metrics = ['mi', 'tokens', 'logprob']
    n_metrics = len(metrics)
    metric_to_idx = {m: i for i, m in enumerate(metrics)}
    
    # Build comparison matrix
    wins = np.zeros((n_metrics, n_metrics))
    totals = np.zeros((n_metrics, n_metrics))
    
    for _, row in merged_df.iterrows():
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
    
    # Fit model (same as before)
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
    
    # Compute covariance matrix
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
    est_to_full = {0: 1, 1: 2}  # tokens=1, logprob=2 in full matrix
    
    for i in range(n_est):
        for j in range(n_est):
            full_i = est_to_full[i]
            full_j = est_to_full[j]
            cov_matrix_full[full_i, full_j] = cov_matrix_est[i, j]
    
    log_params_full = np.concatenate([[0], result.x])
    params = np.exp(log_params_full)
    
    return {
        'metrics': metrics,
        'params': params,
        'log_params': log_params_full,
        'cov_matrix': cov_matrix_full,
        'wins': wins,
        'totals': totals
    }

# Create better visualizations
results = load_and_compute_results()

# ============================================================================
# PLOT 1: Single clean figure - Win Probability Matrix
# ============================================================================

fig = plt.figure(figsize=(10, 8))

# Create win probability matrix
metrics = results['metrics']
n_metrics = len(metrics)
win_prob_matrix = np.zeros((n_metrics, n_metrics))
ci_lower_matrix = np.zeros((n_metrics, n_metrics))
ci_upper_matrix = np.zeros((n_metrics, n_metrics))

for i in range(n_metrics):
    for j in range(n_metrics):
        if i == j:
            win_prob_matrix[i, j] = 0.5
            ci_lower_matrix[i, j] = 0.5
            ci_upper_matrix[i, j] = 0.5
        else:
            # Calculate P(i beats j)
            diff = results['log_params'][i] - results['log_params'][j]
            prob = 1 / (1 + np.exp(-diff))
            
            # Calculate CI
            var_diff = (results['cov_matrix'][i, i] + 
                       results['cov_matrix'][j, j] - 
                       2 * results['cov_matrix'][i, j])
            se_diff = np.sqrt(max(0, var_diff))
            
            # CI for probability using delta method
            grad = prob * (1 - prob)
            se_prob = grad * se_diff
            ci_lower = max(0, prob - 1.96 * se_prob)
            ci_upper = min(1, prob + 1.96 * se_prob)
            
            win_prob_matrix[i, j] = prob
            ci_lower_matrix[i, j] = ci_lower
            ci_upper_matrix[i, j] = ci_upper

# Create heatmap
ax = plt.subplot(111)
im = ax.imshow(win_prob_matrix, cmap='RdYlGn', vmin=0, vmax=1, aspect='equal')

# Add text annotations with CIs
for i in range(n_metrics):
    for j in range(n_metrics):
        if i != j:
            prob = win_prob_matrix[i, j]
            ci_lower = ci_lower_matrix[i, j]
            ci_upper = ci_upper_matrix[i, j]
            
            # Determine if significant
            is_sig = (ci_lower > 0.5 or ci_upper < 0.5)
            
            # Format text
            text = f'{prob:.2f}\n[{ci_lower:.2f}-{ci_upper:.2f}]'
            color = 'white' if prob < 0.3 or prob > 0.7 else 'black'
            weight = 'bold' if is_sig else 'normal'
            
            ax.text(j, i, text, ha='center', va='center', 
                   color=color, fontsize=10, fontweight=weight)

# Customize
ax.set_xticks(range(n_metrics))
ax.set_yticks(range(n_metrics))
ax.set_xticklabels([m.upper() for m in metrics])
ax.set_yticklabels([m.upper() for m in metrics])
ax.set_xlabel('Column Metric', fontweight='bold')
ax.set_ylabel('Row Metric', fontweight='bold')
ax.set_title('P(Row beats Column) with 95% CIs\n(Bold = significant difference from 0.5)', 
            fontsize=14, fontweight='bold', pad=20)

# Add colorbar
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Win Probability', rotation=270, labelpad=20)

# Add grid
ax.set_xticks(np.arange(n_metrics) - 0.5, minor=True)
ax.set_yticks(np.arange(n_metrics) - 0.5, minor=True)
ax.grid(which='minor', color='gray', linestyle='-', linewidth=2)

plt.tight_layout()
plt.savefig('bradley_terry_win_matrix.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: bradley_terry_win_matrix.png")

# ============================================================================
# PLOT 2: Simplified bar chart - Focus on comparisons with MI
# ============================================================================

fig, ax = plt.subplots(1, 1, figsize=(10, 6))

# Extract MI comparisons
mi_idx = metrics.index('mi')
comparisons = []
for i, metric in enumerate(metrics):
    if i != mi_idx:
        # P(metric beats MI)
        diff = results['log_params'][i] - results['log_params'][mi_idx]
        prob = 1 / (1 + np.exp(-diff))
        
        # CI calculation
        var_diff = results['cov_matrix'][i, i]  # Cov with MI is 0
        se_diff = np.sqrt(var_diff)
        
        # Delta method for probability CI
        grad = prob * (1 - prob)
        se_prob = grad * se_diff
        ci_lower = max(0, prob - 1.96 * se_prob)
        ci_upper = min(1, prob + 1.96 * se_prob)
        
        # Also get observed proportion
        observed_wins = results['wins'][i][mi_idx]
        observed_total = results['totals'][i][mi_idx]
        observed_prop = observed_wins / observed_total if observed_total > 0 else 0.5
        
        comparisons.append({
            'metric': metric.upper(),
            'prob': prob,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'observed': observed_prop,
            'significant': ci_lower > 0.5
        })

# Plot
x_pos = np.arange(len(comparisons))
colors = ['#2ecc71' if c['significant'] else '#95a5a6' for c in comparisons]

# Bradley-Terry estimates
bars = ax.bar(x_pos - 0.2, [c['prob'] for c in comparisons], 0.35,
              yerr=[[c['prob'] - c['ci_lower'] for c in comparisons],
                    [c['ci_upper'] - c['prob'] for c in comparisons]],
              capsize=6, color=colors, alpha=0.8,
              label='Bradley-Terry Estimate', edgecolor='black', linewidth=1.5,
              error_kw={'linewidth': 2})

# Observed proportions
ax.bar(x_pos + 0.2, [c['observed'] for c in comparisons], 0.35,
       color='lightblue', alpha=0.8, label='Observed Proportion',
       edgecolor='black', linewidth=1.5)

# Add percentage labels
for i, comp in enumerate(comparisons):
    ax.text(i - 0.2, comp['prob'] + 0.03, f"{comp['prob']:.1%}",
            ha='center', fontweight='bold')
    ax.text(i + 0.2, comp['observed'] + 0.03, f"{comp['observed']:.1%}",
            ha='center', fontweight='bold')

# Reference line at 50%
ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=2,
           label='No preference (50%)')

# Customize
ax.set_ylabel('P(Metric beats MI)', fontsize=13, fontweight='bold')
ax.set_title('Preference for Metrics over Mutual Information (MI)\n' + 
             'Green = significantly better than MI (p < 0.05)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x_pos)
ax.set_xticklabels([c['metric'] for c in comparisons], fontsize=12)
ax.set_ylim([0, 1])
ax.legend(loc='upper left', framealpha=0.95)
ax.grid(True, alpha=0.3, axis='y')

# Add interpretation text
interpretation = ("Both metrics significantly outperform MI\n" if all(c['significant'] for c in comparisons) else
                 "Log-probability significantly outperforms MI\n" if comparisons[1]['significant'] else
                 "Tokens significantly outperforms MI\n" if comparisons[0]['significant'] else
                 "No significant improvement over MI")

ax.text(0.98, 0.02, interpretation, transform=ax.transAxes,
        ha='right', va='bottom', fontsize=11, style='italic',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8))

plt.tight_layout()
plt.savefig('bradley_terry_vs_mi.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: bradley_terry_vs_mi.png")

# ============================================================================
# PLOT 3: Summary figure for paper - most important results only
# ============================================================================

fig, ax = plt.subplots(1, 1, figsize=(8, 6))

# Prepare data for all three pairwise comparisons
all_comparisons = []
comparison_pairs = [('logprob', 'mi'), ('tokens', 'mi'), ('logprob', 'tokens')]

for m1, m2 in comparison_pairs:
    i = metrics.index(m1)
    j = metrics.index(m2)
    
    # Bradley-Terry probability
    diff = results['log_params'][i] - results['log_params'][j]
    prob = 1 / (1 + np.exp(-diff))
    
    # CI
    var_diff = (results['cov_matrix'][i, i] + 
                results['cov_matrix'][j, j] - 
                2 * results['cov_matrix'][i, j])
    se_diff = np.sqrt(max(0, var_diff))
    grad = prob * (1 - prob)
    se_prob = grad * se_diff
    ci_lower = max(0, prob - 1.96 * se_prob)
    ci_upper = min(1, prob + 1.96 * se_prob)
    
    # Observed
    obs_wins = results['wins'][i][j]
    obs_total = results['totals'][i][j]
    obs_prop = obs_wins / obs_total if obs_total > 0 else 0.5
    
    all_comparisons.append({
        'pair': f'{m1.upper()} vs {m2.upper()}',
        'prob': prob,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'observed': obs_prop,
        'significant': ci_lower > 0.5 or ci_upper < 0.5,
        'favors': m1.upper() if prob > 0.5 else m2.upper()
    })

# Create grouped bar chart
x = np.arange(len(all_comparisons))
width = 0.35

# Determine colors based on which metric is favored
bar_colors = []
for comp in all_comparisons:
    if comp['significant']:
        if 'LOGPROB' in comp['favors']:
            bar_colors.append('#2ecc71')  # Green for logprob
        elif 'TOKENS' in comp['favors']:
            bar_colors.append('#3498db')  # Blue for tokens
        else:
            bar_colors.append('#e74c3c')  # Red for MI
    else:
        bar_colors.append('#95a5a6')  # Gray for non-significant

# Plot bars
bars = ax.bar(x, [c['prob'] for c in all_comparisons], width,
              yerr=[[c['prob'] - c['ci_lower'] for c in all_comparisons],
                    [c['ci_upper'] - c['prob'] for c in all_comparisons]],
              capsize=8, color=bar_colors, alpha=0.8,
              edgecolor='black', linewidth=2,
              error_kw={'linewidth': 2.5, 'ecolor': 'black'})

# Add value labels
for i, comp in enumerate(all_comparisons):
    # Probability label
    ax.text(i, comp['prob'] + 0.02, f"{comp['prob']:.1%}",
            ha='center', fontweight='bold', fontsize=11)
    
    # Significance marker
    if comp['significant']:
        ax.text(i, comp['ci_upper'] + 0.05, '*', 
                ha='center', fontsize=20, fontweight='bold')

# Reference line
ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=2)
ax.text(len(all_comparisons) - 0.5, 0.51, 'No preference', 
        fontsize=10, color='red', style='italic')

# Labels and title
ax.set_ylabel('P(First metric preferred)', fontsize=13, fontweight='bold')
ax.set_title('Bradley-Terry Model: Pairwise Metric Preferences', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([c['pair'] for c in all_comparisons], fontsize=11)
ax.set_ylim([0, 0.85])
ax.grid(True, alpha=0.3, axis='y')

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#2ecc71', alpha=0.8, label='Logprob favored'),
    Patch(facecolor='#3498db', alpha=0.8, label='Tokens favored'),
    Patch(facecolor='#95a5a6', alpha=0.8, label='No significant difference'),
]
ax.legend(handles=legend_elements, loc='upper right', framealpha=0.95)

# Add note
ax.text(0.02, 0.98, 'Error bars: 95% CI\n* p < 0.05', 
        transform=ax.transAxes, fontsize=9, style='italic',
        va='top', ha='left')

plt.tight_layout()
plt.savefig('bradley_terry_summary.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: bradley_terry_summary.png")

print("\n" + "=" * 60)
print("Created three improved visualizations:")
print("-" * 60)
print("1. bradley_terry_win_matrix.png - Full win probability matrix")
print("   Shows P(row beats column) for all pairs with CIs")
print("\n2. bradley_terry_vs_mi.png - Focus on MI comparisons")
print("   Compares other metrics against the baseline (MI)")
print("\n3. bradley_terry_summary.png - Clean summary for paper")
print("   Shows all three key comparisons with significance")
print("\nThese plots are much clearer and more interpretable!")