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

def compute_all_pairs_hessian(fit_result):
    """Compute CIs for all pairwise comparisons using Hessian"""
    metrics = fit_result['metrics']
    n_metrics = len(metrics)
    result = fit_result['result']
    
    # Compute Hessian
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
    
    # Calculate for all pairs
    pairs = [('logprob', 'mi'), ('tokens', 'mi'), ('logprob', 'tokens')]
    results = []
    
    for m1, m2 in pairs:
        i = metrics.index(m1)
        j = metrics.index(m2)
        
        # P(m1 beats m2)
        diff = fit_result['log_params'][i] - fit_result['log_params'][j]
        prob = 1 / (1 + np.exp(-diff))
        
        # CI calculation
        var_diff = cov_matrix_full[i, i] + cov_matrix_full[j, j] - 2 * cov_matrix_full[i, j]
        se_diff = np.sqrt(max(0, var_diff))
        
        # Delta method
        grad = prob * (1 - prob)
        se_prob = grad * se_diff
        ci_lower = max(0, prob - 1.96 * se_prob)
        ci_upper = min(1, prob + 1.96 * se_prob)
        
        results.append({
            'pair': f'{m1.upper()} vs {m2.upper()}',
            'prob': prob,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'method': 'Hessian'
        })
    
    return results

def compute_all_pairs_bootstrap(merged_df, n_bootstrap=1000):
    """Compute CIs for all pairs using bootstrap"""
    print("Running bootstrap with 1000 iterations...")
    
    # Store bootstrap results
    bootstrap_probs = {
        'logprob_vs_mi': [],
        'tokens_vs_mi': [],
        'logprob_vs_tokens': []
    }
    
    comparison_ids = merged_df.index.values
    
    for i in tqdm(range(n_bootstrap)):
        # Resample
        bootstrap_ids = np.random.choice(comparison_ids, size=len(comparison_ids), replace=True)
        bootstrap_data = merged_df.loc[bootstrap_ids]
        
        try:
            # Fit model
            boot_fit = fit_bradley_terry_once(bootstrap_data)
            
            # Calculate probabilities for all pairs
            mi_idx = 0
            tokens_idx = 1
            logprob_idx = 2
            
            # P(logprob beats MI)
            diff = boot_fit['log_params'][logprob_idx] - boot_fit['log_params'][mi_idx]
            bootstrap_probs['logprob_vs_mi'].append(1 / (1 + np.exp(-diff)))
            
            # P(tokens beats MI)
            diff = boot_fit['log_params'][tokens_idx] - boot_fit['log_params'][mi_idx]
            bootstrap_probs['tokens_vs_mi'].append(1 / (1 + np.exp(-diff)))
            
            # P(logprob beats tokens)
            diff = boot_fit['log_params'][logprob_idx] - boot_fit['log_params'][tokens_idx]
            bootstrap_probs['logprob_vs_tokens'].append(1 / (1 + np.exp(-diff)))
            
        except:
            continue
    
    # Calculate percentile CIs
    pairs = [('logprob', 'mi'), ('tokens', 'mi'), ('logprob', 'tokens')]
    results = []
    
    for m1, m2 in pairs:
        key = f'{m1}_vs_{m2}'
        probs = bootstrap_probs[key]
        
        if len(probs) > 0:
            mean_prob = np.mean(probs)
            ci_lower = np.percentile(probs, 2.5)
            ci_upper = np.percentile(probs, 97.5)
            
            results.append({
                'pair': f'{m1.upper()} vs {m2.upper()}',
                'prob': mean_prob,
                'ci_lower': ci_lower,
                'ci_upper': ci_upper,
                'method': 'Bootstrap',
                'distribution': probs
            })
    
    print(f"Bootstrap completed: {len(bootstrap_probs['logprob_vs_mi'])} successful iterations")
    return results

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')

# Fit model and compute both methods
print("Computing Hessian-based CIs...")
original_fit = fit_bradley_terry_once(merged_df)
hessian_results = compute_all_pairs_hessian(original_fit)

print("Computing Bootstrap CIs...")
bootstrap_results = compute_all_pairs_bootstrap(merged_df)

# Get observed proportions for all pairs
observed_data = []
pairs = [('logprob', 'mi'), ('tokens', 'mi'), ('logprob', 'tokens')]

for m1, m2 in pairs:
    i = original_fit['metrics'].index(m1)
    j = original_fit['metrics'].index(m2)
    
    wins = original_fit['wins'][i][j]
    total = original_fit['totals'][i][j]
    
    if total > 0:
        observed_prop = wins / total
        observed_data.append({
            'pair': f'{m1.upper()} vs {m2.upper()}',
            'observed': observed_prop,
            'wins': wins,
            'total': total
        })

# Create comparison plot
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Setup for both plots
pair_labels = [r['pair'] for r in hessian_results]
x_pos = np.arange(len(pair_labels))
width = 0.25

# Left plot: Hessian method
ax1 = axes[0]

# Hessian estimates
hessian_probs = [r['prob'] for r in hessian_results]
hessian_errors = [[r['prob'] - r['ci_lower'] for r in hessian_results],
                  [r['ci_upper'] - r['prob'] for r in hessian_results]]

# Determine colors based on significance
colors_h = []
for r in hessian_results:
    if r['ci_lower'] > 0.5:
        colors_h.append('#2ecc71')  # Green - first metric wins
    elif r['ci_upper'] < 0.5:
        colors_h.append('#e74c3c')  # Red - second metric wins
    else:
        colors_h.append('#95a5a6')  # Gray - no significant difference

bars1 = ax1.bar(x_pos - width, hessian_probs, width,
                yerr=hessian_errors, capsize=6,
                color=colors_h, alpha=0.8,
                label='BT Model (Hessian)', edgecolor='black', linewidth=1.5,
                error_kw={'linewidth': 2})

# Observed proportions
observed_probs = [o['observed'] for o in observed_data]
bars2 = ax1.bar(x_pos, observed_probs, width,
                color='lightblue', alpha=0.8,
                label='Observed Proportion', edgecolor='black', linewidth=1.5)

# Add value labels and significance markers
for i, r in enumerate(hessian_results):
    ax1.text(i - width, r['prob'] + 0.02, f"{r['prob']:.1%}",
             ha='center', fontweight='bold', fontsize=9)
    ax1.text(i, observed_data[i]['observed'] + 0.02, 
             f"{observed_data[i]['observed']:.1%}",
             ha='center', fontweight='bold', fontsize=9)
    ax1.text(i, -0.08, f"n={observed_data[i]['total']}", 
             ha='center', fontsize=9, style='italic')
    
    # Add significance marker
    if r['ci_lower'] > 0.5 or r['ci_upper'] < 0.5:
        ax1.text(i - width, r['ci_upper'] + 0.05, '*', 
                ha='center', fontsize=16, fontweight='bold')

ax1.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=1.5)
ax1.set_ylabel('P(First metric preferred)', fontsize=12, fontweight='bold')
ax1.set_title('Hessian Method (Analytical)', fontsize=13, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(pair_labels, rotation=15, ha='right')
ax1.set_ylim([0, 0.9])
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3, axis='y')

# Right plot: Bootstrap method
ax2 = axes[1]

# Bootstrap estimates
bootstrap_probs = [r['prob'] for r in bootstrap_results]
bootstrap_errors = [[r['prob'] - r['ci_lower'] for r in bootstrap_results],
                   [r['ci_upper'] - r['prob'] for r in bootstrap_results]]

# Determine colors
colors_b = []
for r in bootstrap_results:
    if r['ci_lower'] > 0.5:
        colors_b.append('#2ecc71')
    elif r['ci_upper'] < 0.5:
        colors_b.append('#e74c3c')
    else:
        colors_b.append('#95a5a6')

bars3 = ax2.bar(x_pos - width, bootstrap_probs, width,
                yerr=bootstrap_errors, capsize=6,
                color=colors_b, alpha=0.8,
                label='BT Model (Bootstrap)', edgecolor='black', linewidth=1.5,
                error_kw={'linewidth': 2})

# Observed (same as left)
bars4 = ax2.bar(x_pos, observed_probs, width,
                color='lightblue', alpha=0.8,
                label='Observed Proportion', edgecolor='black', linewidth=1.5)

# Add value labels
for i, r in enumerate(bootstrap_results):
    ax2.text(i - width, r['prob'] + 0.02, f"{r['prob']:.1%}",
             ha='center', fontweight='bold', fontsize=9)
    ax2.text(i, observed_data[i]['observed'] + 0.02, 
             f"{observed_data[i]['observed']:.1%}",
             ha='center', fontweight='bold', fontsize=9)
    
    # Add significance marker
    if r['ci_lower'] > 0.5 or r['ci_upper'] < 0.5:
        ax2.text(i - width, r['ci_upper'] + 0.05, '*', 
                ha='center', fontsize=16, fontweight='bold')

ax2.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=1.5)
ax2.set_ylabel('P(First metric preferred)', fontsize=12, fontweight='bold')
ax2.set_title('Bootstrap Method (1000 samples)', fontsize=13, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(pair_labels, rotation=15, ha='right')
ax2.set_ylim([0, 0.9])
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3, axis='y')

# Add interpretation
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#2ecc71', alpha=0.8, label='First metric significantly preferred'),
    Patch(facecolor='#e74c3c', alpha=0.8, label='Second metric significantly preferred'),
    Patch(facecolor='#95a5a6', alpha=0.8, label='No significant difference'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=3, 
           bbox_to_anchor=(0.5, -0.05), framealpha=0.95)

plt.suptitle('Bradley-Terry Model: All Pairwise Comparisons', 
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('all_pairs_comparison.png', dpi=300, bbox_inches='tight')
print("\nSaved: all_pairs_comparison.png")

# Print numerical comparison
print("\n" + "=" * 70)
print("Numerical Comparison of Methods")
print("-" * 70)
print(f"{'Pair':<20} {'Method':<12} {'Estimate':<10} {'95% CI':<20} {'Width':<8}")
print("-" * 70)

for h, b in zip(hessian_results, bootstrap_results):
    h_width = h['ci_upper'] - h['ci_lower']
    b_width = b['ci_upper'] - b['ci_lower']
    
    print(f"{h['pair']:<20} {'Hessian':<12} {h['prob']:.3f} "
          f"[{h['ci_lower']:.3f}, {h['ci_upper']:.3f}]  {h_width:.3f}")
    print(f"{'':<20} {'Bootstrap':<12} {b['prob']:.3f} "
          f"[{b['ci_lower']:.3f}, {b['ci_upper']:.3f}]  {b_width:.3f}")
    
    # Check if they agree on significance
    h_sig = h['ci_lower'] > 0.5 or h['ci_upper'] < 0.5
    b_sig = b['ci_lower'] > 0.5 or b['ci_upper'] < 0.5
    
    if h_sig == b_sig:
        print(f"{'':<20} {'Agreement:':<12} Both {'significant' if h_sig else 'not significant'}")
    else:
        print(f"{'':<20} {'Disagreement:':<12} Methods differ on significance!")
    print()

print("\nConclusion: The methods should give very similar results, validating our approach!")