import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')

print("=" * 80)
print("SIMPLE RATIO ANALYSIS (Direct Preference Counts)")
print("=" * 80)

# Initialize win matrix
metrics = ['mi', 'tokens', 'logprob']
wins = {m: {n: 0 for n in metrics} for m in metrics}
totals = {m: {n: 0 for n in metrics} for m in metrics}

# Count wins for each pair
for _, row in merged_df.iterrows():
    if row['Actual_Choice'] in ['EG', None] or pd.isna(row['Actual_Choice']):
        continue
    
    m1 = row['Original V1 Metric']
    m2 = row['Original V2 Metric']
    choice = row['Actual_Choice']
    
    if m1 in metrics and m2 in metrics:
        totals[m1][m2] += 1
        totals[m2][m1] += 1
        
        if choice == m1:
            wins[m1][m2] += 1
        elif choice == m2:
            wins[m2][m1] += 1

# Calculate simple ratios
print("\n1. DIRECT WIN RATIOS")
print("-" * 40)
print("P(row preferred over column):")
print(f"{'':10} {'mi':>10} {'tokens':>10} {'logprob':>10}")
print("-" * 40)

ratios = {}
for m1 in metrics:
    row_str = f"{m1:10}"
    for m2 in metrics:
        if m1 == m2:
            row_str += f"{'---':>10}"
        else:
            if totals[m1][m2] > 0:
                ratio = wins[m1][m2] / totals[m1][m2]
                ratios[(m1, m2)] = ratio
                row_str += f"{ratio:>10.1%}"
            else:
                row_str += f"{'N/A':>10}"
    print(row_str)

# Calculate overall preference scores (average win rate)
print("\n2. OVERALL PREFERENCE SCORES")
print("-" * 40)
overall_scores = {}
for m in metrics:
    win_rates = []
    for other in metrics:
        if m != other and (m, other) in ratios:
            win_rates.append(ratios[(m, other)])
    overall_scores[m] = np.mean(win_rates) if win_rates else 0
    print(f"{m:10} Average win rate: {overall_scores[m]:.1%}")

# Rank metrics
ranked = sorted(overall_scores.items(), key=lambda x: x[1], reverse=True)
print("\n3. RANKING BY SIMPLE RATIOS")
print("-" * 40)
for i, (metric, score) in enumerate(ranked, 1):
    print(f"{i}. {metric:10} ({score:.1%} average win rate)")

# Key comparisons
print("\n4. KEY PAIRWISE COMPARISONS")
print("-" * 40)
key_pairs = [('logprob', 'mi'), ('tokens', 'mi'), ('logprob', 'tokens')]
for m1, m2 in key_pairs:
    if (m1, m2) in ratios:
        r = ratios[(m1, m2)]
        n = totals[m1][m2]
        print(f"{m1.upper()} vs {m2.upper()}:")
        print(f"  {m1} preferred: {r:.1%} ({wins[m1][m2]}/{n})")
        print(f"  {m2} preferred: {(1-r):.1%} ({wins[m2][m1]}/{n})")
        print()

# Create visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Win matrix heatmap
matrix_data = np.zeros((3, 3))
for i, m1 in enumerate(metrics):
    for j, m2 in enumerate(metrics):
        if m1 != m2 and (m1, m2) in ratios:
            matrix_data[i, j] = ratios[(m1, m2)]
        elif m1 == m2:
            matrix_data[i, j] = 0.5  # Diagonal

im = ax1.imshow(matrix_data, cmap='RdYlGn', vmin=0, vmax=1, aspect='auto')
ax1.set_xticks(range(3))
ax1.set_yticks(range(3))
ax1.set_xticklabels([m.upper() for m in metrics])
ax1.set_yticklabels([m.upper() for m in metrics])
ax1.set_title('Win Rate Matrix\n(row beats column)', fontsize=13, fontweight='bold')

# Add text annotations
for i in range(3):
    for j in range(3):
        if i != j:
            text = ax1.text(j, i, f'{matrix_data[i, j]:.1%}',
                          ha="center", va="center", color="black", fontweight='bold')
        else:
            text = ax1.text(j, i, '—', ha="center", va="center", color="gray")

plt.colorbar(im, ax=ax1, label='Win Rate')

# Plot 2: Overall preference scores
ax2.bar(range(3), [overall_scores[m] for m in metrics], 
        color=['#e74c3c' if s < 0.5 else '#2ecc71' for s in overall_scores.values()],
        alpha=0.7, edgecolor='black', linewidth=2)
ax2.set_xticks(range(3))
ax2.set_xticklabels([m.upper() for m in metrics])
ax2.set_ylabel('Average Win Rate', fontsize=12)
ax2.set_title('Overall Preference Scores', fontsize=13, fontweight='bold')
ax2.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=1.5)
ax2.set_ylim([0, 1])
ax2.grid(True, alpha=0.3, axis='y')

# Add value labels
for i, m in enumerate(metrics):
    ax2.text(i, overall_scores[m] + 0.02, f'{overall_scores[m]:.1%}', 
            ha='center', fontweight='bold')

plt.suptitle('Simple Ratio Analysis (Direct Preference Counts)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('simple_ratio_analysis.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved to: simple_ratio_analysis.png")

# Compare with Bradley-Terry if available
try:
    bt_results = pd.read_csv('bradley_terry_win_probabilities.csv', index_col=0)
    print("\n5. COMPARISON: SIMPLE RATIOS vs BRADLEY-TERRY")
    print("-" * 40)
    for m1, m2 in key_pairs:
        simple = ratios.get((m1, m2), 0)
        bt = bt_results.loc[m1, m2] if m1 in bt_results.index and m2 in bt_results.columns else None
        if bt is not None:
            diff = simple - bt
            print(f"{m1.upper()} vs {m2.upper()}:")
            print(f"  Simple ratio:  {simple:.1%}")
            print(f"  Bradley-Terry: {bt:.1%}")
            print(f"  Difference:    {diff:+.1%}")
            print()
except FileNotFoundError:
    print("\n(Bradley-Terry results not found for comparison)")

print("\n" + "=" * 80)
print("KEY FINDINGS (Simple Ratios)")
print("-" * 80)
print(f"• Strongest metric: {ranked[0][0].upper()} ({ranked[0][1]:.1%} average win rate)")
print(f"• Weakest metric: {ranked[-1][0].upper()} ({ranked[-1][1]:.1%} average win rate)")
best_pair = max(key_pairs, key=lambda p: abs(ratios.get(p, 0.5) - 0.5))
print(f"• Clearest distinction: {best_pair[0].upper()} vs {best_pair[1].upper()} "
      f"({ratios[best_pair]:.1%}/{(1-ratios[best_pair]):.1%})")