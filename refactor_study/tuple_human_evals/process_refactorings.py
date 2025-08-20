import os
import subprocess
import json
import tempfile
import re
import ast
import tokenize
from io import StringIO

def run_radon(command, filepath):
    result = subprocess.run(
        command + [filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout

def extract_mi(mi_out, fpath):
    if not mi_out.strip():
        return 0.0
    try:
        mi_json = json.loads(mi_out)
        for key, value in mi_json.items():
            if isinstance(value, dict) and "mi" in value:
                return float(value["mi"])
            elif isinstance(value, (int, float)):
                return float(value)
        mi_val = mi_json.get(fpath, 0)
        if isinstance(mi_val, dict):
            mi_val = mi_val.get("mi", 0)
        return float(mi_val)
    except json.JSONDecodeError:
        lines = mi_out.strip().split('\n')
        for line in lines:
            if 'mi' in line.lower():
                numbers = re.findall(r'[\d.]+', line)
                if numbers:
                    return float(numbers[0])
    except Exception:
        pass
    return 0.0

def count_tokens(code):
    """Count tokens in Python code using the tokenize module."""
    try:
        # Use StringIO to create a file-like object from the string
        from io import StringIO
        tokens = list(tokenize.generate_tokens(StringIO(code).readline))
        # Filter out comments, whitespace, and newlines
        meaningful_tokens = [t for t in tokens if t.type not in [tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT]]
        return len(meaningful_tokens)
    except Exception as e:
        print(f"Token counting error: {e}")
        return 0

def calculate_cyclomatic_complexity(code):
    """Calculate cyclomatic complexity using AST analysis."""
    try:
        tree = ast.parse(code)
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.AsyncWith, ast.With)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            elif isinstance(node, ast.Assert):
                complexity += 1
            elif isinstance(node, ast.Return):
                complexity += 1
            elif isinstance(node, ast.Raise):
                complexity += 1
            elif isinstance(node, ast.Try):
                complexity += 1
                
        return complexity
    except Exception:
        return 1

def read_logprob_from_metrics(metrics_path):
    if not os.path.isfile(metrics_path):
        return None
    try:
        with open(metrics_path, 'r') as f:
            for line in f:
                if 'Total LogProb:' in line:
                    return float(line.split(':', 1)[1].strip())
    except Exception:
        pass
    return None

def read_pass_rates(chosen_refactoring_path):
    """Read pass rates from chosen_refactoring.txt file."""
    if not os.path.isfile(chosen_refactoring_path):
        return None
    
    try:
        with open(chosen_refactoring_path, 'r') as f:
            content = f.read()
            
        # Extract pass rates for each refactoring
        pass_rates = {}
        lines = content.strip().split('\n')
        
        for line in lines:
            if line.startswith('Refactoring') and 'Mean Pass Rate Before:' in line:
                # Parse: "Refactoring X: Total Loss: Y, Mean Pass Rate Before: Z, Mean Pass Rate After: W"
                try:
                    # Extract refactoring number
                    refac_part = line.split(':')[0]
                    refac_num = int(refac_part.split()[1])
                    
                    # Extract pass rates using regex
                    before_match = re.search(r'Mean Pass Rate Before: ([\d.]+)', line)
                    after_match = re.search(r'Mean Pass Rate After: ([\d.]+)', line)
                    
                    if before_match and after_match:
                        before_rate = float(before_match.group(1))
                        after_rate = float(after_match.group(1))
                        
                        pass_rates[refac_num] = {
                            'before': before_rate,
                            'after': after_rate,
                            'maintained': after_rate >= before_rate  # Check if rates are maintained or improved
                        }
                except (ValueError, IndexError) as e:
                    # Skip lines that can't be parsed
                    continue
        
        return pass_rates
    except Exception as e:
        print(f"Error reading pass rates from {chosen_refactoring_path}: {e}")
        return None

def process_cluster(cluster_path, cluster_name):
    print(f"Processing {cluster_name}...")
    tuple_dirs = sorted(
        [(d, os.path.join(cluster_path, d)) for d in os.listdir(cluster_path)
         if os.path.isdir(os.path.join(cluster_path, d)) and d.startswith("tuple_")]
    )

    cluster_results = []

    for tuple_name, tuple_path in tuple_dirs:
        print(f"  Processing {tuple_name}...")
        refac_dirs = sorted(
            [(d, os.path.join(tuple_path, d)) for d in os.listdir(tuple_path)
             if os.path.isdir(os.path.join(tuple_path, d)) and d.startswith("refactoring_")]
        )

        tuple_results = []

        for refac_name, refac_path in refac_dirs:
            # Gather relevant Python files
            py_files = [f for f in os.listdir(refac_path)
                        if f == "library_helpers.py" or f.endswith("_refactored.py")]
            if not py_files:
                continue

            concatenated_code = ""
            for fname in py_files:
                try:
                    with open(os.path.join(refac_path, fname), 'r') as f:
                        concatenated_code += f.read() + '\n'
                except Exception:
                    continue

            if not concatenated_code.strip():
                continue

            # Write to temp file and run Radon
            with tempfile.NamedTemporaryFile('w+', suffix='.py', delete=False) as tmpf:
                tmpf.write(concatenated_code)
                tmpf_path = tmpf.name

            try:
                mi_out = run_radon(["radon", "mi", "-j"], tmpf_path)
                mi_value = extract_mi(mi_out, tmpf_path)
                
                # Calculate additional metrics
                token_count = count_tokens(concatenated_code)
                cc_value = calculate_cyclomatic_complexity(concatenated_code)
                
            except Exception as e:
                mi_value = 0.0
                token_count = 0
                cc_value = 1
            finally:
                os.remove(tmpf_path)

            logprob = read_logprob_from_metrics(os.path.join(refac_path, "metrics.txt"))
            
            # Read pass rates from chosen_refactoring.txt
            chosen_refactoring_path = os.path.join(tuple_path, "chosen_refactoring.txt")
            pass_rates = read_pass_rates(chosen_refactoring_path)
            
            # Extract refactoring number from name (e.g., "refactoring_1" -> 1)
            refac_num = int(refac_name.split('_')[1]) if '_' in refac_name else 0
            
            if logprob is not None:
                result = {
                    'refactoring': refac_name,
                    'logprob': logprob,
                    'mi': mi_value,
                    'tokens': token_count,
                    'cc': cc_value
                }
                
                # Add pass rate information if available
                if pass_rates and refac_num in pass_rates:
                    result.update({
                        'pass_rate_before': pass_rates[refac_num]['before'],
                        'pass_rate_after': pass_rates[refac_num]['after'],
                        'pass_rate_maintained': pass_rates[refac_num]['maintained']
                    })
                else:
                    result.update({
                        'pass_rate_before': None,
                        'pass_rate_after': None,
                        'pass_rate_maintained': None
                    })
                
                tuple_results.append(result)

        if tuple_results:
            # --- Rank MI: higher is better ---
            mi_values = [r['mi'] for r in tuple_results]
            mi_sorted = sorted(range(len(mi_values)), key=lambda i: mi_values[i], reverse=True)
            mi_ranks = [0] * len(mi_values)
            for rank, idx in enumerate(mi_sorted):
                mi_ranks[idx] = rank + 1

            # --- Rank LogProb: higher (closer to 0 or positive) is better ---
            logprob_values = [r['logprob'] for r in tuple_results]
            logprob_sorted = sorted(range(len(logprob_values)), key=lambda i: logprob_values[i], reverse=True)
            logprob_ranks = [0] * len(logprob_values)
            for rank, idx in enumerate(logprob_sorted):
                logprob_ranks[idx] = rank + 1

            # --- Rank Tokens: lower is better (shorter code) ---
            token_values = [r['tokens'] for r in tuple_results]
            token_sorted = sorted(range(len(token_values)), key=lambda i: token_values[i])
            token_ranks = [0] * len(token_values)
            for rank, idx in enumerate(token_sorted):
                token_ranks[idx] = rank + 1

            # --- Rank CC: lower is better (less complex) ---
            cc_values = [r['cc'] for r in tuple_results]
            cc_sorted = sorted(range(len(cc_values)), key=lambda i: cc_values[i])
            cc_ranks = [0] * len(cc_values)
            for rank, idx in enumerate(cc_sorted):
                cc_ranks[idx] = rank + 1

            # Attach ranks
            for i, result in enumerate(tuple_results):
                result['mi_rank'] = mi_ranks[i]
                result['logprob_rank'] = logprob_ranks[i]
                result['token_rank'] = token_ranks[i]
                result['cc_rank'] = cc_ranks[i]

            # Sort by logprob rank for display
            tuple_results.sort(key=lambda x: x['logprob_rank'])

            cluster_results.append({
                'tuple': tuple_name,
                'results': tuple_results
            })

    # Write output files (both JSON and TXT)
    json_output_path = os.path.join(cluster_path, f"{cluster_name}_rankings.json")
    txt_output_path = os.path.join(cluster_path, f"{cluster_name}_rankings.txt")
    
    # Prepare data for JSON output
    json_data = {
        'cluster': cluster_name,
        'tuples': []
    }
    
    for tup in cluster_results:
            tuple_data = {
                'tuple_name': tup['tuple'],
                'refactorings': []
            }
            
            for r in tup['results']:
                refactoring_data = {
                    'name': r['refactoring'],
                    'metrics': {
                        'mi': r['mi'],
                        'logprob': r['logprob'],
                        'tokens': r['tokens'],
                        'cc': r['cc']
                    },
                    'ranks': {
                        'mi_rank': r['mi_rank'],
                        'logprob_rank': r['logprob_rank'],
                        'token_rank': r['token_rank'],
                        'cc_rank': r['cc_rank']
                    },
                    'pass_rates': {
                        'before': r['pass_rate_before'],
                        'after': r['pass_rate_after'],
                        'maintained': r['pass_rate_maintained']
                    }
                }
                tuple_data['refactorings'].append(refactoring_data)
            
            # Add top refactorings analysis
            passed_refactorings = [r for r in tup['results'] if r['pass_rate_maintained'] is True]
            
            # Top performers overall
            top_mi = min(tup['results'], key=lambda x: x['mi_rank'])
            top_logprob = min(tup['results'], key=lambda x: x['logprob_rank'])
            top_tokens = min(tup['results'], key=lambda x: x['token_rank'])
            top_cc = min(tup['results'], key=lambda x: x['cc_rank'])
            
            tuple_data['top_refactorings_overall'] = {
                'mi': {
                    'name': top_mi['refactoring'],
                    'rank': top_mi['mi_rank'],
                    'score': top_mi['mi']
                },
                'logprob': {
                    'name': top_logprob['refactoring'],
                    'rank': top_logprob['logprob_rank'],
                    'score': top_logprob['logprob']
                },
                'tokens': {
                    'name': top_tokens['refactoring'],
                    'rank': top_tokens['token_rank'],
                    'score': top_tokens['tokens']
                },
                'cc': {
                    'name': top_cc['refactoring'],
                    'rank': top_cc['cc_rank'],
                    'score': top_cc['cc']
                }
            }
            
            # Top performers among passed refactorings
            if passed_refactorings:
                top_mi_passed = min(passed_refactorings, key=lambda x: x['mi_rank'])
                top_logprob_passed = min(passed_refactorings, key=lambda x: x['logprob_rank'])
                top_tokens_passed = min(passed_refactorings, key=lambda x: x['token_rank'])
                top_cc_passed = min(passed_refactorings, key=lambda x: x['cc_rank'])
                
                tuple_data['top_refactorings_passed'] = {
                    'mi': {
                        'name': top_mi_passed['refactoring'],
                        'rank': top_mi_passed['mi_rank'],
                        'score': top_mi_passed['mi']
                    },
                    'logprob': {
                        'name': top_logprob_passed['refactoring'],
                        'rank': top_logprob_passed['logprob_rank'],
                        'score': top_logprob_passed['logprob']
                    },
                    'tokens': {
                        'name': top_tokens_passed['refactoring'],
                        'rank': top_tokens_passed['token_rank'],
                        'score': top_tokens_passed['tokens']
                    },
                    'cc': {
                        'name': top_cc_passed['refactoring'],
                        'rank': top_cc_passed['cc_rank'],
                        'score': top_cc_passed['cc']
                    }
                }
            else:
                tuple_data['top_refactorings_passed'] = None
            
            json_data['tuples'].append(tuple_data)
    
    # Save JSON file
    with open(json_output_path, 'w') as f:
        json.dump(json_data, f, indent=2)
    
    # Save TXT file with both all refactorings and passed-only rankings
    with open(txt_output_path, 'w') as f:
        f.write(f"Cluster: {cluster_name}\n")
        f.write("=" * 80 + "\n\n")
        
        for tup in cluster_results:
            f.write(f"Tuple: {tup['tuple']}\n")
            f.write("-" * 80 + "\n")
            
            # Section 1: All Refactorings
            f.write("ALL REFACTORINGS:\n")
            f.write(f"{'Name':<15} {'MI':<8} {'LogProb':<10} {'Tokens':<8} {'CC':<6} {'PassBefore':<10} {'PassAfter':<10} {'Maintained':<10}\n")
            f.write("-" * 80 + "\n")
            for r in tup['results']:
                maintained_str = "Yes" if r['pass_rate_maintained'] else "No" if r['pass_rate_maintained'] is not None else "N/A"
                pass_before = f"{r['pass_rate_before']:.3f}" if r['pass_rate_before'] is not None else "N/A"
                pass_after = f"{r['pass_rate_after']:.3f}" if r['pass_rate_after'] is not None else "N/A"
                
                f.write(f"{r['refactoring']:<15} {r['mi']:<8.3f} {r['logprob']:<10.1f} {r['tokens']:<8} {r['cc']:<6} "
                        f"{pass_before:<10} {pass_after:<10} {maintained_str:<10}\n")
            
            # Section 2: Only Refactorings that Maintained Pass Rates
            f.write("\nREFACTORINGS THAT MAINTAINED PASS RATES:\n")
            passed_refactorings = [r for r in tup['results'] if r['pass_rate_maintained'] is True]
            
            if passed_refactorings:
                f.write(f"{'Name':<15} {'MI_Rank':<8} {'LogProb_Rank':<12} {'Token_Rank':<11} {'CC_Rank':<8} {'MI':<8} {'LogProb':<10}\n")
                f.write("-" * 80 + "\n")
                for r in passed_refactorings:
                    f.write(f"{r['refactoring']:<15} {r['mi_rank']:<8} {r['logprob_rank']:<12} {r['token_rank']:<11} {r['cc_rank']:<8} "
                            f"{r['mi']:<8.3f} {r['logprob']:<10.1f}\n")
            else:
                f.write("No refactorings maintained their pass rates.\n")
            
            # Section 3: Top Refactorings by Each Metric (Overall)
            f.write("\nTOP REFACTORINGS BY EACH METRIC (ALL):\n")
            f.write("-" * 80 + "\n")
            
            # Find top performers for each metric
            top_mi = min(tup['results'], key=lambda x: x['mi_rank'])
            top_logprob = min(tup['results'], key=lambda x: x['logprob_rank'])
            top_tokens = min(tup['results'], key=lambda x: x['token_rank'])
            top_cc = min(tup['results'], key=lambda x: x['cc_rank'])
            
            f.write(f"Best Maintainability (MI):     {top_mi['refactoring']:<15} Rank: {top_mi['mi_rank']:<2} Score: {top_mi['mi']:<8.3f}\n")
            f.write(f"Best Code Quality (LogProb):   {top_logprob['refactoring']:<15} Rank: {top_logprob['logprob_rank']:<2} Score: {top_logprob['logprob']:<10.1f}\n")
            f.write(f"Most Concise (Tokens):         {top_tokens['refactoring']:<15} Rank: {top_tokens['token_rank']:<2} Score: {top_tokens['tokens']:<8}\n")
            f.write(f"Simplest (CC):                 {top_cc['refactoring']:<15} Rank: {top_cc['cc_rank']:<2} Score: {top_cc['cc']:<6}\n")
            
            # Section 4: Top Refactorings by Each Metric (Passed Only)
            if passed_refactorings:
                f.write("\nTOP REFACTORINGS BY EACH METRIC (PASSED ONLY):\n")
                f.write("-" * 80 + "\n")
                
                # Find top performers among passed refactorings for each metric
                top_mi_passed = min(passed_refactorings, key=lambda x: x['mi_rank'])
                top_logprob_passed = min(passed_refactorings, key=lambda x: x['logprob_rank'])
                top_tokens_passed = min(passed_refactorings, key=lambda x: x['token_rank'])
                top_cc_passed = min(passed_refactorings, key=lambda x: x['cc_rank'])
                
                f.write(f"Best Maintainability (MI):     {top_mi_passed['refactoring']:<15} Rank: {top_mi_passed['mi_rank']:<2} Score: {top_mi_passed['mi']:<8.3f}\n")
                f.write(f"Best Code Quality (LogProb):   {top_logprob_passed['refactoring']:<15} Rank: {top_logprob_passed['logprob_rank']:<2} Score: {top_logprob_passed['logprob']:<10.1f}\n")
                f.write(f"Most Concise (Tokens):         {top_tokens_passed['refactoring']:<15} Rank: {top_tokens_passed['token_rank']:<2} Score: {top_tokens_passed['tokens']:<8}\n")
                f.write(f"Simplest (CC):                 {top_cc_passed['refactoring']:<15} Rank: {top_cc_passed['cc_rank']:<2} Score: {top_cc_passed['cc']:<6}\n")
            else:
                f.write("\nTOP REFACTORINGS BY EACH METRIC (PASSED ONLY):\n")
                f.write("-" * 80 + "\n")
                f.write("No refactorings maintained their pass rates.\n")
            
            f.write("\n" + "=" * 80 + "\n\n")

    print(f"  Wrote results to {json_output_path} and {txt_output_path}")
    return len(cluster_results)

def main():
    # base_dir = "tuple_archive/tuple_human_evals"
    base_dir = "./"
    if not os.path.isdir(base_dir):
        print(f"Directory {base_dir} not found!")
        return

    total = 0
    for cluster_name in sorted(os.listdir(base_dir)):
        cluster_path = os.path.join(base_dir, cluster_name)
        if os.path.isdir(cluster_path) and cluster_name.startswith("cluster_"):
            total += process_cluster(cluster_path, cluster_name)

    print(f"\nCompleted processing {total} tuples across all clusters.")

if __name__ == "__main__":
    main()
