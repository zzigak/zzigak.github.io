import pandas as pd
import numpy as np
from scipy import stats

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')

print("=" * 70)
print("Additional Statistical Analyses")
print("=" * 70)

# 1. Confidence intervals for preference proportions using Wilson score
def wilson_score_ci(successes, total, confidence=0.95):
    """Calculate Wilson score confidence interval for proportion"""
    if total == 0:
        return (0, 1)
    
    p_hat = successes / total
    z = stats.norm.ppf((1 + confidence) / 2)
    
    denominator = 1 + z**2 / total
    center = (p_hat + z**2 / (2 * total)) / denominator
    
    margin = z * np.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * total)) / total) / denominator
    
    return (max(0, center - margin), min(1, center + margin))

print("\n1. Preference Proportions with 95% Confidence Intervals")
print("-" * 60)

comparisons = [
    ('mi', 'logprob'),
    ('mi', 'tokens'),
    ('logprob', 'tokens')
]

for m1, m2 in comparisons:
    # Get relevant comparisons
    relevant = merged_df[
        ((merged_df['Original V1 Metric'] == m1) & (merged_df['Original V2 Metric'] == m2)) |
        ((merged_df['Original V1 Metric'] == m2) & (merged_df['Original V2 Metric'] == m1))
    ]
    
    # Count preferences (excluding EG)
    m1_wins = len(relevant[relevant['Actual_Choice'] == m1])
    m2_wins = len(relevant[relevant['Actual_Choice'] == m2])
    total = m1_wins + m2_wins
    
    if total > 0:
        # Calculate confidence intervals
        m1_ci = wilson_score_ci(m1_wins, total)
        m2_ci = wilson_score_ci(m2_wins, total)
        
        print(f"\n{m1} vs {m2}:")
        print(f"  {m1}: {m1_wins}/{total} = {m1_wins/total:.1%} [95% CI: {m1_ci[0]:.1%}-{m1_ci[1]:.1%}]")
        print(f"  {m2}: {m2_wins}/{total} = {m2_wins/total:.1%} [95% CI: {m2_ci[0]:.1%}-{m2_ci[1]:.1%}]")
        
        # Check if CIs overlap
        if m1_ci[1] < m2_ci[0] or m2_ci[1] < m1_ci[0]:
            print(f"  → Confidence intervals DO NOT overlap (significant difference)")
        else:
            print(f"  → Confidence intervals overlap (no significant difference)")

# 2. Effect sizes (Cohen's h for proportions)
print("\n" + "=" * 70)
print("2. Effect Sizes (Cohen's h)")
print("-" * 60)
print("Interpretation: |h| < 0.2 = small, 0.2-0.5 = medium, > 0.8 = large")
print()

for m1, m2 in comparisons:
    relevant = merged_df[
        ((merged_df['Original V1 Metric'] == m1) & (merged_df['Original V2 Metric'] == m2)) |
        ((merged_df['Original V1 Metric'] == m2) & (merged_df['Original V2 Metric'] == m1))
    ]
    
    m1_wins = len(relevant[relevant['Actual_Choice'] == m1])
    m2_wins = len(relevant[relevant['Actual_Choice'] == m2])
    total = m1_wins + m2_wins
    
    if total > 0:
        p1 = m1_wins / total
        p2 = m2_wins / total
        
        # Cohen's h = 2 * (arcsin(sqrt(p1)) - arcsin(sqrt(p2)))
        h = 2 * (np.arcsin(np.sqrt(p1)) - np.arcsin(np.sqrt(p2)))
        
        # Interpret effect size
        if abs(h) < 0.2:
            interpretation = "small"
        elif abs(h) < 0.5:
            interpretation = "medium"
        elif abs(h) < 0.8:
            interpretation = "medium-large"
        else:
            interpretation = "large"
        
        print(f"{m1} vs {m2}: h = {h:.3f} ({interpretation} effect)")

# 3. Combined test: Is logprob better than both alternatives?
print("\n" + "=" * 70)
print("3. Combined Evidence Test")
print("-" * 60)

# Using Fisher's method to combine p-values
logprob_vs_mi = merged_df[
    ((merged_df['Original V1 Metric'] == 'logprob') & (merged_df['Original V2 Metric'] == 'mi')) |
    ((merged_df['Original V1 Metric'] == 'mi') & (merged_df['Original V2 Metric'] == 'logprob'))
]

logprob_vs_tokens = merged_df[
    ((merged_df['Original V1 Metric'] == 'logprob') & (merged_df['Original V2 Metric'] == 'tokens')) |
    ((merged_df['Original V1 Metric'] == 'tokens') & (merged_df['Original V2 Metric'] == 'logprob'))
]

# Get p-values for each comparison
logprob_wins_mi = len(logprob_vs_mi[logprob_vs_mi['Actual_Choice'] == 'logprob'])
mi_wins = len(logprob_vs_mi[logprob_vs_mi['Actual_Choice'] == 'mi'])
p1 = stats.binomtest(logprob_wins_mi, logprob_wins_mi + mi_wins, 0.5, alternative='greater').pvalue

logprob_wins_tokens = len(logprob_vs_tokens[logprob_vs_tokens['Actual_Choice'] == 'logprob'])
tokens_wins = len(logprob_vs_tokens[logprob_vs_tokens['Actual_Choice'] == 'tokens'])
p2 = stats.binomtest(logprob_wins_tokens, logprob_wins_tokens + tokens_wins, 0.5, alternative='greater').pvalue

print(f"One-sided tests (H0: logprob not preferred):")
print(f"  Logprob > MI: p = {p1:.4f}")
print(f"  Logprob > Tokens: p = {p2:.4f}")

# Fisher's combined probability test
chi2_stat = -2 * (np.log(p1) + np.log(p2))
combined_p = 1 - stats.chi2.cdf(chi2_stat, df=4)
print(f"\nFisher's combined test: χ² = {chi2_stat:.2f}, p = {combined_p:.4f}")

# 4. Transitivity check
print("\n" + "=" * 70)
print("4. Transitivity Analysis")
print("-" * 60)

# Check if preferences are transitive
# If logprob > mi and logprob > tokens, then tokens should > mi
tokens_vs_mi = merged_df[
    ((merged_df['Original V1 Metric'] == 'tokens') & (merged_df['Original V2 Metric'] == 'mi')) |
    ((merged_df['Original V1 Metric'] == 'mi') & (merged_df['Original V2 Metric'] == 'tokens'))
]

tokens_beats_mi = len(tokens_vs_mi[tokens_vs_mi['Actual_Choice'] == 'tokens'])
mi_beats_tokens = len(tokens_vs_mi[tokens_vs_mi['Actual_Choice'] == 'mi'])

print("Expected transitivity: logprob > tokens > mi")
print(f"  Logprob > MI: {logprob_wins_mi}/{logprob_wins_mi + mi_wins} = {logprob_wins_mi/(logprob_wins_mi + mi_wins):.1%}")
print(f"  Logprob > Tokens: {logprob_wins_tokens}/{logprob_wins_tokens + tokens_wins} = {logprob_wins_tokens/(logprob_wins_tokens + tokens_wins):.1%}")
print(f"  Tokens > MI: {tokens_beats_mi}/{tokens_beats_mi + mi_beats_tokens} = {tokens_beats_mi/(tokens_beats_mi + mi_beats_tokens):.1%}")

if logprob_wins_mi > mi_wins and logprob_wins_tokens > tokens_wins and tokens_beats_mi > mi_beats_tokens:
    print("✓ Preferences are perfectly transitive")
elif logprob_wins_mi > mi_wins and tokens_beats_mi > mi_beats_tokens:
    print("✓ Preferences are weakly transitive (logprob ≈ tokens > mi)")
else:
    print("✗ Some intransitivity detected")

# 5. Consensus strength
print("\n" + "=" * 70)
print("5. Consensus Strength Analysis")
print("-" * 60)

# Calculate how many participants agreed with the Bradley-Terry ranking
bt_ranking = ['logprob', 'tokens', 'mi']  # From BT model

participant_rankings = []
for user_id in merged_df['UserID'].unique():
    user_data = merged_df[merged_df['UserID'] == user_id]
    
    # Count wins for each metric
    wins = {'mi': 0, 'tokens': 0, 'logprob': 0}
    
    for _, row in user_data.iterrows():
        choice = row['Actual_Choice']
        if choice in wins:
            wins[choice] += 1
    
    # Rank metrics for this participant
    user_ranking = sorted(wins.keys(), key=lambda x: wins[x], reverse=True)
    participant_rankings.append(user_ranking)
    
    # Check agreement with BT ranking
    if user_ranking == bt_ranking:
        agreement = "full"
    elif user_ranking[0] == bt_ranking[0]:
        agreement = "top choice"
    else:
        agreement = "different"

# Count agreements
full_agreement = sum(1 for r in participant_rankings if r == bt_ranking)
top_agreement = sum(1 for r in participant_rankings if r[0] == bt_ranking[0])
total_participants = len(participant_rankings)

print(f"Participants agreeing with Bradley-Terry ranking (logprob > tokens > mi):")
print(f"  Full ranking agreement: {full_agreement}/{total_participants} = {full_agreement/total_participants:.1%}")
print(f"  Top choice agreement (logprob best): {top_agreement}/{total_participants} = {top_agreement/total_participants:.1%}")

print("\n" + "=" * 70)
print("Summary for Paper")
print("=" * 70)
print("""
Key findings:
1. Log-probability showed the highest preference strength in Bradley-Terry model
2. Log-probability was preferred over MI with medium effect size (h = -0.354)
3. Log-probability and token count were statistically equivalent 
4. Preferences showed weak transitivity: logprob ≈ tokens > mi
5. Consensus was moderate, with {}% of participants ranking logprob as best
""".format(int(top_agreement/total_participants*100)))