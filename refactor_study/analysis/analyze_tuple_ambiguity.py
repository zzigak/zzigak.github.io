import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 11

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')

print("=" * 80)
print("TUPLE AMBIGUITY ANALYSIS BY PAIR TYPE")
print("=" * 80)

# Calculate consensus for each tuple
tuple_stats = merged_df.groupby(['TupleID', 'Pair Type']).agg({
    'Actual_Choice': [
        lambda x: x.value_counts(normalize=True).iloc[0] if len(x) > 0 else 0,  # consensus rate
        lambda x: x.value_counts().index[0] if len(x) > 0 else None,  # majority choice
        'count'  # total votes
    ],
    'UserID': 'nunique'  # unique participants
}).reset_index()
tuple_stats.columns = ['TupleID', 'Pair Type', 'Consensus_Rate', 'Majority_Choice', 'Total_Votes', 'Unique_Participants']

# Get unique pair types
pair_types = tuple_stats['Pair Type'].unique()

# Test different thresholds
thresholds = [0.60, 0.65, 0.70, 0.75, 0.80]

# Create analysis for each threshold
print("\nAMBIGUOUS TUPLES BY PAIR TYPE AT DIFFERENT THRESHOLDS")
print("-" * 80)

results_data = []

for threshold in thresholds:
    print(f"\nThreshold: < {threshold*100:.0f}% consensus (ambiguous)")
    print("-" * 60)
    
    threshold_data = {'threshold': threshold}
    
    for pair_type in sorted(pair_types):
        # Get tuples for this pair type
        type_tuples = tuple_stats[tuple_stats['Pair Type'] == pair_type]
        total_count = len(type_tuples)
        
        # Count ambiguous tuples (below threshold)
        ambiguous_count = (type_tuples['Consensus_Rate'] < threshold).sum()
        ambiguous_pct = (ambiguous_count / total_count * 100) if total_count > 0 else 0
        
        # Count clear tuples (at or above threshold)
        clear_count = total_count - ambiguous_count
        clear_pct = (clear_count / total_count * 100) if total_count > 0 else 0
        
        print(f"  {pair_type:20} {ambiguous_count:2}/{total_count:2} ambiguous ({ambiguous_pct:5.1f}%) | "
              f"{clear_count:2} clear ({clear_pct:5.1f}%)")
        
        threshold_data[f'{pair_type}_ambiguous'] = ambiguous_count
        threshold_data[f'{pair_type}_total'] = total_count
        threshold_data[f'{pair_type}_pct'] = ambiguous_pct
    
    # Overall statistics
    total_tuples = len(tuple_stats)
    total_ambiguous = (tuple_stats['Consensus_Rate'] < threshold).sum()
    print(f"\n  TOTAL:               {total_ambiguous:2}/{total_tuples:2} ambiguous "
          f"({total_ambiguous/total_tuples*100:5.1f}%)")
    
    results_data.append(threshold_data)

# Create visualization
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Plot 1: Ambiguous tuples by threshold for each pair type
ax = axes[0]
x = np.arange(len(thresholds))
width = 0.25
colors = ['#e74c3c', '#3498db', '#2ecc71']

for i, pair_type in enumerate(sorted(pair_types)):
    ambiguous_counts = [d[f'{pair_type}_ambiguous'] for d in results_data]
    totals = [d[f'{pair_type}_total'] for d in results_data]
    
    bars = ax.bar(x + i*width, ambiguous_counts, width, 
                  label=pair_type.replace('_', ' ').upper(), 
                  color=colors[i], alpha=0.8, edgecolor='black')
    
    # Add total count labels on top
    for j, bar in enumerate(bars):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'/{totals[0]}', ha='center', fontsize=8)

ax.set_xlabel('Consensus Threshold (%)', fontsize=12)
ax.set_ylabel('Number of Ambiguous Tuples', fontsize=12)
ax.set_title('Ambiguous Tuples by Pair Type', fontsize=13, fontweight='bold')
ax.set_xticks(x + width)
ax.set_xticklabels([f'<{int(t*100)}%' for t in thresholds])
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3, axis='y')

# Plot 2: Percentage ambiguous by threshold
ax = axes[1]
for i, pair_type in enumerate(sorted(pair_types)):
    percentages = [d[f'{pair_type}_pct'] for d in results_data]
    ax.plot([t*100 for t in thresholds], percentages, 'o-', 
            linewidth=2.5, markersize=8, label=pair_type.replace('_', ' ').upper(),
            color=colors[i])

ax.set_xlabel('Consensus Threshold (%)', fontsize=12)
ax.set_ylabel('% of Tuples that are Ambiguous', fontsize=12)
ax.set_title('Percentage of Ambiguous Tuples', fontsize=13, fontweight='bold')
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_ylim([0, 105])

# Plot 3: Consensus distribution by pair type
ax = axes[2]
positions = []
data_to_plot = []
labels = []

for i, pair_type in enumerate(sorted(pair_types)):
    type_data = tuple_stats[tuple_stats['Pair Type'] == pair_type]['Consensus_Rate'] * 100
    data_to_plot.append(type_data)
    labels.append(pair_type.replace('_', ' ').upper())
    positions.append(i)

bp = ax.boxplot(data_to_plot, positions=positions, widths=0.6, 
                patch_artist=True, showmeans=True)

# Color the boxes
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

# Add threshold lines
ax.axhline(y=65, color='red', linestyle='--', alpha=0.5, linewidth=1.5, label='65% threshold')
ax.axhline(y=75, color='orange', linestyle='--', alpha=0.5, linewidth=1.5, label='75% threshold')

ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel('Consensus Rate (%)', fontsize=12)
ax.set_title('Consensus Distribution by Pair Type', fontsize=13, fontweight='bold')
ax.legend(loc='lower right', fontsize=9)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim([20, 105])

plt.suptitle('Tuple Ambiguity Analysis by Comparison Type', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('tuple_ambiguity_by_type.png', dpi=300, bbox_inches='tight')
print("\nSaved: tuple_ambiguity_by_type.png")

# Detailed analysis for 65% and 75% thresholds
print("\n" + "=" * 80)
print("DETAILED ANALYSIS: 65% AND 75% THRESHOLDS")
print("=" * 80)

for threshold in [0.65, 0.75]:
    print(f"\n{threshold*100:.0f}% Threshold Analysis")
    print("-" * 60)
    
    for pair_type in sorted(pair_types):
        type_tuples = tuple_stats[tuple_stats['Pair Type'] == pair_type]
        ambiguous = type_tuples[type_tuples['Consensus_Rate'] < threshold]
        clear = type_tuples[type_tuples['Consensus_Rate'] >= threshold]
        
        print(f"\n{pair_type.replace('_', ' ').upper()}:")
        print(f"  Total tuples: {len(type_tuples)}")
        print(f"  Ambiguous (<{threshold*100:.0f}%): {len(ambiguous)} tuples")
        print(f"  Clear (≥{threshold*100:.0f}%): {len(clear)} tuples")
        
        if len(ambiguous) > 0:
            print(f"  Ambiguous tuple IDs: {sorted(ambiguous['TupleID'].tolist())}")
            print(f"  Consensus rates: {[f'{x*100:.0f}%' for x in sorted(ambiguous['Consensus_Rate'].tolist())]}")

# Save summary table
summary_df = pd.DataFrame(results_data)
summary_df.to_csv('tuple_ambiguity_summary.csv', index=False)
print("\nSummary data saved to: tuple_ambiguity_summary.csv")

# Key findings
print("\n" + "=" * 80)
print("KEY FINDINGS")
print("=" * 80)

# Find which pair type is most ambiguous
for threshold in [0.65, 0.75]:
    print(f"\nAt {threshold*100:.0f}% threshold:")
    max_ambiguous_type = None
    max_ambiguous_pct = 0
    
    for pair_type in pair_types:
        type_tuples = tuple_stats[tuple_stats['Pair Type'] == pair_type]
        ambiguous_pct = ((type_tuples['Consensus_Rate'] < threshold).sum() / len(type_tuples) * 100) if len(type_tuples) > 0 else 0
        
        if ambiguous_pct > max_ambiguous_pct:
            max_ambiguous_pct = ambiguous_pct
            max_ambiguous_type = pair_type
    
    if max_ambiguous_type:
        print(f"  Most ambiguous: {max_ambiguous_type} ({max_ambiguous_pct:.1f}% of tuples)")
    
    # Count responses that would be removed
    ambiguous_tuples = tuple_stats[tuple_stats['Consensus_Rate'] < threshold]
    responses_removed = merged_df.merge(ambiguous_tuples[['TupleID', 'Pair Type']], 
                                        on=['TupleID', 'Pair Type'], how='inner')
    print(f"  Total responses removed: {len(responses_removed)}/{len(merged_df)} ({len(responses_removed)/len(merged_df)*100:.1f}%)")