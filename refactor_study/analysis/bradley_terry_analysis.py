import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def fit_bradley_terry(comparisons_df):
    """
    Fit Bradley-Terry model to pairwise comparison data.
    
    The Bradley-Terry model assumes that the probability of item i beating item j is:
    P(i beats j) = π_i / (π_i + π_j)
    
    where π_i is the strength parameter for item i.
    """
    
    # Get unique metrics
    metrics = ['mi', 'tokens', 'logprob']
    n_metrics = len(metrics)
    metric_to_idx = {m: i for i, m in enumerate(metrics)}
    
    # Build comparison matrix
    # wins[i][j] = number of times metric i beat metric j
    wins = np.zeros((n_metrics, n_metrics))
    totals = np.zeros((n_metrics, n_metrics))
    
    for _, row in comparisons_df.iterrows():
        if row['Actual_Choice'] in ['EG', None] or pd.isna(row['Actual_Choice']):
            continue
            
        m1 = row['Original V1 Metric']
        m2 = row['Original V2 Metric']
        choice = row['Actual_Choice']
        
        idx1 = metric_to_idx[m1]
        idx2 = metric_to_idx[m2]
        
        if choice == m1:
            wins[idx1][idx2] += 1
        elif choice == m2:
            wins[idx2][idx1] += 1
            
        totals[idx1][idx2] += 1
        totals[idx2][idx1] += 1
    
    # Maximum likelihood estimation using log-likelihood
    def neg_log_likelihood(log_params):
        """Negative log-likelihood for Bradley-Terry model"""
        # Set first parameter to 0 (reference category)
        params = np.exp(np.concatenate([[0], log_params]))
        ll = 0
        
        for i in range(n_metrics):
            for j in range(i+1, n_metrics):
                if totals[i][j] > 0:
                    # P(i beats j) = params[i] / (params[i] + params[j])
                    p_ij = params[i] / (params[i] + params[j])
                    
                    # Add log-likelihood contributions
                    if wins[i][j] > 0:
                        ll += wins[i][j] * np.log(p_ij + 1e-10)
                    if wins[j][i] > 0:
                        ll += wins[j][i] * np.log(1 - p_ij + 1e-10)
        
        return -ll
    
    # Initial guess (all equal strength)
    init_params = np.zeros(n_metrics - 1)
    
    # Optimize
    result = minimize(neg_log_likelihood, init_params, method='BFGS')
    
    # Get final parameters
    log_params_optimal = result.x
    params_optimal = np.exp(np.concatenate([[0], log_params_optimal]))
    
    # Normalize so they sum to 1 (for interpretability)
    params_normalized = params_optimal / params_optimal.sum()
    
    # Calculate standard errors using Hessian
    from scipy.optimize import approx_fprime
    
    def calc_standard_errors(log_params):
        """Calculate standard errors using numerical approximation of Hessian"""
        eps = 1e-5
        n = len(log_params)
        hessian = np.zeros((n, n))
        
        for i in range(n):
            def grad_i(x):
                return approx_fprime(x, neg_log_likelihood, eps)
            
            grad_at_param = grad_i(log_params)
            
            for j in range(n):
                x_plus = log_params.copy()
                x_plus[j] += eps
                grad_plus = grad_i(x_plus)
                
                hessian[i, j] = (grad_plus[i] - grad_at_param[i]) / eps
        
        try:
            # Covariance matrix is inverse of Hessian
            cov_matrix = np.linalg.inv(hessian)
            se = np.sqrt(np.diag(cov_matrix))
            se_full = np.concatenate([[0], se])  # Add 0 for reference category
        except:
            se_full = np.zeros(n_metrics)
        
        return se_full
    
    se = calc_standard_errors(log_params_optimal)
    
    # Create results dataframe
    results = pd.DataFrame({
        'Metric': metrics,
        'Strength': params_optimal,
        'Normalized_Strength': params_normalized,
        'Log_Strength': np.concatenate([[0], log_params_optimal]),
        'SE_Log_Strength': se,
        'Rank': stats.rankdata(-params_normalized)
    })
    
    # Calculate win probabilities matrix
    win_probs = np.zeros((n_metrics, n_metrics))
    for i in range(n_metrics):
        for j in range(n_metrics):
            if i != j:
                win_probs[i][j] = params_optimal[i] / (params_optimal[i] + params_optimal[j])
    
    win_probs_df = pd.DataFrame(win_probs, 
                                columns=metrics,
                                index=metrics)
    
    return results, win_probs_df, wins, totals

# Load the intermediate data
merged_df = pd.read_csv('intermediate_long_format.csv')

# Fit Bradley-Terry model
print("=" * 60)
print("Bradley-Terry Model Analysis")
print("=" * 60)

results, win_probs, wins_matrix, totals_matrix = fit_bradley_terry(merged_df)

print("\n1. Metric Strength Rankings:")
print("-" * 40)
results_sorted = results.sort_values('Rank')
for _, row in results_sorted.iterrows():
    ci_lower = np.exp(row['Log_Strength'] - 1.96 * row['SE_Log_Strength'])
    ci_upper = np.exp(row['Log_Strength'] + 1.96 * row['SE_Log_Strength'])
    print(f"{int(row['Rank'])}. {row['Metric']:8s}: strength = {row['Normalized_Strength']:.3f} "
          f"(raw: {row['Strength']:.3f}, 95% CI: [{ci_lower:.3f}, {ci_upper:.3f}])")

print("\n2. Pairwise Win Probabilities:")
print("-" * 40)
print("P(row beats column):")
print(win_probs.round(3).to_string())

print("\n3. Observed vs Expected Comparisons:")
print("-" * 40)
metrics = ['mi', 'tokens', 'logprob']
for i, m1 in enumerate(metrics):
    for j, m2 in enumerate(metrics):
        if i < j:
            observed_m1_wins = wins_matrix[i][j]
            observed_m2_wins = wins_matrix[j][i]
            total = observed_m1_wins + observed_m2_wins
            if total > 0:
                expected_m1_wins = win_probs.iloc[i, j] * total
                expected_m2_wins = win_probs.iloc[j, i] * total
                print(f"{m1} vs {m2}:")
                print(f"  Observed: {m1}={int(observed_m1_wins)}, {m2}={int(observed_m2_wins)}")
                print(f"  Expected: {m1}={expected_m1_wins:.1f}, {m2}={expected_m2_wins:.1f}")
                print(f"  P({m1} beats {m2}) = {win_probs.iloc[i, j]:.3f}")

# Model fit statistics
print("\n4. Model Fit Statistics:")
print("-" * 40)

# Calculate deviance (goodness of fit)
deviance = 0
for i in range(len(metrics)):
    for j in range(i+1, len(metrics)):
        if totals_matrix[i][j] > 0:
            n_ij = totals_matrix[i][j]
            w_ij = wins_matrix[i][j]
            w_ji = wins_matrix[j][i]
            p_ij = win_probs.iloc[i, j]
            
            if w_ij > 0:
                deviance += 2 * w_ij * np.log(w_ij / (n_ij * p_ij + 1e-10))
            if w_ji > 0:
                deviance += 2 * w_ji * np.log(w_ji / (n_ij * (1-p_ij) + 1e-10))

df = (len(metrics) * (len(metrics) - 1)) // 2 - (len(metrics) - 1)
p_value = 1 - stats.chi2.cdf(deviance, df) if df > 0 else 1.0

print(f"Deviance: {deviance:.2f}")
print(f"Degrees of freedom: {df}")
print(f"p-value: {p_value:.4f}")

if p_value > 0.05:
    print("Model fits well (p > 0.05)")
else:
    print("Model may not fit perfectly (p < 0.05)")

# Save results
results.to_csv('bradley_terry_results.csv', index=False)
win_probs.to_csv('bradley_terry_win_probabilities.csv')

print(f"\n5. Interpretation:")
print("-" * 40)
best_metric = results_sorted.iloc[0]['Metric']
print(f"Based on the Bradley-Terry model, '{best_metric}' is the strongest metric overall.")
print(f"It has a {results_sorted.iloc[0]['Normalized_Strength']*100:.1f}% relative strength.")

# Calculate relative odds
for i in range(1, len(results_sorted)):
    ratio = results_sorted.iloc[0]['Strength'] / results_sorted.iloc[i]['Strength']
    print(f"'{best_metric}' is {ratio:.2f}x stronger than '{results_sorted.iloc[i]['Metric']}'")

print("\nResults saved to:")
print("  - bradley_terry_results.csv")
print("  - bradley_terry_win_probabilities.csv")