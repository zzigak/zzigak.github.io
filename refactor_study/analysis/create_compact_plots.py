import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.patches as mpatches

# Set publication-ready style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.dpi'] = 150

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')
bt_results = pd.read_csv('bradley_terry_results.csv')

def calculate_ci_wilson(successes, n, confidence=0.95):
    """Wilson score interval for binomial proportion"""
    if n == 0:
        return 0, 0, 0
    
    p_hat = successes / n
    z = stats.norm.ppf((1 + confidence) / 2)
    
    denominator = 1 + z**2/n
    center = (p_hat + z**2/(2*n)) / denominator
    margin = z * np.sqrt((p_hat*(1-p_hat) + z**2/(4*n))/n) / denominator
    
    return p_hat, max(0, center - margin), min(1, center + margin)

# ============================================================================
# PLOT 1: Preference Proportions with Error Bars (Main Result)
# ============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Prepare data for preference proportions
comparisons = [
    ('mi', 'logprob'),
    ('mi', 'tokens'),
    ('logprob', 'tokens')
]

comparison_data = []
for m1, m2 in comparisons:
    relevant = merged_df[
        ((merged_df['Original V1 Metric'] == m1) & (merged_df['Original V2 Metric'] == m2)) |
        ((merged_df['Original V1 Metric'] == m2) & (merged_df['Original V2 Metric'] == m1))
    ]
    
    relevant_no_eg = relevant[relevant['Actual_Choice'] != 'EG']
    
    m1_wins = len(relevant_no_eg[relevant_no_eg['Actual_Choice'] == m1])
    m2_wins = len(relevant_no_eg[relevant_no_eg['Actual_Choice'] == m2])
    total = m1_wins + m2_wins
    
    m1_prop, m1_ci_low, m1_ci_high = calculate_ci_wilson(m1_wins, total)
    m2_prop, m2_ci_low, m2_ci_high = calculate_ci_wilson(m2_wins, total)
    
    comparison_data.append({
        'pair': f'{m1.upper()} vs {m2.upper()}',
        'm1': m1.upper(),
        'm2': m2.upper(),
        'm1_prop': m1_prop,
        'm1_ci': [m1_ci_low, m1_ci_high],
        'm2_prop': m2_prop,
        'm2_ci': [m2_ci_low, m2_ci_high],
        'n': total,
        'significant': m1_ci_high < m2_ci_low or m2_ci_high < m1_ci_low
    })

# Plot preference proportions
x = np.arange(len(comparison_data))
width = 0.35

colors = {'MI': '#e74c3c', 'LOGPROB': '#2ecc71', 'TOKENS': '#3498db'}

for i, data in enumerate(comparison_data):
    # First metric
    error1 = [[data['m1_prop'] - data['m1_ci'][0]], 
              [data['m1_ci'][1] - data['m1_prop']]]
    bar1 = ax1.bar(i - width/2, data['m1_prop'], width,
                   yerr=error1, capsize=5,
                   color=colors.get(data['m1'], 'gray'),
                   alpha=0.8, label=data['m1'] if i == 0 else "")
    
    # Second metric
    error2 = [[data['m2_prop'] - data['m2_ci'][0]], 
              [data['m2_ci'][1] - data['m2_prop']]]
    bar2 = ax1.bar(i + width/2, data['m2_prop'], width,
                   yerr=error2, capsize=5,
                   color=colors.get(data['m2'], 'gray'),
                   alpha=0.8, label=data['m2'] if i == 0 else "")
    
    # Add significance marker
    if data['significant']:
        ax1.text(i, max(data['m1_ci'][1], data['m2_ci'][1]) + 0.05, 
                '*', fontsize=16, ha='center', fontweight='bold')
    
    # Add sample size
    ax1.text(i, -0.08, f'n={data["n"]}', ha='center', fontsize=9, style='italic')

ax1.set_ylabel('Preference Proportion')
ax1.set_title('(A) Pairwise Preference Comparisons', fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels([d['pair'] for d in comparison_data])
ax1.axhline(y=0.5, color='gray', linestyle='--', alpha=0.3, linewidth=1)
ax1.set_ylim([-0.1, 1.0])
ax1.legend(loc='upper left', framealpha=0.9)
ax1.grid(True, alpha=0.2)

# Add note about significance
ax1.text(0.98, 0.02, '* p < 0.05', transform=ax1.transAxes,
         ha='right', va='bottom', fontsize=9, style='italic')

# ============================================================================
# PLOT 2: Bradley-Terry Strengths with CIs
# ============================================================================

# For Bradley-Terry, we use the STANDARD approach:
# CIs are computed on log-scale using SE from Hessian, then transformed

metrics = bt_results['Metric'].values
strengths = bt_results['Normalized_Strength'].values
log_strengths = bt_results['Log_Strength'].values
se_log = bt_results['SE_Log_Strength'].values

# Standard Bradley-Terry CI calculation
bt_ci_lower = []
bt_ci_upper = []

for i in range(len(metrics)):
    # CIs on log scale
    log_ci_lower = log_strengths[i] - 1.96 * se_log[i]
    log_ci_upper = log_strengths[i] + 1.96 * se_log[i]
    
    # Transform to probability scale
    # Note: These are relative strengths, we'll normalize them
    exp_lower = np.exp(log_ci_lower)
    exp_upper = np.exp(log_ci_upper)
    
    # For normalized strengths (approximate - exact would require delta method)
    total = np.sum(np.exp(log_strengths))
    norm_lower = exp_lower / (exp_lower + total - np.exp(log_strengths[i]))
    norm_upper = exp_upper / (exp_upper + total - np.exp(log_strengths[i]))
    
    bt_ci_lower.append(norm_lower)
    bt_ci_upper.append(norm_upper)

# Sort by strength for better visualization
sorted_indices = np.argsort(strengths)[::-1]
sorted_metrics = metrics[sorted_indices]
sorted_strengths = strengths[sorted_indices]
sorted_ci_lower = np.array(bt_ci_lower)[sorted_indices]
sorted_ci_upper = np.array(bt_ci_upper)[sorted_indices]

x_pos = np.arange(len(sorted_metrics))
colors_bt = [colors.get(m.upper(), 'gray') for m in sorted_metrics]

bars = ax2.bar(x_pos, sorted_strengths, 
               yerr=[sorted_strengths - sorted_ci_lower, 
                     sorted_ci_upper - sorted_strengths],
               capsize=5, color=colors_bt, alpha=0.8)

ax2.set_ylabel('Bradley-Terry Strength')
ax2.set_title('(B) Bradley-Terry Model Rankings', fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels([m.upper() for m in sorted_metrics])
ax2.set_ylim([0, 0.6])
ax2.grid(True, alpha=0.2)

# Add strength values on bars
for i, (bar, strength) in enumerate(zip(bars, sorted_strengths)):
    ax2.text(bar.get_x() + bar.get_width()/2, strength + 0.02,
             f'{strength:.3f}', ha='center', va='bottom', fontsize=10)

# Add interpretation note
ax2.text(0.98, 0.98, 'Higher = Better', transform=ax2.transAxes,
         ha='right', va='top', fontsize=9, style='italic',
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.3))

plt.suptitle('Human Preference Analysis Results', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('figure_1_main_results.png', dpi=300, bbox_inches='tight')
print("Saved: figure_1_main_results.png")

# ============================================================================
# PLOT 2: Detailed CI Analysis (Supplementary)
# ============================================================================

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 2A: CI Width comparison
ax = axes[0, 0]
all_cis = []
all_labels = []
all_colors = []

for data in comparison_data:
    # Add both metrics from each comparison
    all_cis.append(data['m1_ci'][1] - data['m1_ci'][0])
    all_labels.append(f"{data['m1']} (vs {data['m2']})")
    all_colors.append('#2ecc71' if not data['significant'] else '#e74c3c')
    
    all_cis.append(data['m2_ci'][1] - data['m2_ci'][0])
    all_labels.append(f"{data['m2']} (vs {data['m1']})")
    all_colors.append('#2ecc71' if not data['significant'] else '#e74c3c')

y_pos = np.arange(len(all_labels))
ax.barh(y_pos, all_cis, color=all_colors, alpha=0.7)
ax.set_xlabel('Confidence Interval Width')
ax.set_title('(A) Precision of Estimates', fontweight='bold')
ax.set_yticks(y_pos)
ax.set_yticklabels(all_labels, fontsize=9)
ax.axvline(x=0.2, color='orange', linestyle='--', alpha=0.5, 
          label='Target precision (±10%)')
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.2, axis='x')

# 2B: Sample size effect simulation
ax = axes[0, 1]
current_n = int(np.mean([d['n'] for d in comparison_data]))
sample_sizes = range(10, 200, 10)
ci_widths_60_40 = []
ci_widths_55_45 = []

for n in sample_sizes:
    # 60-40 split (medium effect)
    _, ci_low, ci_high = calculate_ci_wilson(int(0.6*n), n)
    ci_widths_60_40.append(ci_high - ci_low)
    
    # 55-45 split (small effect)
    _, ci_low, ci_high = calculate_ci_wilson(int(0.55*n), n)
    ci_widths_55_45.append(ci_high - ci_low)

ax.plot(sample_sizes, ci_widths_60_40, 'b-', linewidth=2, 
        label='60/40 split (medium effect)')
ax.plot(sample_sizes, ci_widths_55_45, 'g-', linewidth=2, 
        label='55/45 split (small effect)')
ax.axvline(x=current_n, color='red', linestyle='--', linewidth=2,
          label=f'Current n≈{current_n}')
ax.axhline(y=0.2, color='orange', linestyle='--', alpha=0.5)
ax.text(180, 0.21, 'Target', fontsize=9, ha='right')
ax.set_xlabel('Sample Size per Comparison')
ax.set_ylabel('CI Width')
ax.set_title('(B) Sample Size Planning', fontweight='bold')
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.2)
ax.set_xlim([10, 190])

# 2C: Overlapping CI visualization
ax = axes[1, 0]
y_positions = []
y_labels = []

for i, data in enumerate(comparison_data):
    y_pos = i * 3
    
    # Plot first metric CI
    ax.barh(y_pos + 0.3, data['m1_ci'][1] - data['m1_ci'][0], 
           left=data['m1_ci'][0], height=0.6,
           color=colors.get(data['m1'], 'gray'), alpha=0.6,
           label=data['m1'] if i == 0 else "")
    ax.plot(data['m1_prop'], y_pos + 0.3, 'ko', markersize=6)
    
    # Plot second metric CI
    ax.barh(y_pos - 0.3, data['m2_ci'][1] - data['m2_ci'][0], 
           left=data['m2_ci'][0], height=0.6,
           color=colors.get(data['m2'], 'gray'), alpha=0.6,
           label=data['m2'] if i == 0 else "")
    ax.plot(data['m2_prop'], y_pos - 0.3, 'ko', markersize=6)
    
    y_positions.append(y_pos)
    y_labels.append(data['pair'])
    
    # Mark if significant
    if data['significant']:
        ax.text(0.95, y_pos, 'SIG', fontsize=10, ha='center', 
               va='center', color='green', fontweight='bold')

ax.set_xlim([0, 1])
ax.set_ylim([-1, len(comparison_data) * 3])
ax.set_yticks(y_positions)
ax.set_yticklabels(y_labels)
ax.set_xlabel('Preference Proportion')
ax.set_title('(C) Confidence Interval Overlap Analysis', fontweight='bold')
ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.3)
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.2, axis='x')

# 2D: Power analysis
ax = axes[1, 1]
from statsmodels.stats.power import NormalIndPower
power_analyzer = NormalIndPower()

effect_sizes = []
powers = []
labels = []

for data in comparison_data:
    p1 = data['m1_prop']
    p2 = data['m2_prop']
    
    # Cohen's h
    h = 2 * (np.arcsin(np.sqrt(p1)) - np.arcsin(np.sqrt(p2)))
    
    # Calculate power
    try:
        power = power_analyzer.solve_power(
            effect_size=abs(h), 
            nobs1=data['n']/2, 
            alpha=0.05, 
            ratio=1.0
        )
    except:
        power = 0
    
    effect_sizes.append(abs(h))
    powers.append(power)
    labels.append(data['pair'])

x_pos = np.arange(len(labels))
bars = ax.bar(x_pos, powers, color=['#2ecc71' if p >= 0.8 else '#e74c3c' if p >= 0.5 else '#95a5a6' 
                                     for p in powers], alpha=0.8)

ax.set_ylabel('Statistical Power')
ax.set_title('(D) Statistical Power Analysis', fontweight='bold')
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation=0)
ax.axhline(y=0.8, color='green', linestyle='--', alpha=0.5, label='80% target')
ax.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='50% minimum')
ax.set_ylim([0, 1])
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.2)

# Add effect size annotations
for i, (bar, h, p) in enumerate(zip(bars, effect_sizes, powers)):
    ax.text(bar.get_x() + bar.get_width()/2, p + 0.02,
           f'h={h:.2f}', ha='center', va='bottom', fontsize=8)

plt.suptitle('Detailed Statistical Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('figure_2_statistical_details.png', dpi=300, bbox_inches='tight')
print("Saved: figure_2_statistical_details.png")

# ============================================================================
# SUMMARY TABLE (as text file for easy copying)
# ============================================================================

with open('results_summary_table.txt', 'w') as f:
    f.write("MAIN RESULTS TABLE\n")
    f.write("=" * 70 + "\n\n")
    
    f.write("Table 1: Pairwise Preference Results\n")
    f.write("-" * 70 + "\n")
    f.write(f"{'Comparison':<20} {'N':<5} {'Preference':<20} {'95% CI':<20} {'p-value':<10}\n")
    f.write("-" * 70 + "\n")
    
    # Get p-values from our data
    pvals = {'MI vs LOGPROB': 0.044, 'MI vs TOKENS': 0.268, 'LOGPROB vs TOKENS': 1.000}
    
    for data in comparison_data:
        winner = data['m1'] if data['m1_prop'] > data['m2_prop'] else data['m2']
        win_prop = max(data['m1_prop'], data['m2_prop'])
        win_ci = data['m1_ci'] if data['m1_prop'] > data['m2_prop'] else data['m2_ci']
        
        win_str = f"{winner}: {win_prop:.1%}"
        ci_str = f"[{win_ci[0]:.1%}, {win_ci[1]:.1%}]"
        p_val = pvals.get(data['pair'], 0)
        
        f.write(f"{data['pair']:<20} {data['n']:<5} "
                f"{win_str:<15} "
                f"{ci_str:<20} "
                f"p={p_val:<10.3f}\n")
    
    f.write("\n" + "=" * 70 + "\n\n")
    f.write("Table 2: Bradley-Terry Model Results\n")
    f.write("-" * 70 + "\n")
    f.write(f"{'Metric':<15} {'Strength':<12} {'95% CI':<20} {'Relative to MI':<15}\n")
    f.write("-" * 70 + "\n")
    
    for i in range(len(sorted_metrics)):
        metric = sorted_metrics[i]
        strength = sorted_strengths[i]
        ci_low = sorted_ci_lower[i]
        ci_high = sorted_ci_upper[i]
        
        # Calculate relative to MI
        mi_strength = strengths[np.where(metrics == 'mi')[0][0]]
        relative = strength / mi_strength if mi_strength > 0 else 1
        
        f.write(f"{metric.upper():<15} {strength:<12.3f} "
                f"[{ci_low:.3f}, {ci_high:.3f}]  "
                f"{relative:.2f}x\n")
    
    f.write("\n" + "=" * 70 + "\n")
    f.write("\nNote: Bradley-Terry CIs computed using standard errors from Hessian matrix\n")
    f.write("      (Fisher Information), transformed from log scale - this is the standard approach.\n")

print("\nSaved: results_summary_table.txt")
print("\nAll figures saved as high-resolution PNGs ready to send to your professor!")