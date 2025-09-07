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
print("OUTLIER DETECTION - Multiple Approaches")
print("=" * 70)

# Get consensus from full dataset
consensus_probs, bt_params, metrics = fit_bradley_terry(merged_df)

# Analyze each participant
participant_scores = []

for user_id in merged_df['UserID'].unique():
    user_data = merged_df[merged_df['UserID'] == user_id]
    
    # Track specific preferences
    preferences = {
        'logprob_over_mi': 0,
        'tokens_over_mi': 0,
        'logprob_over_tokens': 0,
        'mi_over_logprob': 0,
        'mi_over_tokens': 0,
        'tokens_over_logprob': 0,
        'total_comparisons': 0
    }
    
    agreements = []
    
    for _, row in user_data.iterrows():
        if pd.isna(row['Actual_Choice']) or row['Actual_Choice'] == 'EG':
            continue
            
        m1 = row['Original V1 Metric']
        m2 = row['Original V2 Metric']
        choice = row['Actual_Choice']
        
        # Track specific choices
        if (m1 == 'logprob' and m2 == 'mi') or (m1 == 'mi' and m2 == 'logprob'):
            if choice == 'logprob':
                preferences['logprob_over_mi'] += 1
            elif choice == 'mi':
                preferences['mi_over_logprob'] += 1
                
        if (m1 == 'tokens' and m2 == 'mi') or (m1 == 'mi' and m2 == 'tokens'):
            if choice == 'tokens':
                preferences['tokens_over_mi'] += 1
            elif choice == 'mi':
                preferences['mi_over_tokens'] += 1
                
        if (m1 == 'logprob' and m2 == 'tokens') or (m1 == 'tokens' and m2 == 'logprob'):
            if choice == 'logprob':
                preferences['logprob_over_tokens'] += 1
            elif choice == 'tokens':
                preferences['tokens_over_logprob'] += 1
        
        preferences['total_comparisons'] += 1
        
        # Calculate agreement score
        consensus_prob_m1_wins = consensus_probs.get((m1, m2), 0.5)
        
        if choice == m1:
            agreement_score = consensus_prob_m1_wins
        else:
            agreement_score = 1 - consensus_prob_m1_wins
        
        agreements.append(agreement_score)
    
    # Get user info
    user_info = results_df[results_df['UserID'] == user_id].iloc[0] if len(results_df[results_df['UserID'] == user_id]) > 0 else None
    
    participant_scores.append({
        'UserID': user_id,
        'Name': user_info['Name'] if user_info is not None else 'Unknown',
        'Mean_Agreement': np.mean(agreements) if agreements else 0,
        'Chose_MI_over_logprob': preferences['mi_over_logprob'],
        'Chose_MI_over_tokens': preferences['mi_over_tokens'],
        'Chose_tokens_over_logprob': preferences['tokens_over_logprob'],
        'Chose_logprob_over_tokens': preferences['logprob_over_tokens'],
        'Total_Comparisons': preferences['total_comparisons']
    })

# Create dataframe
participant_df = pd.DataFrame(participant_scores)

# Calculate different outlier criteria
participant_df['Z_Score'] = stats.zscore(participant_df['Mean_Agreement'])

# Method 1: Bottom quartile of agreement
q25 = participant_df['Mean_Agreement'].quantile(0.25)
participant_df['Bottom_Quartile'] = participant_df['Mean_Agreement'] < q25

# Method 2: Chose MI too often (unusual since MI is weakest)
participant_df['MI_Preference'] = (participant_df['Chose_MI_over_logprob'] + 
                                   participant_df['Chose_MI_over_tokens'])
participant_df['High_MI_Preference'] = participant_df['MI_Preference'] >= 2

# Method 3: Z-score < -1.5 (less strict than -2)
participant_df['Z_Below_1.5'] = participant_df['Z_Score'] < -1.5

print("\n1. AGREEMENT STATISTICS")
print("-" * 50)
print(f"Mean agreement: {participant_df['Mean_Agreement'].mean():.1%}")
print(f"Std deviation: {participant_df['Mean_Agreement'].std():.1%}")
print(f"Min agreement: {participant_df['Mean_Agreement'].min():.1%}")
print(f"Max agreement: {participant_df['Mean_Agreement'].max():.1%}")

# Show different outlier detection methods
print("\n2. OUTLIER DETECTION METHODS")
print("-" * 50)
print(f"Method 1 - Bottom quartile (<{q25:.1%}): {participant_df['Bottom_Quartile'].sum()} participants")
print(f"Method 2 - High MI preference (≥2 times): {participant_df['High_MI_Preference'].sum()} participants")
print(f"Method 3 - Z-score < -1.5: {participant_df['Z_Below_1.5'].sum()} participants")

# Let's use bottom quartile as it's most interpretable
outlier_method = 'Bottom_Quartile'
participant_df['Is_Outlier'] = participant_df[outlier_method]

print(f"\nUsing Method 1 (bottom quartile) for analysis...")

# Sort and show outliers
participant_df = participant_df.sort_values('Mean_Agreement')
outliers = participant_df[participant_df['Is_Outlier']]

print("\n3. IDENTIFIED OUTLIERS")
print("-" * 50)
print(f"{'Name':<20} {'UserID':<12} {'Agreement':<12} {'MI choices':<15} {'Tokens>Logprob':<15}")
print("-" * 70)

for _, p in outliers.iterrows():
    print(f"{p['Name']:<20} {p['UserID']:<12} {p['Mean_Agreement']:.1%} "
          f"MI: {p['MI_Preference']:.0f} times     "
          f"T>L: {p['Chose_tokens_over_logprob']:.0f} times")

# Compare with and without outliers
print("\n4. IMPACT ON RESULTS")
print("-" * 50)

# Original
print("With all participants:")
orig_lt = consensus_probs.get(('logprob', 'tokens'), 0.5)
orig_lm = consensus_probs.get(('logprob', 'mi'), 0.5)
orig_tm = consensus_probs.get(('tokens', 'mi'), 0.5)
print(f"  P(logprob > tokens): {orig_lt:.3f}")
print(f"  P(logprob > mi): {orig_lm:.3f}")
print(f"  P(tokens > mi): {orig_tm:.3f}")

# Without outliers
clean_df = merged_df[~merged_df['UserID'].isin(outliers['UserID'])]
clean_probs, clean_params, _ = fit_bradley_terry(clean_df)

print(f"\nWithout {len(outliers)} outliers (bottom quartile):")
clean_lt = clean_probs.get(('logprob', 'tokens'), 0.5)
clean_lm = clean_probs.get(('logprob', 'mi'), 0.5)
clean_tm = clean_probs.get(('tokens', 'mi'), 0.5)
print(f"  P(logprob > tokens): {clean_lt:.3f}")
print(f"  P(logprob > mi): {clean_lm:.3f}")
print(f"  P(tokens > mi): {clean_tm:.3f}")

print("\nChanges:")
print(f"  Logprob vs Tokens: {orig_lt:.3f} → {clean_lt:.3f} ({(clean_lt-orig_lt)*100:+.1f}pp)")
print(f"  Logprob vs MI: {orig_lm:.3f} → {clean_lm:.3f} ({(clean_lm-orig_lm)*100:+.1f}pp)")
print(f"  Tokens vs MI: {orig_tm:.3f} → {clean_tm:.3f} ({(clean_tm-orig_tm)*100:+.1f}pp)")

gap_before = orig_lt - 0.5
gap_after = clean_lt - 0.5
print(f"\nLogprob vs Tokens gap from 50%:")
print(f"  Before: {gap_before*100:+.1f}pp")
print(f"  After: {gap_after*100:+.1f}pp")
print(f"  {'✓ Gap increased' if abs(gap_after) > abs(gap_before) else '✗ Gap decreased'}")

# Try different thresholds
print("\n5. SENSITIVITY ANALYSIS - Different Outlier Thresholds")
print("-" * 50)

thresholds = [0.10, 0.15, 0.20, 0.25, 0.30]
print(f"{'Threshold':<12} {'N outliers':<12} {'P(L>T) orig':<15} {'P(L>T) clean':<15} {'Change':<10}")
print("-" * 70)

for thresh in thresholds:
    q = participant_df['Mean_Agreement'].quantile(thresh)
    outlier_ids = participant_df[participant_df['Mean_Agreement'] < q]['UserID']
    
    if len(outlier_ids) > 0:
        test_df = merged_df[~merged_df['UserID'].isin(outlier_ids)]
        test_probs, _, _ = fit_bradley_terry(test_df)
        test_lt = test_probs.get(('logprob', 'tokens'), 0.5)
        change = test_lt - orig_lt
        
        print(f"Bottom {thresh*100:.0f}%    {len(outlier_ids):<12} {orig_lt:.3f}          "
              f"{test_lt:.3f}          {change*100:+.1f}pp")

# Save cleaned dataset with bottom quartile removed
clean_df.to_csv('intermediate_long_format_no_outliers.csv', index=False)
print(f"\nCleaned dataset (without bottom quartile) saved to: intermediate_long_format_no_outliers.csv")

# Save participant analysis
participant_df.to_csv('participant_outlier_analysis.csv', index=False)
print(f"Full analysis saved to: participant_outlier_analysis.csv")