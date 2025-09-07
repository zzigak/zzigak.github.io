import pandas as pd
import numpy as np
from collections import defaultdict
from scipy import stats

# Load data
assignments_df = pd.read_csv('user_study_final_shuffled_assignments.csv')
results_df = pd.read_csv('results.csv')

# Transform results from wide to long format
# Each participant has 10 tuple responses spread across columns
response_cols = []
for i in range(10):
    base = 7 + i * 4  # Starting position for each set of response columns
    response_cols.append({
        'tuple_id_col': base,
        'pair_id_col': base + 1,
        'choice_col': base + 2,
        'reason_col': base + 3
    })

# Create long format dataframe
long_results = []
for _, row in results_df.iterrows():
    user_id = row['UserID']
    
    for i, cols in enumerate(response_cols):
        tuple_id = row.iloc[cols['tuple_id_col']-1] if pd.notna(row.iloc[cols['tuple_id_col']-1]) else None
        if tuple_id is None or tuple_id == '':
            continue
            
        long_results.append({
            'UserID': user_id,
            'Position': i + 1,
            'TupleID': int(tuple_id) if not pd.isna(float(tuple_id)) else None,
            'Choice': row.iloc[cols['choice_col']-1],
            'Reason': row.iloc[cols['reason_col']-1]
        })

long_results_df = pd.DataFrame(long_results)

# Merge with assignments to get swap info and pair type
merged_df = pd.merge(
    long_results_df,
    assignments_df[['User ID', 'Position', 'Tuple Index', 'Tuple Name', 'Cluster', 
                    'Pair Type', 'Original V1 Metric', 'Original V2 Metric', 'Swapped']],
    left_on=['UserID', 'Position'],
    right_on=['User ID', 'Position'],
    how='inner'
)

# Adjust choices based on swap flag
def get_actual_choice(row):
    """Convert V1/V2 choice to actual metric chosen, accounting for swaps"""
    if pd.isna(row['Choice']) or row['Choice'] == 'EG':
        return row['Choice']
    
    if row['Swapped'] == 'Yes':
        # If swapped, V1 shown was actually original V2
        if row['Choice'] == 'V1':
            return row['Original V2 Metric']
        elif row['Choice'] == 'V2':
            return row['Original V1 Metric']
    else:
        # Not swapped
        if row['Choice'] == 'V1':
            return row['Original V1 Metric']
        elif row['Choice'] == 'V2':
            return row['Original V2 Metric']
    
    return row['Choice']

merged_df['Actual_Choice'] = merged_df.apply(get_actual_choice, axis=1)

# Save intermediate long format file
merged_df.to_csv('intermediate_long_format.csv', index=False)
print(f"Saved intermediate long format to intermediate_long_format.csv")

# Aggregate preferences by cluster, tuple, and pair type
aggregated = []

for (cluster, tuple_name, pair_type), group in merged_df.groupby(['Cluster', 'Tuple Name', 'Pair Type']):
    # Get the original metrics for this pair type
    original_v1 = group['Original V1 Metric'].iloc[0]
    original_v2 = group['Original V2 Metric'].iloc[0]
    
    # Count choices
    choice_counts = group['Actual_Choice'].value_counts()
    
    v1_count = choice_counts.get(original_v1, 0)
    v2_count = choice_counts.get(original_v2, 0)
    eg_count = choice_counts.get('EG', 0)
    total = len(group)
    
    # Determine winner
    if v1_count > v2_count:
        winner = original_v1
        win_pct = (v1_count / total) * 100
    elif v2_count > v1_count:
        winner = original_v2
        win_pct = (v2_count / total) * 100
    else:
        winner = 'TIE'
        win_pct = max(v1_count, v2_count) / total * 100 if total > 0 else 0
    
    aggregated.append({
        'Cluster': cluster,
        'Tuple': tuple_name,
        'Pair_Type': pair_type,
        'Metric_1': original_v1,
        'Metric_2': original_v2,
        f'{original_v1}_Count': v1_count,
        f'{original_v2}_Count': v2_count,
        'EG_Count': eg_count,
        'Total_Responses': total,
        'Winner': winner,
        'Win_Percentage': round(win_pct, 1),
        'Participants': ', '.join(group['UserID'].unique())
    })

# Create final dataframe and save
final_df = pd.DataFrame(aggregated)
final_df = final_df.sort_values(['Cluster', 'Tuple', 'Pair_Type'])

# Save per-tuple analysis to CSV
final_df.to_csv('preference_analysis_per_tuple.csv', index=False)

# Print summary statistics
print("Preference Analysis Summary")
print("=" * 50)
print(f"Total unique tuples analyzed: {final_df['Tuple'].nunique()}")
print(f"Total comparisons: {final_df['Total_Responses'].sum()}")
print()

# Summary by pair type
for pair_type in final_df['Pair_Type'].unique():
    pair_data = final_df[final_df['Pair_Type'] == pair_type]
    print(f"\n{pair_type}:")
    print(f"  Total comparisons: {pair_data['Total_Responses'].sum()}")
    
    # Count wins by metric
    for metric in ['mi', 'tokens', 'logprob']:
        wins = len(pair_data[pair_data['Winner'] == metric])
        if wins > 0:
            print(f"  {metric} wins: {wins}")
    
    ties = len(pair_data[pair_data['Winner'] == 'TIE'])
    if ties > 0:
        print(f"  Ties: {ties}")

# Create overall aggregation by pair type (summing across all tuples)
overall_aggregated = []

for pair_type in merged_df['Pair Type'].unique():
    pair_data = merged_df[merged_df['Pair Type'] == pair_type]
    
    # Get the metrics being compared
    original_v1 = pair_data['Original V1 Metric'].iloc[0]
    original_v2 = pair_data['Original V2 Metric'].iloc[0]
    
    # Count total votes across all tuples
    choice_counts = pair_data['Actual_Choice'].value_counts()
    
    v1_total = choice_counts.get(original_v1, 0)
    v2_total = choice_counts.get(original_v2, 0)
    eg_total = choice_counts.get('EG', 0)
    total = len(pair_data)
    
    # Determine overall winner
    if v1_total > v2_total:
        winner = original_v1
        win_pct = (v1_total / total) * 100
    elif v2_total > v1_total:
        winner = original_v2
        win_pct = (v2_total / total) * 100
    else:
        winner = 'TIE'
        win_pct = max(v1_total, v2_total) / total * 100 if total > 0 else 0
    
    # Count how many tuples each metric won
    tuple_wins_v1 = 0
    tuple_wins_v2 = 0
    tuple_ties = 0
    
    for _, tuple_group in pair_data.groupby('Tuple Name'):
        tuple_counts = tuple_group['Actual_Choice'].value_counts()
        v1_count = tuple_counts.get(original_v1, 0)
        v2_count = tuple_counts.get(original_v2, 0)
        if v1_count > v2_count:
            tuple_wins_v1 += 1
        elif v2_count > v1_count:
            tuple_wins_v2 += 1
        else:
            tuple_ties += 1
    
    # Calculate percentages excluding EG responses
    non_eg_total = v1_total + v2_total
    if non_eg_total > 0:
        v1_pct_no_eg = (v1_total / non_eg_total) * 100
        v2_pct_no_eg = (v2_total / non_eg_total) * 100
        winner_no_eg = original_v1 if v1_total > v2_total else (original_v2 if v2_total > v1_total else 'TIE')
        win_pct_no_eg = max(v1_pct_no_eg, v2_pct_no_eg)
        
        # Binomial test for statistical significance (excluding EG)
        # Null hypothesis: p = 0.5 (no preference)
        # Test if the observed split is significantly different from 50/50
        max_votes = max(v1_total, v2_total)
        binom_test = stats.binomtest(max_votes, non_eg_total, 0.5, alternative='two-sided')
        binom_result = binom_test.pvalue
        
        # Determine significance level
        if binom_result < 0.001:
            significance = '***'
        elif binom_result < 0.01:
            significance = '**'
        elif binom_result < 0.05:
            significance = '*'
        else:
            significance = 'ns'
        
        # Calculate odds ratio
        # Odds of preferring v1 = v1_total / v2_total
        # If v2_total is 0, add 0.5 to both for continuity correction
        if v2_total == 0:
            odds_ratio = (v1_total + 0.5) / 0.5
        elif v1_total == 0:
            odds_ratio = 0.5 / (v2_total + 0.5)
        else:
            odds_ratio = v1_total / v2_total
        
        # Calculate 95% CI for log odds ratio
        # Using Woolf's method with continuity correction
        a = v1_total if v1_total > 0 else 0.5
        b = v2_total if v2_total > 0 else 0.5
        log_or = np.log(a/b)
        se_log_or = np.sqrt(1/a + 1/b)
        ci_lower = np.exp(log_or - 1.96 * se_log_or)
        ci_upper = np.exp(log_or + 1.96 * se_log_or)
    else:
        v1_pct_no_eg = 0
        v2_pct_no_eg = 0
        winner_no_eg = 'N/A'
        win_pct_no_eg = 0
        binom_result = 1.0
        significance = 'N/A'
        odds_ratio = np.nan
        ci_lower = np.nan
        ci_upper = np.nan
    
    overall_aggregated.append({
        'Pair_Type': pair_type,
        'Metric_1': original_v1,
        'Metric_2': original_v2,
        f'{original_v1}_Total_Votes': v1_total,
        f'{original_v2}_Total_Votes': v2_total,
        'EG_Total_Votes': eg_total,
        'Total_Votes': total,
        'Overall_Winner': winner,
        'Win_Percentage': round(win_pct, 1),
        f'{original_v1}_Pct_NoEG': round(v1_pct_no_eg, 1),
        f'{original_v2}_Pct_NoEG': round(v2_pct_no_eg, 1),
        'Winner_NoEG': winner_no_eg,
        'Win_Pct_NoEG': round(win_pct_no_eg, 1),
        'Binomial_P_Value': round(binom_result, 4),
        'Significance': significance,
        'Odds_Ratio': round(odds_ratio, 3) if not np.isnan(odds_ratio) else 'N/A',
        'OR_CI_Lower': round(ci_lower, 3) if not np.isnan(ci_lower) else 'N/A',
        'OR_CI_Upper': round(ci_upper, 3) if not np.isnan(ci_upper) else 'N/A',
        f'{original_v1}_Tuple_Wins': tuple_wins_v1,
        f'{original_v2}_Tuple_Wins': tuple_wins_v2,
        'Tuple_Ties': tuple_ties,
        'Total_Tuples': tuple_wins_v1 + tuple_wins_v2 + tuple_ties
    })

# Create overall dataframe and save
overall_df = pd.DataFrame(overall_aggregated)
overall_df.to_csv('preference_analysis_overall.csv', index=False)

# Print overall summary
print("\n" + "=" * 50)
print("Overall Preference Analysis (Summed Across All Tuples)")
print("=" * 50)

for _, row in overall_df.iterrows():
    metric_1 = row['Metric_1']
    metric_2 = row['Metric_2']
    m1_votes = row[f'{metric_1}_Total_Votes']
    m2_votes = row[f'{metric_2}_Total_Votes']
    m1_wins = row[f'{metric_1}_Tuple_Wins']
    m2_wins = row[f'{metric_2}_Tuple_Wins']
    m1_pct_no_eg = row[f'{metric_1}_Pct_NoEG']
    m2_pct_no_eg = row[f'{metric_2}_Pct_NoEG']
    total = row['Total_Votes']
    
    print(f"\n{row['Pair_Type']} ({metric_1} vs {metric_2}):")
    print(f"  Total votes: {total}")
    print(f"  With EG included:")
    print(f"    {metric_1}: {m1_votes} votes ({m1_votes/total*100:.1f}%)")
    print(f"    {metric_2}: {m2_votes} votes ({m2_votes/total*100:.1f}%)")
    print(f"    Equally Good: {row['EG_Total_Votes']} votes ({row['EG_Total_Votes']/total*100:.1f}%)")
    print(f"    Winner: {row['Overall_Winner']} ({row['Win_Percentage']}% of votes)")
    print(f"  Excluding EG responses:")
    print(f"    {metric_1}: {m1_pct_no_eg}%")
    print(f"    {metric_2}: {m2_pct_no_eg}%")
    print(f"    Winner: {row['Winner_NoEG']} ({row['Win_Pct_NoEG']}%) {row['Significance']}")
    print(f"    Odds ratio ({metric_1}/{metric_2}): {row['Odds_Ratio']} [95% CI: {row['OR_CI_Lower']}-{row['OR_CI_Upper']}]")
    print(f"    Binomial test p-value: {row['Binomial_P_Value']}")
    print(f"    Statistical significance: {row['Significance']} (*** p<0.001, ** p<0.01, * p<0.05, ns=not significant)")
    print(f"  Tuple-level wins: {metric_1}={m1_wins}, {metric_2}={m2_wins}, Ties={row['Tuple_Ties']}")

print(f"\nResults saved to:")
print(f"  - intermediate_long_format.csv (intermediate data)")
print(f"  - preference_analysis_per_tuple.csv (per-tuple analysis)")
print(f"  - preference_analysis_overall.csv (overall aggregated analysis)")

# Run Bradley-Terry analysis
print("\n" + "=" * 60)
print("Running Bradley-Terry Model Analysis...")
print("=" * 60)

import subprocess
import sys

try:
    # Run the Bradley-Terry analysis script
    result = subprocess.run([sys.executable, "bradley_terry_analysis.py"], 
                          capture_output=True, text=True, check=True)
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error running Bradley-Terry analysis: {e}")
    print(f"Error output: {e.stderr}")
except FileNotFoundError:
    print("bradley_terry_analysis.py not found. Please ensure it's in the same directory.")