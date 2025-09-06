import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')
results_df = pd.read_csv('results.csv')

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
    
    return win_probs, params, metrics

print("=" * 70)
print("OUTLIER DETECTION: Agreement with Bradley-Terry Consensus")
print("=" * 70)

# Get consensus probabilities from full dataset
consensus_probs, bt_params, metrics = fit_bradley_terry(merged_df)

print("\nBradley-Terry consensus (what we're measuring against):")
print("-" * 50)
print("Model parameters (relative strengths):")
for i, m in enumerate(metrics):
    print(f"  {m}: {bt_params[i]:.3f}")

print("\nConsensus win probabilities:")
for pair, prob in sorted(consensus_probs.items()):
    if pair[0] < pair[1]:  # Only show each pair once
        print(f"  P({pair[0]} > {pair[1]}): {prob:.3f}")
        print(f"  P({pair[1]} > {pair[0]}): {1-prob:.3f}")

# Analyze each participant's agreement with consensus
print("\n" + "=" * 70)
print("PARTICIPANT ANALYSIS")
print("-" * 70)

participant_scores = []

for user_id in merged_df['UserID'].unique():
    user_data = merged_df[merged_df['UserID'] == user_id]
    
    # Calculate agreement with consensus for each choice
    agreements = []
    disagreements = []
    
    for _, row in user_data.iterrows():
        if pd.isna(row['Actual_Choice']) or row['Actual_Choice'] == 'EG':
            continue
            
        m1 = row['Original V1 Metric']
        m2 = row['Original V2 Metric']
        choice = row['Actual_Choice']
        
        # What does the consensus say?
        consensus_prob_m1_wins = consensus_probs.get((m1, m2), 0.5)
        
        # Did the participant agree with consensus?
        if choice == m1:
            agreement_score = consensus_prob_m1_wins
        else:  # chose m2
            agreement_score = 1 - consensus_prob_m1_wins
        
        agreements.append(agreement_score)
        
        # Track strong disagreements (chose option with <30% consensus support)
        if agreement_score < 0.3:
            disagreements.append({
                'chose': choice,
                'over': m2 if choice == m1 else m1,
                'consensus_support': agreement_score
            })
    
    # Get user info
    user_info = results_df[results_df['UserID'] == user_id].iloc[0] if len(results_df[results_df['UserID'] == user_id]) > 0 else None
    
    participant_scores.append({
        'UserID': user_id,
        'Name': user_info['Name'] if user_info is not None else 'Unknown',
        'Mean_Agreement': np.mean(agreements) if agreements else 0,
        'Min_Agreement': min(agreements) if agreements else 0,
        'Num_Choices': len(agreements),
        'Strong_Disagreements': len(disagreements),
        'Disagreement_Details': disagreements
    })

# Create dataframe and identify outliers
participant_df = pd.DataFrame(participant_scores)

# Use a simple z-score cutoff on mean agreement
participant_df['Z_Score'] = stats.zscore(participant_df['Mean_Agreement'])
participant_df['Is_Outlier'] = participant_df['Z_Score'] < -2  # 2 standard deviations below mean

# Sort by agreement
participant_df = participant_df.sort_values('Mean_Agreement')

print("\nParticipant agreement with consensus (sorted worst to best):")
print(f"{'Name':<20} {'UserID':<12} {'Mean Agreement':<15} {'Z-Score':<10} {'Outlier?':<10}")
print("-" * 70)

for _, p in participant_df.head(10).iterrows():  # Show bottom 10
    outlier = "YES***" if p['Is_Outlier'] else "no"
    print(f"{p['Name']:<20} {p['UserID']:<12} {p['Mean_Agreement']:.1%} {p['Z_Score']:>10.2f} {outlier:<10}")

# Show details of outliers
outliers = participant_df[participant_df['Is_Outlier']]

if len(outliers) > 0:
    print("\n" + "=" * 70)
    print(f"OUTLIER DETAILS ({len(outliers)} participants)")
    print("-" * 70)
    
    for _, p in outliers.iterrows():
        print(f"\n{p['Name']} ({p['UserID']})")
        print(f"  Mean agreement: {p['Mean_Agreement']:.1%} (Z = {p['Z_Score']:.2f})")
        print(f"  Made {p['Num_Choices']} choices, {p['Strong_Disagreements']} strongly against consensus")
        
        if p['Disagreement_Details']:
            print("  Examples of unusual choices:")
            for d in p['Disagreement_Details'][:3]:
                print(f"    - Chose {d['chose']} over {d['over']} (only {d['consensus_support']:.1%} consensus support)")

# Compare results with and without outliers
print("\n" + "=" * 70)
print("IMPACT OF REMOVING OUTLIERS")
print("-" * 70)

# Original model (already computed)
print("\nOriginal results (all participants):")
for pair in [('logprob', 'mi'), ('tokens', 'mi'), ('logprob', 'tokens')]:
    prob = consensus_probs.get(pair, 0.5)
    print(f"  P({pair[0]} > {pair[1]}): {prob:.3f}")

# Model without outliers
if len(outliers) > 0:
    clean_df = merged_df[~merged_df['UserID'].isin(outliers['UserID'])]
    clean_probs, clean_params, _ = fit_bradley_terry(clean_df)
    
    print(f"\nResults without {len(outliers)} outliers:")
    for pair in [('logprob', 'mi'), ('tokens', 'mi'), ('logprob', 'tokens')]:
        prob = clean_probs.get(pair, 0.5)
        print(f"  P({pair[0]} > {pair[1]}): {prob:.3f}")
    
    print("\nChange in key comparison (logprob vs tokens):")
    orig_lt = consensus_probs.get(('logprob', 'tokens'), 0.5)
    clean_lt = clean_probs.get(('logprob', 'tokens'), 0.5)
    change = clean_lt - orig_lt
    print(f"  Original: P(logprob > tokens) = {orig_lt:.3f}")
    print(f"  Without outliers: P(logprob > tokens) = {clean_lt:.3f}")
    print(f"  Change: {change:+.3f} ({change*100:+.1f} percentage points)")
    
    if abs(change) > 0.02:
        print(f"\n  {'✓' if clean_lt > 0.5 else '✗'} Removing outliers {'increases' if change > 0 else 'decreases'} logprob preference")
        print(f"  This {'helps' if change > 0 else 'does not help'} differentiate logprob from tokens")
    
    # Save cleaned data
    clean_df.to_csv('intermediate_long_format_no_outliers.csv', index=False)
    print(f"\nCleaned dataset saved to: intermediate_long_format_no_outliers.csv")
    
    # Create comparison plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Distribution of agreement scores
    ax1.hist(participant_df['Mean_Agreement'], bins=20, edgecolor='black', alpha=0.7, label='All participants')
    ax1.axvline(participant_df['Mean_Agreement'].mean(), color='blue', linestyle='--', label='Mean')
    ax1.axvline(participant_df['Mean_Agreement'].mean() - 2*participant_df['Mean_Agreement'].std(), 
               color='red', linestyle='--', label='Outlier threshold (-2σ)')
    
    # Mark outliers
    for _, outlier in outliers.iterrows():
        ax1.axvline(outlier['Mean_Agreement'], color='red', alpha=0.5, linewidth=0.5)
    
    ax1.set_xlabel('Mean Agreement with Bradley-Terry Consensus')
    ax1.set_ylabel('Number of Participants')
    ax1.set_title('Distribution of Agreement Scores')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Right: Impact on results
    comparisons = ['LOGPROB\nvs MI', 'TOKENS\nvs MI', 'LOGPROB\nvs TOKENS']
    x_pos = np.arange(len(comparisons))
    width = 0.35
    
    orig_probs = [
        consensus_probs.get(('logprob', 'mi'), 0.5),
        consensus_probs.get(('tokens', 'mi'), 0.5),
        consensus_probs.get(('logprob', 'tokens'), 0.5)
    ]
    
    clean_probs_list = [
        clean_probs.get(('logprob', 'mi'), 0.5),
        clean_probs.get(('tokens', 'mi'), 0.5),
        clean_probs.get(('logprob', 'tokens'), 0.5)
    ]
    
    bars1 = ax2.bar(x_pos - width/2, orig_probs, width, label='All participants', 
                    color='lightblue', edgecolor='black', linewidth=1.5)
    bars2 = ax2.bar(x_pos + width/2, clean_probs_list, width, label=f'Without {len(outliers)} outliers',
                    color='lightgreen', edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for i in range(len(comparisons)):
        ax2.text(i - width/2, orig_probs[i] + 0.01, f'{orig_probs[i]:.3f}', 
                ha='center', fontweight='bold')
        ax2.text(i + width/2, clean_probs_list[i] + 0.01, f'{clean_probs_list[i]:.3f}', 
                ha='center', fontweight='bold')
        
        # Show change
        change = clean_probs_list[i] - orig_probs[i]
        if abs(change) > 0.01:
            ax2.text(i, max(orig_probs[i], clean_probs_list[i]) + 0.05,
                    f'{change:+.3f}', ha='center', fontsize=9, style='italic')
    
    ax2.axhline(y=0.5, color='red', linestyle='--', alpha=0.5)
    ax2.set_ylabel('P(First metric preferred)')
    ax2.set_title('Impact of Removing Outliers on Bradley-Terry Results')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(comparisons)
    ax2.set_ylim([0.3, 0.8])
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Outlier Analysis: Agreement with Bradley-Terry Consensus', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('outlier_impact.png', dpi=300, bbox_inches='tight')
    print("\nPlot saved to: outlier_impact.png")
    
else:
    print("\nNo outliers detected (no participants > 2 SD below mean agreement)")

# Save participant analysis
participant_df.to_csv('participant_agreement_scores.csv', index=False)
print("\nParticipant scores saved to: participant_agreement_scores.csv")