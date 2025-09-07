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
results_df = pd.read_csv('results.csv')

# Extract experience data
experience_data = results_df[['UserID', 'Name', 'How long have you been programming for?']].drop_duplicates()
experience_data.columns = ['UserID', 'Name_Results', 'Programming_Experience']

# Merge with participant data
participant_df = participant_df.merge(experience_data[['UserID', 'Programming_Experience']], 
                                      on='UserID', how='left')

# Convert experience to numeric years
def experience_to_years(exp_str):
    if pd.isna(exp_str):
        return np.nan
    exp_str = str(exp_str).lower()
    if '10+' in exp_str or '10 years' in exp_str:
        return 11  # Use 11 to distinguish from 5-10 range
    elif '5-10' in exp_str or '5 - 10' in exp_str:
        return 7.5
    elif '3-5' in exp_str or '3 - 5' in exp_str:
        return 4
    elif '2-5' in exp_str or '2 - 5' in exp_str:
        return 3.5
    elif '1-3' in exp_str or '1 - 3' in exp_str:
        return 2
    elif 'less than 1' in exp_str or '<1' in exp_str:
        return 0.5
    else:
        # Try to extract number
        import re
        numbers = re.findall(r'\d+', exp_str)
        if numbers:
            return float(numbers[0])
        return np.nan

participant_df['Years_Programming'] = participant_df['Programming_Experience'].apply(experience_to_years)

# Keep only 10+ years experience
EXPERIENCE_CATEGORY = "10+ years"
EXPERIENCE_THRESHOLD_YEARS = 10  # For display purposes

# Identify participants NOT in 10+ category (those with < 11 in our numeric scale)
below_threshold = participant_df[participant_df['Years_Programming'] < 11]
outlier_ids = below_threshold['UserID'].values

print(f"Keeping only participants with {EXPERIENCE_CATEGORY} experience")
print(f"Removing {len(outlier_ids)} participants without 10+ years experience:")

# Get all participants not in 10+ category
all_non_ten_plus = participant_df[participant_df['Programming_Experience'] != '10+ years']
outlier_ids = all_non_ten_plus['UserID'].values

for _, p in all_non_ten_plus.iterrows():
    exp_str = p['Programming_Experience'] if pd.notna(p['Programming_Experience']) else 'Unknown'
    print(f"  - {p['Name']} ({p['UserID']}): {exp_str} (Agreement: {p['Mean_Agreement']:.1%})")

# Create datasets
full_df = merged_df
clean_df = merged_df[~merged_df['UserID'].isin(outlier_ids)]

# Fit models
print("\nFitting Bradley-Terry models...")
full_results, full_wins, full_totals, metrics = fit_bradley_terry_with_ci(full_df)
clean_results, clean_wins, clean_totals, _ = fit_bradley_terry_with_ci(clean_df)

# Create comparison plot with three panels
fig, axes = plt.subplots(1, 3, figsize=(20, 7))

# Setup for all plots
comparisons = [r['pair'] for r in full_results]
x_pos = np.arange(len(comparisons))
width = 0.35

# Panel 1: All Participants
ax1 = axes[0]
full_probs = [r['prob'] for r in full_results]
full_errors = [[r['prob'] - r['ci_lower'] for r in full_results],
               [r['ci_upper'] - r['prob'] for r in full_results]]

colors_full = []
for r in full_results:
    if r['ci_lower'] > 0.5:
        colors_full.append('#2ecc71')
    elif r['ci_upper'] < 0.5:
        colors_full.append('#e74c3c')
    else:
        colors_full.append('#95a5a6')

bars1 = ax1.bar(x_pos, full_probs, width,
                yerr=full_errors, capsize=8,
                color=colors_full, alpha=0.8,
                edgecolor='black', linewidth=2,
                error_kw={'linewidth': 2.5})

for i, r in enumerate(full_results):
    ax1.text(i, r['prob'] + 0.02, f"{r['prob']:.1%}",
             ha='center', fontweight='bold', fontsize=11)
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

for i, pair in enumerate([('logprob', 'mi'), ('tokens', 'mi'), ('logprob', 'tokens')]):
    idx1 = metrics.index(pair[0])
    idx2 = metrics.index(pair[1])
    n = full_totals[idx1][idx2]
    ax1.text(i, 0.32, f'n={int(n)}', ha='center', fontsize=9, style='italic')

# Panel 2: Experienced Participants Only
ax2 = axes[1]
clean_probs = [r['prob'] for r in clean_results]
clean_errors = [[r['prob'] - r['ci_lower'] for r in clean_results],
                [r['ci_upper'] - r['prob'] for r in clean_results]]

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

for i, r in enumerate(clean_results):
    ax2.text(i, r['prob'] + 0.02, f"{r['prob']:.1%}",
             ha='center', fontweight='bold', fontsize=11)
    if r['ci_lower'] > 0.5 or r['ci_upper'] < 0.5:
        ax2.text(i, r['ci_upper'] + 0.05, '*',
                ha='center', fontsize=18, fontweight='bold')
    change = r['prob'] - full_results[i]['prob']
    if abs(change) > 0.01:
        ax2.text(i, r['ci_lower'] - 0.08, f'({change*100:+.1f}pp)',
                ha='center', fontsize=9, style='italic', color='blue')

ax2.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=2)
ax2.set_ylabel('P(First metric preferred)', fontsize=13, fontweight='bold')
ax2.set_title(f'Only {EXPERIENCE_CATEGORY} Experience (n={len(participant_df) - len(outlier_ids)})', 
              fontsize=14, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(comparisons, fontsize=11)
ax2.set_ylim([0.3, 0.85])
ax2.grid(True, alpha=0.3, axis='y')

for i, pair in enumerate([('logprob', 'mi'), ('tokens', 'mi'), ('logprob', 'tokens')]):
    idx1 = metrics.index(pair[0])
    idx2 = metrics.index(pair[1])
    n = clean_totals[idx1][idx2]
    ax2.text(i, 0.32, f'n={int(n)}', ha='center', fontsize=9, style='italic')

# Panel 3: Experience Distribution
ax3 = axes[2]

# Create bins for experience levels matching actual categories
exp_levels = participant_df['Years_Programming'].dropna()
# Adjusted bins to match actual data: 2-5 years (3.5), 5-10 years (7.5), 10+ years (11)
bins = [0, 1, 2.5, 5, 10, 12]
labels = ['<1', '1-2', '2-5', '5-10', '10+']
counts, edges, patches = ax3.hist(exp_levels, bins=bins, alpha=0.7, edgecolor='black')

# Color bars based on 10+ threshold
for i, patch in enumerate(patches):
    if edges[i+1] < 11:  # Less than 11 means not 10+
        patch.set_facecolor('#e74c3c')
        patch.set_alpha(0.7)
    else:
        patch.set_facecolor('#2ecc71')
        patch.set_alpha(0.7)

ax3.axvline(10.5, color='red', linestyle='--', linewidth=2.5,
            label=f'Threshold: {EXPERIENCE_CATEGORY}')
ax3.set_xlabel('Years of Programming Experience', fontsize=12)
ax3.set_ylabel('Number of Participants', fontsize=12)
ax3.set_title('Experience Distribution', fontsize=14, fontweight='bold')
ax3.set_xticks(bins)
ax3.set_xticklabels(['0'] + labels, fontsize=10)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)

# Add annotations
ax3.text(9, max(counts) * 0.9, 
         f'< 10 years', ha='right', fontsize=10, fontweight='bold', color='#e74c3c')
ax3.text(10.7, max(counts) * 0.9, 
         f'10+ years', ha='left', fontsize=10, fontweight='bold', color='#2ecc71')

# Add legend for main plots
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#2ecc71', alpha=0.8, label='First metric significantly preferred'),
    Patch(facecolor='#95a5a6', alpha=0.8, label='No significant difference'),
    Patch(facecolor='#e74c3c', alpha=0.8, label='Second metric significantly preferred'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=3,
           bbox_to_anchor=(0.5, -0.08), framealpha=0.95)

plt.suptitle(f'Impact of Keeping Only {EXPERIENCE_CATEGORY} Programming Experience', 
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('experience_comparison.png', dpi=300, bbox_inches='tight')
print("\nSaved: experience_comparison.png")

# Print detailed statistics
print("\n" + "=" * 80)
print("DETAILED STATISTICS")
print("-" * 80)
print(f"Total participants: {len(participant_df)}")
print(f"Experience filter: {EXPERIENCE_CATEGORY} only")
print(f"Participants removed: {len(outlier_ids)} ({len(outlier_ids)/len(participant_df)*100:.1f}%)")
print(f"Participants retained: {len(participant_df) - len(outlier_ids)} ({(len(participant_df)-len(outlier_ids))/len(participant_df)*100:.1f}%)")

# Show experience breakdown
print("\nExperience Distribution (actual categories from data):")
exp_categories = participant_df['Programming_Experience'].value_counts()
for cat, count in exp_categories.items():
    print(f"  {cat:15}: {count} participants")

print("\n" + "=" * 80)
print("PREFERENCE CHANGES")
print("-" * 80)
print(f"{'Comparison':<20} {'All Data':<25} {'Experienced Only':<25} {'Change'}")
print("-" * 80)

for f, c in zip(full_results, clean_results):
    change = c['prob'] - f['prob']
    f_str = f"{f['prob']:.1%} [{f['ci_lower']:.1%}-{f['ci_upper']:.1%}]"
    c_str = f"{c['prob']:.1%} [{c['ci_lower']:.1%}-{c['ci_upper']:.1%}]"
    print(f"{f['pair']:<20} {f_str:<25} {c_str:<25} {change*100:+.1f}pp")

# Effect size analysis
print("\n" + "=" * 80)
print("EFFECT SIZE ANALYSIS")
print("-" * 80)

for i, (f, c) in enumerate(zip(full_results, clean_results)):
    effect = abs(c['prob'] - f['prob'])
    ci_overlap = not (c['ci_lower'] > f['ci_upper'] or c['ci_upper'] < f['ci_lower'])
    
    print(f"{f['pair']}:")
    print(f"  Effect size: {effect*100:.2f} percentage points")
    print(f"  CI overlap: {'Yes' if ci_overlap else 'No'}")
    print(f"  Direction: {'Strengthened' if abs(c['prob']-0.5) > abs(f['prob']-0.5) else 'Weakened'}")

# Key insights
print("\n" + "=" * 80)
print("KEY INSIGHTS")
print("-" * 80)

# Check if any preferences changed significance
for f, c in zip(full_results, clean_results):
    f_sig = f['ci_lower'] > 0.5 or f['ci_upper'] < 0.5
    c_sig = c['ci_lower'] > 0.5 or c['ci_upper'] < 0.5
    
    if f_sig != c_sig:
        print(f"• {f['pair']}: Changed from {'significant' if f_sig else 'non-significant'} "
              f"to {'significant' if c_sig else 'non-significant'}")
    elif abs(c['prob'] - f['prob']) > 0.05:
        print(f"• {f['pair']}: Large change of {(c['prob']-f['prob'])*100:+.1f}pp")

# Save filtered dataset
clean_df.to_csv('dataset_experience_filtered.csv', index=False)
print(f"\nFiltered dataset saved to: dataset_experience_filtered.csv")

# Save participant data with experience
participant_df.to_csv('participant_experience_analysis.csv', index=False)
print(f"Participant analysis saved to: participant_experience_analysis.csv")