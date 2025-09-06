import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')
results_df = pd.read_csv('results.csv')

# Load Bradley-Terry results to get consensus
bt_results = pd.read_csv('bradley_terry_results.csv')

def fit_bradley_terry(comparisons_df):
    """Fit Bradley-Terry model to get consensus preferences"""
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
    
    log_params = np.concatenate([[0], result.x])
    params = np.exp(log_params)
    
    # Calculate win probabilities
    win_probs = {}
    for i in range(n_metrics):
        for j in range(n_metrics):
            if i != j:
                p_ij = params[i] / (params[i] + params[j])
                win_probs[(metrics[i], metrics[j])] = p_ij
    
    return win_probs

# Get consensus probabilities
consensus_probs = fit_bradley_terry(merged_df)

# Analyze each participant
participant_analysis = []

for user_id in merged_df['UserID'].unique():
    user_data = merged_df[merged_df['UserID'] == user_id]
    
    # Calculate different outlier metrics
    
    # 1. Agreement with consensus
    agreements = []
    log_likelihood = 0
    
    for _, row in user_data.iterrows():
        if pd.isna(row['Actual_Choice']) or row['Actual_Choice'] == 'EG':
            continue
            
        m1 = row['Original V1 Metric']
        m2 = row['Original V2 Metric']
        choice = row['Actual_Choice']
        
        # Get consensus probability
        if choice == m1:
            prob = consensus_probs.get((m1, m2), 0.5)
        elif choice == m2:
            prob = consensus_probs.get((m2, m1), 0.5)
        else:
            prob = 0.5
        
        agreements.append(prob)
        log_likelihood += np.log(prob + 1e-10)
    
    # 2. Consistency score (transitivity violations)
    transitivity_violations = 0
    comparisons_made = {}
    
    for _, row in user_data.iterrows():
        if pd.isna(row['Actual_Choice']) or row['Actual_Choice'] == 'EG':
            continue
            
        m1 = row['Original V1 Metric']
        m2 = row['Original V2 Metric']
        choice = row['Actual_Choice']
        
        if choice == m1:
            comparisons_made[(m1, m2)] = 1
            comparisons_made[(m2, m1)] = 0
        elif choice == m2:
            comparisons_made[(m1, m2)] = 0
            comparisons_made[(m2, m1)] = 1
    
    # Check transitivity: if A>B and B>C, then A>C
    metrics = ['mi', 'tokens', 'logprob']
    for i, m1 in enumerate(metrics):
        for j, m2 in enumerate(metrics):
            for k, m3 in enumerate(metrics):
                if i != j and j != k and i != k:
                    if (m1, m2) in comparisons_made and (m2, m3) in comparisons_made and (m1, m3) in comparisons_made:
                        if comparisons_made[(m1, m2)] == 1 and comparisons_made[(m2, m3)] == 1:
                            if comparisons_made[(m1, m3)] == 0:
                                transitivity_violations += 1
    
    # 3. Response time consistency (if available)
    # 4. EG rate (too many "equally good" might indicate lack of engagement)
    eg_rate = len(user_data[user_data['Actual_Choice'] == 'EG']) / len(user_data)
    
    # Get user info
    user_info = results_df[results_df['UserID'] == user_id].iloc[0] if len(results_df[results_df['UserID'] == user_id]) > 0 else None
    
    participant_analysis.append({
        'UserID': user_id,
        'Name': user_info['Name'] if user_info is not None else 'Unknown',
        'Mean_Agreement': np.mean(agreements) if agreements else 0,
        'Log_Likelihood': log_likelihood,
        'Transitivity_Violations': transitivity_violations,
        'EG_Rate': eg_rate,
        'Total_Comparisons': len(user_data)
    })

# Create dataframe
participant_df = pd.DataFrame(participant_analysis)

# Calculate outlier scores using multiple methods
# 1. Z-score on mean agreement
participant_df['Agreement_Z'] = stats.zscore(participant_df['Mean_Agreement'])

# 2. Z-score on log-likelihood
participant_df['LL_Z'] = stats.zscore(participant_df['Log_Likelihood'])

# 3. Combined outlier score
participant_df['Outlier_Score'] = (
    -participant_df['Agreement_Z'] +  # Lower agreement = higher outlier score
    -participant_df['LL_Z'] +  # Lower likelihood = higher outlier score
    participant_df['Transitivity_Violations'] +  # More violations = higher score
    abs(participant_df['EG_Rate'] - participant_df['EG_Rate'].median()) * 10  # Extreme EG rates
)

# Identify outliers (multiple criteria)
participant_df['Is_Outlier'] = (
    (participant_df['Agreement_Z'] < -2) |  # Very low agreement
    (participant_df['LL_Z'] < -2) |  # Very unlikely responses
    (participant_df['Transitivity_Violations'] > 2) |  # Many inconsistencies
    (participant_df['Outlier_Score'] > participant_df['Outlier_Score'].quantile(0.95))  # Top 5% outlier score
)

print("=" * 70)
print("Outlier Detection Analysis")
print("=" * 70)

# Summary statistics
print(f"\nTotal participants: {len(participant_df)}")
print(f"Identified outliers: {participant_df['Is_Outlier'].sum()}")
print(f"Outlier rate: {participant_df['Is_Outlier'].mean():.1%}")

# Show outliers
outliers = participant_df[participant_df['Is_Outlier']].sort_values('Outlier_Score', ascending=False)

if len(outliers) > 0:
    print("\n" + "-" * 70)
    print("Identified Outliers:")
    print("-" * 70)
    
    for _, p in outliers.iterrows():
        print(f"\n{p['Name']} ({p['UserID']})")
        print(f"  Mean agreement with consensus: {p['Mean_Agreement']:.2%}")
        print(f"  Agreement Z-score: {p['Agreement_Z']:.2f}")
        print(f"  Log-likelihood Z-score: {p['LL_Z']:.2f}")
        print(f"  Transitivity violations: {p['Transitivity_Violations']}")
        print(f"  EG rate: {p['EG_Rate']:.1%}")
        print(f"  Overall outlier score: {p['Outlier_Score']:.2f}")
        
        # Show their specific unusual choices
        user_data = merged_df[merged_df['UserID'] == p['UserID']]
        unusual_choices = []
        
        for _, row in user_data.iterrows():
            if pd.isna(row['Actual_Choice']) or row['Actual_Choice'] == 'EG':
                continue
                
            m1 = row['Original V1 Metric']
            m2 = row['Original V2 Metric']
            choice = row['Actual_Choice']
            
            # Check if this goes strongly against consensus
            if choice == m1:
                prob = consensus_probs.get((m1, m2), 0.5)
            else:
                prob = consensus_probs.get((m2, m1), 0.5)
            
            if prob < 0.3:  # Chose something with <30% consensus probability
                unusual_choices.append(f"    Chose {choice} over {m2 if choice == m1 else m1} (consensus: {prob:.1%})")
        
        if unusual_choices:
            print("  Unusual choices:")
            for uc in unusual_choices[:3]:  # Show top 3 unusual choices
                print(uc)
else:
    print("\nNo significant outliers detected!")

# Rerun Bradley-Terry without outliers
print("\n" + "=" * 70)
print("Bradley-Terry Analysis: With vs Without Outliers")
print("-" * 70)

# Original model
original_fit = fit_bradley_terry(merged_df)

# Model without outliers
clean_df = merged_df[~merged_df['UserID'].isin(outliers['UserID'])]
clean_fit = fit_bradley_terry(clean_df) if len(outliers) > 0 else original_fit

# Compare key probabilities
comparisons = [('logprob', 'mi'), ('tokens', 'mi'), ('logprob', 'tokens')]

print(f"\n{'Comparison':<20} {'Original':<15} {'Without Outliers':<20} {'Change':<10}")
print("-" * 70)

for m1, m2 in comparisons:
    orig_prob = original_fit.get((m1, m2), 0.5)
    clean_prob = clean_fit.get((m1, m2), 0.5)
    change = clean_prob - orig_prob
    
    print(f"{m1.upper()} vs {m2.upper():<14} {orig_prob:.3f} ({orig_prob:.1%})    "
          f"{clean_prob:.3f} ({clean_prob:.1%})    {change:+.3f} ({change*100:+.1f}%)")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Agreement distribution
ax1 = axes[0, 0]
ax1.hist(participant_df['Mean_Agreement'], bins=20, edgecolor='black', alpha=0.7)
ax1.axvline(participant_df['Mean_Agreement'].mean(), color='red', linestyle='--', label='Mean')
ax1.axvline(participant_df['Mean_Agreement'].mean() - 2*participant_df['Mean_Agreement'].std(), 
           color='orange', linestyle='--', label='2 SD threshold')
ax1.set_xlabel('Mean Agreement with Consensus')
ax1.set_ylabel('Count')
ax1.set_title('Distribution of Agreement Scores')
ax1.legend()

# 2. Outlier scores
ax2 = axes[0, 1]
ax2.scatter(range(len(participant_df)), 
           participant_df.sort_values('Outlier_Score')['Outlier_Score'],
           c=['red' if x else 'blue' for x in participant_df.sort_values('Outlier_Score')['Is_Outlier']],
           alpha=0.6)
ax2.axhline(participant_df['Outlier_Score'].quantile(0.95), 
           color='red', linestyle='--', label='95th percentile')
ax2.set_xlabel('Participant (sorted)')
ax2.set_ylabel('Outlier Score')
ax2.set_title('Outlier Score Distribution')
ax2.legend()

# 3. Transitivity violations
ax3 = axes[1, 0]
violation_counts = participant_df['Transitivity_Violations'].value_counts().sort_index()
ax3.bar(violation_counts.index, violation_counts.values, edgecolor='black', alpha=0.7)
ax3.set_xlabel('Number of Transitivity Violations')
ax3.set_ylabel('Number of Participants')
ax3.set_title('Transitivity Consistency')

# 4. Impact on results
ax4 = axes[1, 1]
if len(outliers) > 0:
    x_pos = np.arange(len(comparisons))
    width = 0.35
    
    orig_probs = [original_fit.get(comp, 0.5) for comp in comparisons]
    clean_probs = [clean_fit.get(comp, 0.5) for comp in comparisons]
    
    ax4.bar(x_pos - width/2, orig_probs, width, label='With outliers', alpha=0.8)
    ax4.bar(x_pos + width/2, clean_probs, width, label='Without outliers', alpha=0.8)
    ax4.set_ylabel('P(First beats Second)')
    ax4.set_title('Impact of Removing Outliers')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels([f'{m1.upper()} vs {m2.upper()}' for m1, m2 in comparisons], rotation=15)
    ax4.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
    ax4.legend()
else:
    ax4.text(0.5, 0.5, 'No outliers detected', ha='center', va='center', fontsize=14)
    ax4.set_title('Impact of Removing Outliers')

plt.suptitle('Outlier Detection Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('outlier_analysis.png', dpi=300, bbox_inches='tight')
print("\nSaved: outlier_analysis.png")

# Save cleaned dataset
if len(outliers) > 0:
    clean_df.to_csv('intermediate_long_format_no_outliers.csv', index=False)
    print(f"\nSaved cleaned dataset without {len(outliers)} outliers to: intermediate_long_format_no_outliers.csv")

# Summary recommendation
print("\n" + "=" * 70)
print("RECOMMENDATION")
print("-" * 70)

if len(outliers) > 0:
    max_change = max([abs(clean_fit.get(comp, 0.5) - original_fit.get(comp, 0.5)) for comp in comparisons])
    
    if max_change > 0.05:  # More than 5% change
        print("⚠️  Removing outliers changes results by >5%. Consider:")
        print("   1. Report both analyses (with and without outliers)")
        print("   2. Use robust methods that downweight outliers")
        print("   3. Investigate outliers for data quality issues")
    else:
        print("✓ Removing outliers has minimal impact (<5% change).")
        print("  You can proceed with the full dataset or note outliers as a robustness check.")
else:
    print("✓ No significant outliers detected. Proceed with full dataset.")

participant_df.to_csv('participant_outlier_analysis.csv', index=False)
print("\nDetailed participant analysis saved to: participant_outlier_analysis.csv")