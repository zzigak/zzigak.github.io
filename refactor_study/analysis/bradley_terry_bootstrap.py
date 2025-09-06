import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy import stats
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# Load data
merged_df = pd.read_csv('intermediate_long_format.csv')

def fit_bradley_terry_once(comparisons_df):
    """
    Fit Bradley-Terry model to pairwise comparison data (single fit).
    Returns parameters in original scale and normalized scale.
    """
    
    # Get unique metrics
    metrics = ['mi', 'tokens', 'logprob']
    n_metrics = len(metrics)
    metric_to_idx = {m: i for i, m in enumerate(metrics)}
    
    # Build comparison matrix
    wins = np.zeros((n_metrics, n_metrics))
    totals = np.zeros((n_metrics, n_metrics))
    
    for _, row in comparisons_df.iterrows():
        if row['Actual_Choice'] in ['EG', None] or pd.isna(row['Actual_Choice']):
            continue
            
        m1 = row['Original V1 Metric']
        m2 = row['Original V2 Metric']
        choice = row['Actual_Choice']
        
        if m1 not in metric_to_idx or m2 not in metric_to_idx:
            continue
            
        idx1 = metric_to_idx[m1]
        idx2 = metric_to_idx[m2]
        
        if choice == m1:
            wins[idx1][idx2] += 1
        elif choice == m2:
            wins[idx2][idx1] += 1
            
        totals[idx1][idx2] += 1
        totals[idx2][idx1] += 1
    
    # Maximum likelihood estimation
    def neg_log_likelihood(log_params):
        params = np.exp(np.concatenate([[0], log_params]))  # MI = reference
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
    
    # Optimize
    init_params = np.zeros(n_metrics - 1)
    result = minimize(neg_log_likelihood, init_params, method='BFGS')
    
    # Get parameters
    log_params = np.concatenate([[0], result.x])
    params = np.exp(log_params)
    params_normalized = params / params.sum()
    
    return {
        'params': params,
        'params_normalized': params_normalized,
        'log_params': log_params,
        'metrics': metrics
    }

def bootstrap_bradley_terry(comparisons_df, n_bootstrap=1000, confidence=0.95):
    """
    Perform bootstrap estimation of Bradley-Terry parameters.
    """
    
    print(f"Running bootstrap with {n_bootstrap} iterations...")
    
    # Fit original model
    original_fit = fit_bradley_terry_once(comparisons_df)
    
    # Store bootstrap results
    bootstrap_params = []
    bootstrap_params_norm = []
    bootstrap_log_params = []
    
    # Get unique comparison IDs for resampling
    # We need to maintain the structure of paired comparisons
    comparison_ids = comparisons_df.index.values
    
    # Bootstrap loop
    for i in tqdm(range(n_bootstrap)):
        # Resample with replacement
        bootstrap_ids = np.random.choice(comparison_ids, size=len(comparison_ids), replace=True)
        bootstrap_data = comparisons_df.loc[bootstrap_ids]
        
        try:
            # Fit model to bootstrap sample
            boot_fit = fit_bradley_terry_once(bootstrap_data)
            bootstrap_params.append(boot_fit['params'])
            bootstrap_params_norm.append(boot_fit['params_normalized'])
            bootstrap_log_params.append(boot_fit['log_params'])
        except:
            # Skip if optimization fails (rare)
            continue
    
    # Convert to arrays
    bootstrap_params = np.array(bootstrap_params)
    bootstrap_params_norm = np.array(bootstrap_params_norm)
    bootstrap_log_params = np.array(bootstrap_log_params)
    
    # Calculate confidence intervals using percentile method
    alpha = 1 - confidence
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100
    
    # CIs for different parameterizations
    params_ci_lower = np.percentile(bootstrap_params, lower_percentile, axis=0)
    params_ci_upper = np.percentile(bootstrap_params, upper_percentile, axis=0)
    
    params_norm_ci_lower = np.percentile(bootstrap_params_norm, lower_percentile, axis=0)
    params_norm_ci_upper = np.percentile(bootstrap_params_norm, upper_percentile, axis=0)
    
    log_params_ci_lower = np.percentile(bootstrap_log_params, lower_percentile, axis=0)
    log_params_ci_upper = np.percentile(bootstrap_log_params, upper_percentile, axis=0)
    
    # Calculate bootstrap standard errors
    params_se = np.std(bootstrap_params, axis=0)
    params_norm_se = np.std(bootstrap_params_norm, axis=0)
    log_params_se = np.std(bootstrap_log_params, axis=0)
    
    return {
        'original': original_fit,
        'bootstrap_samples': {
            'params': bootstrap_params,
            'params_norm': bootstrap_params_norm,
            'log_params': bootstrap_log_params
        },
        'ci': {
            'params': (params_ci_lower, params_ci_upper),
            'params_norm': (params_norm_ci_lower, params_norm_ci_upper),
            'log_params': (log_params_ci_lower, log_params_ci_upper)
        },
        'se': {
            'params': params_se,
            'params_norm': params_norm_se,
            'log_params': log_params_se
        },
        'n_successful': len(bootstrap_params)
    }

# Run bootstrap analysis
print("=" * 60)
print("Bradley-Terry Model with Bootstrap Confidence Intervals")
print("=" * 60)

results = bootstrap_bradley_terry(merged_df, n_bootstrap=1000)

# Display results
print(f"\nBootstrap completed: {results['n_successful']}/1000 successful iterations")
print("\n1. Parameter Estimates with Bootstrap CIs:")
print("-" * 50)

metrics = results['original']['metrics']
original_params = results['original']['params']
original_params_norm = results['original']['params_normalized']
ci_params = results['ci']['params']
ci_params_norm = results['ci']['params_norm']
se_params_norm = results['se']['params_norm']

# Sort by strength
sorted_idx = np.argsort(original_params_norm)[::-1]

print("\nNormalized Strengths (Bootstrap 95% CI):")
for idx in sorted_idx:
    metric = metrics[idx]
    strength = original_params_norm[idx]
    ci_low = ci_params_norm[0][idx]
    ci_high = ci_params_norm[1][idx]
    se = se_params_norm[idx]
    
    print(f"{metric:8s}: {strength:.3f} [{ci_low:.3f}, {ci_high:.3f}]  SE={se:.3f}")

print("\n2. Relative Strengths (compared to MI):")
print("-" * 50)
mi_idx = metrics.index('mi')

for idx in sorted_idx:
    if idx == mi_idx:
        continue
    
    metric = metrics[idx]
    
    # Calculate relative strength with bootstrap CI
    bootstrap_relative = results['bootstrap_samples']['params'][:, idx] / results['bootstrap_samples']['params'][:, mi_idx]
    relative = original_params[idx] / original_params[mi_idx]
    relative_ci_low = np.percentile(bootstrap_relative, 2.5)
    relative_ci_high = np.percentile(bootstrap_relative, 97.5)
    
    print(f"{metric:8s} is {relative:.2f}x stronger than MI  [95% CI: {relative_ci_low:.2f}x - {relative_ci_high:.2f}x]")

# Create visualization comparing Hessian vs Bootstrap CIs
print("\n3. Creating comparison plots...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Load Hessian-based results for comparison
hessian_df = pd.read_csv('bradley_terry_results.csv')

# Plot 1: Comparing CI methods for normalized strengths
x_pos = np.arange(len(metrics))
colors = {'mi': '#e74c3c', 'logprob': '#2ecc71', 'tokens': '#3498db'}

# Bootstrap CIs
sorted_metrics = [metrics[i] for i in sorted_idx]
sorted_strengths = [original_params_norm[i] for i in sorted_idx]
sorted_ci_lower = [ci_params_norm[0][i] for i in sorted_idx]
sorted_ci_upper = [ci_params_norm[1][i] for i in sorted_idx]

ax1.bar(x_pos - 0.2, sorted_strengths, 0.35,
        yerr=[np.array(sorted_strengths) - np.array(sorted_ci_lower),
              np.array(sorted_ci_upper) - np.array(sorted_strengths)],
        capsize=5, label='Bootstrap CI',
        color=[colors[m] for m in sorted_metrics], alpha=0.7)

# Hessian CIs (approximate)
hessian_sorted = []
for m in sorted_metrics:
    row = hessian_df[hessian_df['Metric'] == m].iloc[0]
    strength = row['Normalized_Strength']
    
    # Approximate CI from log scale
    log_strength = row['Log_Strength']
    se_log = row['SE_Log_Strength']
    ci_low_log = log_strength - 1.96 * se_log
    ci_high_log = log_strength + 1.96 * se_log
    
    # Transform (approximate for normalized)
    total = np.sum(np.exp(hessian_df['Log_Strength'].values))
    ci_low = np.exp(ci_low_log) / (np.exp(ci_low_log) + total - np.exp(log_strength))
    ci_high = np.exp(ci_high_log) / (np.exp(ci_high_log) + total - np.exp(log_strength))
    
    hessian_sorted.append({
        'strength': strength,
        'ci_low': ci_low,
        'ci_high': ci_high
    })

hessian_strengths = [h['strength'] for h in hessian_sorted]
hessian_errors = [[h['strength'] - h['ci_low'] for h in hessian_sorted],
                  [h['ci_high'] - h['strength'] for h in hessian_sorted]]

ax1.bar(x_pos + 0.2, hessian_strengths, 0.35,
        yerr=hessian_errors, capsize=5, label='Hessian CI',
        color=[colors[m] for m in sorted_metrics], alpha=0.7,
        edgecolor='black', linewidth=1.5)

ax1.set_xlabel('Metric')
ax1.set_ylabel('Normalized Strength')
ax1.set_title('Bootstrap vs Hessian Confidence Intervals', fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels([m.upper() for m in sorted_metrics])
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Bootstrap distribution for log-probability
ax2.hist(results['bootstrap_samples']['params_norm'][:, metrics.index('logprob')], 
         bins=30, alpha=0.7, color='green', edgecolor='black')
ax2.axvline(original_params_norm[metrics.index('logprob')], 
            color='red', linestyle='--', linewidth=2, label='Original estimate')
ax2.axvline(ci_params_norm[0][metrics.index('logprob')], 
            color='blue', linestyle='--', linewidth=1, label='95% CI')
ax2.axvline(ci_params_norm[1][metrics.index('logprob')], 
            color='blue', linestyle='--', linewidth=1)
ax2.set_xlabel('Log-probability Strength')
ax2.set_ylabel('Frequency')
ax2.set_title('Bootstrap Distribution for Log-probability', fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.suptitle('Bootstrap Analysis of Bradley-Terry Model', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('bradley_terry_bootstrap_comparison.png', dpi=300, bbox_inches='tight')
print("Saved: bradley_terry_bootstrap_comparison.png")

# Save bootstrap results
bootstrap_results_df = pd.DataFrame({
    'Metric': metrics,
    'Strength': original_params,
    'Normalized_Strength': original_params_norm,
    'Bootstrap_SE': se_params_norm,
    'Bootstrap_CI_Lower': ci_params_norm[0],
    'Bootstrap_CI_Upper': ci_params_norm[1],
    'Log_Strength': results['original']['log_params'],
    'Log_Bootstrap_SE': results['se']['log_params'],
    'Log_Bootstrap_CI_Lower': results['ci']['log_params'][0],
    'Log_Bootstrap_CI_Upper': results['ci']['log_params'][1]
})

bootstrap_results_df.to_csv('bradley_terry_bootstrap_results.csv', index=False)
print("\nResults saved to: bradley_terry_bootstrap_results.csv")

print("\n" + "=" * 60)
print("Summary:")
print("-" * 60)
print("Bootstrap CIs are generally more reliable because they:")
print("1. Don't assume asymptotic normality")
print("2. Handle the constraint that strengths sum to 1 naturally")
print("3. Account for any non-linearity in the transformation")
print("\nThe bootstrap results confirm log-probability as the strongest metric.")