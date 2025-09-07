import pandas as pd
import numpy as np

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')
results_df = pd.read_csv('results.csv')

# Define metric pairs
metric_pairs = [
    ('mi', 'tokens'),
    ('mi', 'logprob'),
    ('logprob', 'tokens')
]

# Initialize data structure for individual preferences
individual_preferences = {}

# Process each participant
for user_id in merged_df['UserID'].unique():
    user_data = merged_df[merged_df['UserID'] == user_id]
    
    # Get user info
    user_info = results_df[results_df['UserID'] == user_id].iloc[0] if len(results_df[results_df['UserID'] == user_id]) > 0 else None
    user_name = user_info['Name'] if user_info is not None else 'Unknown'
    
    # Initialize preference counts for this user
    user_prefs = {}
    for m1, m2 in metric_pairs:
        user_prefs[f'{m1}_vs_{m2}'] = {
            m1: 0,
            m2: 0,
            'EG': 0,
            'total': 0
        }
    
    # Count preferences
    for _, row in user_data.iterrows():
        if pd.isna(row['Actual_Choice']):
            continue
        
        m1 = row['Original V1 Metric']
        m2 = row['Original V2 Metric']
        choice = row['Actual_Choice']
        
        # Find the matching pair (order might be reversed)
        pair_key = None
        if (m1, m2) in metric_pairs:
            pair_key = f'{m1}_vs_{m2}'
        elif (m2, m1) in metric_pairs:
            pair_key = f'{m2}_vs_{m1}'
        
        if pair_key:
            user_prefs[pair_key]['total'] += 1
            if choice == 'EG':
                user_prefs[pair_key]['EG'] += 1
            elif choice in [m1, m2]:
                # Normalize to the pair order
                if '_vs_' in pair_key:
                    metric1, metric2 = pair_key.replace('_vs_', ' ').split()
                    if choice == metric1:
                        user_prefs[pair_key][metric1] += 1
                    else:
                        user_prefs[pair_key][metric2] += 1
    
    individual_preferences[user_id] = {
        'name': user_name,
        'preferences': user_prefs
    }

# Create detailed output
print("=" * 80)
print("Individual Participant Preference Matrix")
print("=" * 80)

# Create summary tables for each metric pair
for m1, m2 in metric_pairs:
    pair_key = f'{m1}_vs_{m2}'
    
    print(f"\n{m1.upper()} vs {m2.upper()} Comparison:")
    print("-" * 60)
    
    # Collect data for this pair
    pair_data = []
    for user_id, data in individual_preferences.items():
        prefs = data['preferences'][pair_key]
        if prefs['total'] > 0:
            pair_data.append({
                'UserID': user_id,
                'Name': data['name'],
                f'{m1}_wins': prefs[m1],
                f'{m2}_wins': prefs[m2],
                'EG': prefs['EG'],
                'Total': prefs['total'],
                f'{m1}_pct': (prefs[m1] / prefs['total'] * 100) if prefs['total'] > 0 else 0,
                f'{m2}_pct': (prefs[m2] / prefs['total'] * 100) if prefs['total'] > 0 else 0,
                'EG_pct': (prefs['EG'] / prefs['total'] * 100) if prefs['total'] > 0 else 0,
                'Winner': m1 if prefs[m1] > prefs[m2] else (m2 if prefs[m2] > prefs[m1] else 'TIE/EG')
            })
    
    pair_df = pd.DataFrame(pair_data)
    
    if len(pair_df) > 0:
        # Sort by preference strength for first metric
        pair_df = pair_df.sort_values(f'{m1}_pct', ascending=False)
        
        # Print individual results
        print(f"{'Name':<20} {'UserID':<12} {m1:>8} {m2:>8} {'EG':>5} {'Total':>6} {'Winner':>10}")
        print("-" * 70)
        
        for _, row in pair_df.iterrows():
            print(f"{row['Name']:<20} {row['UserID']:<12} "
                  f"{row[f'{m1}_wins']:>8} {row[f'{m2}_wins']:>8} "
                  f"{row['EG']:>5} {row['Total']:>6} {row['Winner']:>10}")
        
        # Summary statistics
        print(f"\nSummary:")
        total_m1_wins = pair_df[f'{m1}_wins'].sum()
        total_m2_wins = pair_df[f'{m2}_wins'].sum()
        total_eg = pair_df['EG'].sum()
        total_comparisons = pair_df['Total'].sum()
        
        print(f"  Total {m1} wins: {total_m1_wins} ({total_m1_wins/total_comparisons*100:.1f}%)")
        print(f"  Total {m2} wins: {total_m2_wins} ({total_m2_wins/total_comparisons*100:.1f}%)")
        print(f"  Total EG: {total_eg} ({total_eg/total_comparisons*100:.1f}%)")
        
        # Count how many participants preferred each metric
        m1_preferred = len(pair_df[pair_df['Winner'] == m1])
        m2_preferred = len(pair_df[pair_df['Winner'] == m2])
        tie_eg = len(pair_df[pair_df['Winner'] == 'TIE/EG'])
        
        print(f"\nParticipant preferences:")
        print(f"  Participants preferring {m1}: {m1_preferred}")
        print(f"  Participants preferring {m2}: {m2_preferred}")
        print(f"  Participants with tie/mostly EG: {tie_eg}")
        
        # Save to CSV
        pair_df.to_csv(f'individual_preferences_{m1}_vs_{m2}.csv', index=False)

# Create a comprehensive matrix for all participants
print("\n" + "=" * 80)
print("Comprehensive Preference Matrix (All Participants)")
print("-" * 80)

# Create matrix data
matrix_data = []
for user_id, data in individual_preferences.items():
    row = {
        'UserID': user_id,
        'Name': data['name']
    }
    
    for m1, m2 in metric_pairs:
        pair_key = f'{m1}_vs_{m2}'
        prefs = data['preferences'][pair_key]
        
        row[f'{m1}_vs_{m2}_{m1}'] = prefs[m1]
        row[f'{m1}_vs_{m2}_{m2}'] = prefs[m2]
        row[f'{m1}_vs_{m2}_EG'] = prefs['EG']
        row[f'{m1}_vs_{m2}_total'] = prefs['total']
        
        # Add winner for this pair
        if prefs['total'] > 0:
            if prefs[m1] > prefs[m2]:
                row[f'{m1}_vs_{m2}_winner'] = m1
            elif prefs[m2] > prefs[m1]:
                row[f'{m1}_vs_{m2}_winner'] = m2
            else:
                row[f'{m1}_vs_{m2}_winner'] = 'TIE/EG'
        else:
            row[f'{m1}_vs_{m2}_winner'] = 'N/A'
    
    matrix_data.append(row)

matrix_df = pd.DataFrame(matrix_data)
matrix_df.to_csv('individual_preference_matrix_complete.csv', index=False)

# Identify consistent patterns
print("\nConsistent Preference Patterns:")
print("-" * 40)

# Check for participants who always prefer one metric
for user_id, data in individual_preferences.items():
    metric_wins = {'mi': 0, 'tokens': 0, 'logprob': 0}
    total_decisions = 0
    
    for pair_key, prefs in data['preferences'].items():
        for metric in metric_wins:
            if metric in pair_key:
                metric_wins[metric] += prefs[metric]
                total_decisions += prefs[metric]
    
    if total_decisions > 0:
        # Check if any metric dominates (>70% of non-EG choices)
        for metric, wins in metric_wins.items():
            if wins / total_decisions > 0.7:
                print(f"{data['name']} ({user_id}): Strong preference for {metric} "
                      f"({wins}/{total_decisions} = {wins/total_decisions*100:.1f}%)")

# Identify contrarians (opposite of overall consensus)
print("\nContrarian Patterns (opposite of overall consensus):")
print("-" * 40)

# Calculate overall consensus for each pair
overall_consensus = {}
for m1, m2 in metric_pairs:
    pair_key = f'{m1}_vs_{m2}'
    total_m1 = sum(data['preferences'][pair_key][m1] for data in individual_preferences.values())
    total_m2 = sum(data['preferences'][pair_key][m2] for data in individual_preferences.values())
    
    if total_m1 > total_m2:
        overall_consensus[pair_key] = m1
    elif total_m2 > total_m1:
        overall_consensus[pair_key] = m2
    else:
        overall_consensus[pair_key] = 'TIE'

# Find contrarians
for user_id, data in individual_preferences.items():
    contrarian_count = 0
    total_pairs = 0
    
    for pair_key, consensus_winner in overall_consensus.items():
        prefs = data['preferences'][pair_key]
        if prefs['total'] > 0 and consensus_winner != 'TIE':
            total_pairs += 1
            # Check if user preferred the opposite
            m1, m2 = pair_key.replace('_vs_', ' ').split()
            user_winner = m1 if prefs[m1] > prefs[m2] else (m2 if prefs[m2] > prefs[m1] else 'TIE')
            
            if user_winner != 'TIE' and user_winner != consensus_winner:
                contrarian_count += 1
    
    if total_pairs > 0 and contrarian_count / total_pairs > 0.5:
        print(f"{data['name']} ({user_id}): Contrarian on {contrarian_count}/{total_pairs} pairs "
              f"({contrarian_count/total_pairs*100:.1f}%)")

print(f"\nResults saved to:")
print(f"  - individual_preferences_mi_vs_tokens.csv")
print(f"  - individual_preferences_mi_vs_logprob.csv")
print(f"  - individual_preferences_logprob_vs_tokens.csv")
print(f"  - individual_preference_matrix_complete.csv")