import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')
bt_results = pd.read_csv('bradley_terry_results.csv')

print("=" * 70)
print("Error Bar Analysis for Sample Size Determination")
print("=" * 70)

# 1. Calculate confidence intervals for preference proportions
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

# Analyze each metric comparison
comparisons = [
    ('mi', 'logprob'),
    ('mi', 'tokens'),
    ('logprob', 'tokens')
]

ci_data = []

for m1, m2 in comparisons:
    # Get relevant comparisons
    relevant = merged_df[
        ((merged_df['Original V1 Metric'] == m1) & (merged_df['Original V2 Metric'] == m2)) |
        ((merged_df['Original V1 Metric'] == m2) & (merged_df['Original V2 Metric'] == m1))
    ]
    
    # Exclude EG responses
    relevant_no_eg = relevant[relevant['Actual_Choice'] != 'EG']
    
    m1_wins = len(relevant_no_eg[relevant_no_eg['Actual_Choice'] == m1])
    m2_wins = len(relevant_no_eg[relevant_no_eg['Actual_Choice'] == m2])
    total = m1_wins + m2_wins
    
    # Calculate CIs
    m1_prop, m1_ci_low, m1_ci_high = calculate_ci_wilson(m1_wins, total)
    m2_prop, m2_ci_low, m2_ci_high = calculate_ci_wilson(m2_wins, total)
    
    ci_data.append({
        'comparison': f'{m1} vs {m2}',
        'm1': m1,
        'm2': m2,
        'm1_prop': m1_prop,
        'm1_ci_low': m1_ci_low,
        'm1_ci_high': m1_ci_high,
        'm1_ci_width': m1_ci_high - m1_ci_low,
        'm2_prop': m2_prop,
        'm2_ci_low': m2_ci_low,
        'm2_ci_high': m2_ci_high,
        'm2_ci_width': m2_ci_high - m2_ci_low,
        'n': total,
        'overlapping': m1_ci_high > m2_ci_low and m2_ci_high > m1_ci_low
    })

# Create figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Preference proportions with error bars
ax1 = axes[0, 0]
x_pos = np.arange(len(ci_data))
width = 0.35

for i, row in enumerate(ci_data):
    # Plot first metric
    ax1.bar(i - width/2, row['m1_prop'], width, 
            yerr=[[row['m1_prop'] - row['m1_ci_low']], 
                  [row['m1_ci_high'] - row['m1_prop']]], 
            label=row['m1'] if i == 0 else "", 
            alpha=0.8, capsize=5)
    
    # Plot second metric
    ax1.bar(i + width/2, row['m2_prop'], width, 
            yerr=[[row['m2_prop'] - row['m2_ci_low']], 
                  [row['m2_ci_high'] - row['m2_prop']]], 
            label=row['m2'] if i == 0 else "", 
            alpha=0.8, capsize=5)
    
    # Add sample size annotation
    ax1.text(i, -0.1, f'n={row["n"]}', ha='center', fontsize=9)

ax1.set_ylabel('Preference Proportion')
ax1.set_title('Preference Proportions with 95% CI Error Bars')
ax1.set_xticks(x_pos)
ax1.set_xticklabels([row['comparison'] for row in ci_data])
ax1.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
ax1.set_ylim([0, 1])
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Bradley-Terry parameters with error bars
ax2 = axes[0, 1]
metrics = bt_results['Metric'].values
strengths = bt_results['Normalized_Strength'].values
log_strengths = bt_results['Log_Strength'].values
se_log = bt_results['SE_Log_Strength'].values

# Calculate CI for normalized strengths (using delta method)
ci_lower = []
ci_upper = []
for i in range(len(metrics)):
    log_low = log_strengths[i] - 1.96 * se_log[i]
    log_high = log_strengths[i] + 1.96 * se_log[i]
    
    # Transform to strength scale
    strength_low = np.exp(log_low)
    strength_high = np.exp(log_high)
    
    # Normalize (approximate)
    total_strength = np.sum(np.exp(log_strengths))
    norm_low = strength_low / (total_strength + strength_low - np.exp(log_strengths[i]))
    norm_high = strength_high / (total_strength + strength_high - np.exp(log_strengths[i]))
    
    ci_lower.append(norm_low)
    ci_upper.append(norm_high)

x_pos = np.arange(len(metrics))
colors = ['#2ecc71', '#3498db', '#e74c3c']
ax2.bar(x_pos, strengths, yerr=[strengths - ci_lower, np.array(ci_upper) - strengths],
        color=colors, alpha=0.8, capsize=5)
ax2.set_ylabel('Bradley-Terry Strength')
ax2.set_title('Bradley-Terry Model Parameters with 95% CI')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(metrics)
ax2.grid(True, alpha=0.3)

# 3. CI Width Analysis
ax3 = axes[1, 0]
labels = []
widths = []
colors_list = []

for row in ci_data:
    labels.append(f"{row['m1']} ({row['comparison']})")
    widths.append(row['m1_ci_width'])
    colors_list.append('#e74c3c' if row['overlapping'] else '#2ecc71')
    
    labels.append(f"{row['m2']} ({row['comparison']})")
    widths.append(row['m2_ci_width'])
    colors_list.append('#e74c3c' if row['overlapping'] else '#2ecc71')

y_pos = np.arange(len(labels))
ax3.barh(y_pos, widths, color=colors_list, alpha=0.8)
ax3.set_xlabel('CI Width')
ax3.set_title('Confidence Interval Widths\n(Red = overlapping CIs, Green = separated)')
ax3.set_yticks(y_pos)
ax3.set_yticklabels(labels, fontsize=8)
ax3.axvline(x=0.2, color='gray', linestyle='--', alpha=0.5, label='Target precision')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. Sample size simulation
ax4 = axes[1, 1]

# Simulate how CI width changes with sample size
current_n = int(np.mean([row['n'] for row in ci_data]))
sample_sizes = range(10, 200, 10)
ci_widths_sim = []

for n in sample_sizes:
    # Assume 60-40 split (typical from our data)
    p = 0.6
    _, ci_low, ci_high = calculate_ci_wilson(int(p*n), n)
    ci_widths_sim.append(ci_high - ci_low)

ax4.plot(sample_sizes, ci_widths_sim, 'b-', linewidth=2)
ax4.axvline(x=current_n, color='red', linestyle='--', label=f'Current n≈{current_n}')
ax4.axhline(y=0.2, color='green', linestyle='--', alpha=0.5, label='Target precision (±10%)')
ax4.set_xlabel('Sample Size per Comparison')
ax4.set_ylabel('Expected CI Width')
ax4.set_title('Sample Size vs. Confidence Interval Width')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('error_bar_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

# Print detailed analysis
print("\n1. CURRENT CONFIDENCE INTERVAL ANALYSIS")
print("-" * 60)

for row in ci_data:
    print(f"\n{row['comparison']}:")
    print(f"  {row['m1']}: {row['m1_prop']:.1%} [{row['m1_ci_low']:.1%}, {row['m1_ci_high']:.1%}]")
    print(f"  {row['m2']}: {row['m2_prop']:.1%} [{row['m2_ci_low']:.1%}, {row['m2_ci_high']:.1%}]")
    print(f"  CI Width: {row['m1']}: ±{row['m1_ci_width']/2:.1%}, {row['m2']}: ±{row['m2_ci_width']/2:.1%}")
    print(f"  Sample size: n={row['n']}")
    
    if row['overlapping']:
        overlap_amount = min(row['m1_ci_high'], row['m2_ci_high']) - max(row['m1_ci_low'], row['m2_ci_low'])
        print(f"  ⚠️  CIs OVERLAP by {overlap_amount:.1%} - more participants may help")
    else:
        separation = max(row['m1_ci_low'], row['m2_ci_low']) - min(row['m1_ci_high'], row['m2_ci_high'])
        print(f"  ✓ CIs SEPARATED by {abs(separation):.1%} - sufficient evidence")

# Power analysis
print("\n" + "=" * 70)
print("2. POWER ANALYSIS AND SAMPLE SIZE RECOMMENDATION")
print("-" * 60)

from statsmodels.stats.power import NormalIndPower
power_analyzer = NormalIndPower()

for row in ci_data:
    # Calculate effect size from observed data
    p1 = row['m1_prop']
    p2 = row['m2_prop']
    pooled_p = (p1 + p2) / 2
    
    # Cohen's h effect size
    h = 2 * (np.arcsin(np.sqrt(p1)) - np.arcsin(np.sqrt(p2)))
    
    # Calculate power with current sample size
    current_power = power_analyzer.solve_power(
        effect_size=abs(h), 
        nobs1=row['n']/2, 
        alpha=0.05, 
        ratio=1.0
    )
    
    print(f"\n{row['comparison']}:")
    print(f"  Observed effect size (Cohen's h): {h:.3f}")
    print(f"  Current statistical power: {current_power:.1%}")
    
    if abs(h) > 0.1:  # Only if there's a meaningful effect
        # Calculate sample size needed for 80% power
        try:
            n_needed = power_analyzer.solve_power(
                effect_size=abs(h), 
                power=0.8, 
                alpha=0.05, 
                ratio=1.0
            )
            n_needed_total = int(n_needed * 2)
            
            print(f"  Sample size for 80% power: {n_needed_total} total")
            
            if n_needed_total > row['n']:
                additional = n_needed_total - row['n']
                print(f"  📊 Need {additional} more responses ({additional/row['n']*100:.0f}% increase)")
            else:
                print(f"  ✓ Current sample size is sufficient")
        except:
            print(f"  Sample size calculation failed (effect too small)")
    else:
        print(f"  Effect too small to meaningfully detect")

print("\n" + "=" * 70)
print("3. RECOMMENDATIONS")
print("-" * 60)

# Overall recommendation
max_ci_width = max([row['m1_ci_width'] for row in ci_data] + [row['m2_ci_width'] for row in ci_data])
overlapping_count = sum(1 for row in ci_data if row['overlapping'])

print(f"\nCurrent status:")
print(f"  • Maximum CI width: ±{max_ci_width/2:.1%}")
print(f"  • Overlapping CIs: {overlapping_count}/{len(ci_data)} comparisons")
print(f"  • Average sample size: {np.mean([row['n'] for row in ci_data]):.0f} per comparison")

if overlapping_count > len(ci_data) / 2:
    print(f"\n⚠️  RECOMMENDATION: Collect more data")
    print(f"  The overlapping confidence intervals suggest insufficient precision.")
    print(f"  Target: 15-25 more participants to achieve ±10% precision")
elif max_ci_width > 0.25:
    print(f"\n⚠️  MODERATE: Consider more data for precision")
    print(f"  CIs are somewhat wide (>{0.25/2:.1%}). More data would increase precision.")
    print(f"  Target: 10-15 more participants")
else:
    print(f"\n✓ SUFFICIENT: Current sample size appears adequate")
    print(f"  Most comparisons have reasonable precision.")
    print(f"  Additional data would provide marginal improvements.")

print(f"\nFigure saved as 'error_bar_analysis.png'")