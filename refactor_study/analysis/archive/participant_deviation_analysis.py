import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')
results_df = pd.read_csv('results.csv')

# Load Bradley-Terry results to get consensus rankings
bt_results = pd.read_csv('bradley_terry_results.csv')
bt_probs = pd.read_csv('bradley_terry_win_probabilities.csv', index_col=0)

# Get consensus preferences for each pair type
def get_consensus_winner(metric1, metric2):
    """Get the consensus winner based on Bradley-Terry probabilities"""
    if metric1 == metric2:
        return None
    prob_1_wins = bt_probs.loc[metric1, metric2]
    if prob_1_wins > 0.5:
        return metric1
    elif prob_1_wins < 0.5:
        return metric2
    else:
        return 'TIE'

# Calculate agreement scores for each participant
participant_analysis = []

for user_id in merged_df['UserID'].unique():
    user_data = merged_df[merged_df['UserID'] == user_id]
    
    total_comparisons = 0
    agreements = 0
    disagreements = 0
    chose_eg = 0
    
    # Track specific disagreements
    disagreement_details = []
    
    for _, row in user_data.iterrows():
        if pd.isna(row['Actual_Choice']):
            continue
            
        total_comparisons += 1
        m1 = row['Original V1 Metric']
        m2 = row['Original V2 Metric']
        user_choice = row['Actual_Choice']
        consensus = get_consensus_winner(m1, m2)
        
        if user_choice == 'EG':
            chose_eg += 1
            # Count EG as partial agreement (0.5) if consensus is not overwhelming
            prob = bt_probs.loc[m1, m2] if m1 != m2 else 0.5
            if 0.4 < prob < 0.6:  # Close to tie
                agreements += 0.5
            else:
                disagreement_details.append({
                    'comparison': f"{m1} vs {m2}",
                    'user_choice': 'EG',
                    'consensus': consensus,
                    'bt_prob': prob
                })
        elif user_choice == consensus:
            agreements += 1
        else:
            disagreements += 1
            prob = bt_probs.loc[m1, m2] if m1 != m2 else 0.5
            disagreement_details.append({
                'comparison': f"{m1} vs {m2}",
                'user_choice': user_choice,
                'consensus': consensus,
                'bt_prob': prob
            })
    
    agreement_rate = agreements / total_comparisons if total_comparisons > 0 else 0
    
    # Get user info
    user_info = results_df[results_df['UserID'] == user_id].iloc[0] if len(results_df[results_df['UserID'] == user_id]) > 0 else None
    
    participant_analysis.append({
        'UserID': user_id,
        'Name': user_info['Name'] if user_info is not None else 'Unknown',
        'Email': user_info['Email'] if user_info is not None else 'Unknown',
        'Total_Comparisons': total_comparisons,
        'Agreements': agreements,
        'Disagreements': disagreements,
        'EG_Choices': chose_eg,
        'Agreement_Rate': agreement_rate,
        'Disagreement_Rate': disagreements / total_comparisons if total_comparisons > 0 else 0,
        'EG_Rate': chose_eg / total_comparisons if total_comparisons > 0 else 0,
        'Disagreement_Details': disagreement_details
    })

# Create dataframe
participant_df = pd.DataFrame(participant_analysis)
participant_df = participant_df.sort_values('Agreement_Rate', ascending=False)

# Calculate z-scores for agreement rates
mean_agreement = participant_df['Agreement_Rate'].mean()
std_agreement = participant_df['Agreement_Rate'].std()
participant_df['Agreement_Z_Score'] = (participant_df['Agreement_Rate'] - mean_agreement) / std_agreement

# Identify outliers (z-score < -2 or very low agreement rate)
participant_df['Is_Outlier'] = (participant_df['Agreement_Z_Score'] < -2) | (participant_df['Agreement_Rate'] < 0.3)

print("=" * 70)
print("Individual Participant Deviation Analysis")
print("=" * 70)

print(f"\nOverall Statistics:")
print(f"  Mean agreement rate: {mean_agreement:.2%}")
print(f"  Std deviation: {std_agreement:.2%}")
print(f"  Total participants: {len(participant_df)}")

# Show top conformists
print("\n" + "=" * 70)
print("Top 5 Most Conforming Participants (highest agreement with consensus):")
print("-" * 70)
for i, row in participant_df.head(5).iterrows():
    print(f"{row['Name']:20s} ({row['UserID']})")
    print(f"  Agreement rate: {row['Agreement_Rate']:.1%} (Z-score: {row['Agreement_Z_Score']:+.2f})")
    print(f"  Choices: {int(row['Agreements'])} agreements, {int(row['Disagreements'])} disagreements, {int(row['EG_Choices'])} EG")

# Show deviators
print("\n" + "=" * 70)
print("Most Deviating Participants (lowest agreement with consensus):")
print("-" * 70)
outliers = participant_df[participant_df['Is_Outlier']]
if len(outliers) > 0:
    for i, row in outliers.iterrows():
        print(f"\n{row['Name']:20s} ({row['UserID']})")
        print(f"  Agreement rate: {row['Agreement_Rate']:.1%} (Z-score: {row['Agreement_Z_Score']:+.2f})")
        print(f"  Choices: {int(row['Agreements'])} agreements, {int(row['Disagreements'])} disagreements, {int(row['EG_Choices'])} EG")
        
        if row['Disagreements'] > 0 and row['Disagreement_Details']:
            print(f"  Key disagreements:")
            for detail in row['Disagreement_Details'][:5]:  # Show top 5 disagreements
                print(f"    - {detail['comparison']}: chose {detail['user_choice']}, consensus was {detail['consensus']} (BT prob: {detail['bt_prob']:.2f})")
else:
    bottom_5 = participant_df.tail(5)
    for i, row in bottom_5.iterrows():
        print(f"\n{row['Name']:20s} ({row['UserID']})")
        print(f"  Agreement rate: {row['Agreement_Rate']:.1%} (Z-score: {row['Agreement_Z_Score']:+.2f})")
        print(f"  Choices: {int(row['Agreements'])} agreements, {int(row['Disagreements'])} disagreements, {int(row['EG_Choices'])} EG")

# Analyze patterns in disagreements
print("\n" + "=" * 70)
print("Common Patterns in Deviations:")
print("-" * 70)

# Collect all disagreements
all_disagreements = []
for _, row in participant_df.iterrows():
    for detail in row['Disagreement_Details']:
        all_disagreements.append(detail)

if all_disagreements:
    disagreement_df = pd.DataFrame(all_disagreements)
    comparison_counts = disagreement_df['comparison'].value_counts()
    
    print("\nMost controversial comparisons (most disagreements with consensus):")
    for comp, count in comparison_counts.head(5).items():
        total_for_comp = len(merged_df[
            ((merged_df['Original V1 Metric'] == comp.split(' vs ')[0]) & 
             (merged_df['Original V2 Metric'] == comp.split(' vs ')[1])) |
            ((merged_df['Original V1 Metric'] == comp.split(' vs ')[1]) & 
             (merged_df['Original V2 Metric'] == comp.split(' vs ')[0]))
        ])
        disagree_rate = count / total_for_comp if total_for_comp > 0 else 0
        print(f"  {comp}: {count} disagreements ({disagree_rate:.1%} disagreement rate)")

# Check for systematic biases
print("\n" + "=" * 70)
print("Systematic Preferences Analysis:")
print("-" * 70)

for user_id in participant_df[participant_df['Agreement_Rate'] < 0.5]['UserID']:
    user_data = merged_df[merged_df['UserID'] == user_id]
    
    # Count preferences for each metric
    metric_preferences = {'mi': 0, 'tokens': 0, 'logprob': 0, 'EG': 0}
    
    for _, row in user_data.iterrows():
        choice = row['Actual_Choice']
        if choice in metric_preferences:
            metric_preferences[choice] += 1
    
    total = sum(metric_preferences.values())
    if total > 0:
        user_info = participant_df[participant_df['UserID'] == user_id].iloc[0]
        print(f"\n{user_info['Name']} preference distribution:")
        for metric, count in sorted(metric_preferences.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                print(f"  {metric}: {count}/{total} ({count/total:.1%})")

# Statistical test for uniformity of agreement rates
print("\n" + "=" * 70)
print("Statistical Analysis:")
print("-" * 70)

# Shapiro-Wilk test for normality
statistic, p_value = stats.shapiro(participant_df['Agreement_Rate'])
print(f"Shapiro-Wilk test for normality of agreement rates:")
print(f"  Statistic: {statistic:.4f}")
print(f"  p-value: {p_value:.4f}")
if p_value > 0.05:
    print("  Agreement rates appear normally distributed")
else:
    print("  Agreement rates may not be normally distributed")

# Save detailed results
participant_df[['UserID', 'Name', 'Email', 'Agreement_Rate', 'Disagreement_Rate', 
                'EG_Rate', 'Agreement_Z_Score', 'Is_Outlier']].to_csv('participant_deviation_analysis.csv', index=False)

print(f"\nDetailed results saved to participant_deviation_analysis.csv")

# Create a simple visualization
try:
    plt.figure(figsize=(10, 6))
    plt.hist(participant_df['Agreement_Rate'], bins=15, edgecolor='black', alpha=0.7)
    plt.axvline(mean_agreement, color='red', linestyle='--', label=f'Mean ({mean_agreement:.2f})')
    plt.axvline(mean_agreement - 2*std_agreement, color='orange', linestyle='--', label='2 SD below mean')
    plt.xlabel('Agreement Rate with Consensus')
    plt.ylabel('Number of Participants')
    plt.title('Distribution of Participant Agreement with Bradley-Terry Consensus')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('participant_agreement_distribution.png', dpi=150, bbox_inches='tight')
    print(f"Distribution plot saved to participant_agreement_distribution.png")
except Exception as e:
    print(f"Could not create visualization: {e}")