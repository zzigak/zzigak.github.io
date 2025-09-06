import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Set publication-ready style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['figure.dpi'] = 150

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')

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

# Create single figure for preference proportions
fig, ax = plt.subplots(1, 1, figsize=(10, 6))

# Prepare data
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

# Define colors for each metric
colors = {'MI': '#e74c3c', 'LOGPROB': '#2ecc71', 'TOKENS': '#3498db'}

# Set up x positions
x = np.arange(len(comparison_data))
width = 0.35

# Plot bars with error bars
for i, data in enumerate(comparison_data):
    # First metric
    error1 = [[data['m1_prop'] - data['m1_ci'][0]], 
              [data['m1_ci'][1] - data['m1_prop']]]
    bar1 = ax.bar(i - width/2, data['m1_prop'], width,
                   yerr=error1, capsize=6,
                   color=colors.get(data['m1'], 'gray'),
                   alpha=0.8, edgecolor='black', linewidth=1.5,
                   label=data['m1'] if i == 0 else "",
                   error_kw={'linewidth': 2, 'ecolor': 'black'})
    
    # Second metric
    error2 = [[data['m2_prop'] - data['m2_ci'][0]], 
              [data['m2_ci'][1] - data['m2_prop']]]
    bar2 = ax.bar(i + width/2, data['m2_prop'], width,
                   yerr=error2, capsize=6,
                   color=colors.get(data['m2'], 'gray'),
                   alpha=0.8, edgecolor='black', linewidth=1.5,
                   label=data['m2'] if i == 0 else "",
                   error_kw={'linewidth': 2, 'ecolor': 'black'})
    
    # Add percentage labels on bars
    ax.text(i - width/2, data['m1_prop'] + 0.02, f"{data['m1_prop']:.1%}",
            ha='center', va='bottom', fontweight='bold', fontsize=10)
    ax.text(i + width/2, data['m2_prop'] + 0.02, f"{data['m2_prop']:.1%}",
            ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Add significance marker
    if data['significant']:
        y_max = max(data['m1_ci'][1], data['m2_ci'][1])
        ax.plot([i - width/2, i + width/2], [y_max + 0.08, y_max + 0.08], 
                'k-', linewidth=1.5)
        ax.text(i, y_max + 0.10, '*', fontsize=20, ha='center', fontweight='bold')
        ax.text(i, y_max + 0.14, 'p < 0.05', fontsize=9, ha='center', style='italic')
    
    # Add sample size below
    ax.text(i, -0.08, f'n = {data["n"]}', ha='center', fontsize=10, 
            style='italic', color='gray')

# Customize plot
ax.set_ylabel('Preference Proportion', fontsize=13, fontweight='bold')
ax.set_title('Human Preference for Code Readability Metrics', fontsize=15, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([d['pair'] for d in comparison_data], fontsize=11)
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.4, linewidth=1.5, 
           label='No preference (50%)')
ax.set_ylim([-0.1, 1.0])

# Create custom legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=colors['LOGPROB'], alpha=0.8, edgecolor='black', label='Log-probability'),
    Patch(facecolor=colors['TOKENS'], alpha=0.8, edgecolor='black', label='Token count'),
    Patch(facecolor=colors['MI'], alpha=0.8, edgecolor='black', label='Mutual Information'),
]
ax.legend(handles=legend_elements, loc='upper right', framealpha=0.95, 
          title='Metrics', title_fontsize=11)

# Add grid for better readability
ax.grid(True, alpha=0.2, axis='y')
ax.set_axisbelow(True)

# Add interpretation note
ax.text(0.02, 0.98, 'Error bars: 95% CI (Wilson score method)', 
        transform=ax.transAxes, fontsize=9, style='italic',
        va='top', ha='left',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.7))

plt.tight_layout()
plt.savefig('preference_proportions_clean.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: preference_proportions_clean.png")

# Also create a version without the significance annotations for cleaner look
fig2, ax2 = plt.subplots(1, 1, figsize=(10, 6))

for i, data in enumerate(comparison_data):
    # First metric
    error1 = [[data['m1_prop'] - data['m1_ci'][0]], 
              [data['m1_ci'][1] - data['m1_prop']]]
    bar1 = ax2.bar(i - width/2, data['m1_prop'], width,
                    yerr=error1, capsize=6,
                    color=colors.get(data['m1'], 'gray'),
                    alpha=0.8, edgecolor='black', linewidth=1.5,
                    error_kw={'linewidth': 2, 'ecolor': 'black'})
    
    # Second metric
    error2 = [[data['m2_prop'] - data['m2_ci'][0]], 
              [data['m2_ci'][1] - data['m2_prop']]]
    bar2 = ax2.bar(i + width/2, data['m2_prop'], width,
                    yerr=error2, capsize=6,
                    color=colors.get(data['m2'], 'gray'),
                    alpha=0.8, edgecolor='black', linewidth=1.5,
                    error_kw={'linewidth': 2, 'ecolor': 'black'})
    
    # Add percentage labels on bars
    ax2.text(i - width/2, data['m1_prop'] + 0.02, f"{data['m1_prop']:.1%}",
             ha='center', va='bottom', fontweight='bold', fontsize=10)
    ax2.text(i + width/2, data['m2_prop'] + 0.02, f"{data['m2_prop']:.1%}",
             ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Add sample size below
    ax2.text(i, -0.08, f'n = {data["n"]}', ha='center', fontsize=10, 
             style='italic', color='gray')

ax2.set_ylabel('Preference Proportion', fontsize=13, fontweight='bold')
ax2.set_title('Human Preference for Code Readability Metrics', fontsize=15, fontweight='bold', pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels([d['pair'] for d in comparison_data], fontsize=11)
ax2.axhline(y=0.5, color='gray', linestyle='--', alpha=0.4, linewidth=1.5)
ax2.set_ylim([-0.1, 0.85])

# Legend
legend_elements = [
    Patch(facecolor=colors['LOGPROB'], alpha=0.8, edgecolor='black', label='Log-probability'),
    Patch(facecolor=colors['TOKENS'], alpha=0.8, edgecolor='black', label='Token count'),
    Patch(facecolor=colors['MI'], alpha=0.8, edgecolor='black', label='Mutual Information'),
]
ax2.legend(handles=legend_elements, loc='upper right', framealpha=0.95, 
           title='Metrics', title_fontsize=11)

ax2.grid(True, alpha=0.2, axis='y')
ax2.set_axisbelow(True)

ax2.text(0.02, 0.98, 'Error bars represent 95% confidence intervals', 
         transform=ax2.transAxes, fontsize=9, style='italic',
         va='top', ha='left')

plt.tight_layout()
plt.savefig('preference_proportions_simple.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: preference_proportions_simple.png")

print("\nCreated two versions:")
print("1. preference_proportions_clean.png - with significance markers")
print("2. preference_proportions_simple.png - cleaner version without markers")