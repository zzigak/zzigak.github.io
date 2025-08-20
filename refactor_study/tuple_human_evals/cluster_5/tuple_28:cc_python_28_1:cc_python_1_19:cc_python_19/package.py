import os
import re
from pathlib import Path
import math

# --- Configuration ---
BASE_DIR = Path(".")
CHOSEN_REFACTORING_FILE = BASE_DIR / "chosen_refactoring.txt"
ORIGINAL_DIR = BASE_DIR / "original"
PROBLEM_QUERIES_DIR = BASE_DIR / "problem_queries"
REFACTORING_DIR_PREFIX = "refactoring_"

OUTPUT_ORIGINAL_FILE = BASE_DIR / "original.txt"
OUTPUT_BEST_REFACTORING_FILE = BASE_DIR / "best_refactoring.txt"
OUTPUT_WORST_REFACTORING_FILE = BASE_DIR / "worst_refactoring.txt"

SEPARATOR_QUERY_ORIGINAL = "=========" # For original.txt

# New titles for refactoring output files
TITLE_LIBRARY_HELPERS = "########## LIBRARY HELPERS ##########"
TITLE_PROGRAM_REFACTORINGS = "########################################\n\n PROGRAM REFACTORINGS\n\n ########################################"
TITLE_PROGRAM_PREFIX = "########## PROGRAM: "
TITLE_PROGRAM_SUFFIX = " ##########"


def parse_refactoring_stats(filepath):
    """
    Parses the chosen_refactoring.txt file.
    Returns a tuple: (chosen_index, list_of_stats_dicts)
    Each stats_dict: {'index': int, 'logprob': float, 'rate_before': float, 'rate_after': float}
    """
    ref_data_map = {}
    chosen_idx = -1

    with open(filepath, 'r') as f:
        lines = f.readlines()

    current_ref_idx_from_line = None
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("Selected Refactoring:"):
            try:
                chosen_idx = int(line.split(":")[1].strip())
            except (IndexError, ValueError) as e:
                print(f"Warning: Could not parse 'Selected Refactoring' line: {line}. Error: {e}")
            continue

        ref_match = re.match(r"Refactoring (\d+):", line)
        if ref_match:
            current_ref_idx_from_line = int(ref_match.group(1))
            if current_ref_idx_from_line not in ref_data_map:
                ref_data_map[current_ref_idx_from_line] = {
                    'index': current_ref_idx_from_line,
                    'logprob': None,
                    'rate_before': None,
                    'rate_after': None,
                    'total_loss': None,
                    'tokens': None
                }
        
        if current_ref_idx_from_line is not None:
            logprob_tokens_match = re.search(r"LogProb: ([-\d\.]+), Tokens: (\d+)", line)
            if logprob_tokens_match:
                try:
                    ref_data_map[current_ref_idx_from_line]['logprob'] = float(logprob_tokens_match.group(1))
                    ref_data_map[current_ref_idx_from_line]['tokens'] = int(logprob_tokens_match.group(2))
                except (ValueError, TypeError) as e:
                    print(f"Warning: Could not parse LogProb/Tokens from line: {line}. Error: {e}")
                continue 

            loss_rates_match = re.search(
                r"Total Loss: ([\d\.]+), Mean Pass Rate Before: ([\d\.]+), Mean Pass Rate After: ([\d\.]+)", line
            )
            if loss_rates_match:
                try:
                    ref_data_map[current_ref_idx_from_line]['total_loss'] = float(loss_rates_match.group(1))
                    ref_data_map[current_ref_idx_from_line]['rate_before'] = float(loss_rates_match.group(2))
                    ref_data_map[current_ref_idx_from_line]['rate_after'] = float(loss_rates_match.group(3))
                except (ValueError, TypeError) as e:
                    print(f"Warning: Could not parse Loss/Rates from line: {line}. Error: {e}")
                continue
    
    all_stats = []
    for idx, data in ref_data_map.items():
        if all(key in data and data[key] is not None for key in ['logprob', 'rate_before', 'rate_after']):
            all_stats.append(data)
        else:
            print(f"Warning: Incomplete data for refactoring index {idx}: {data}")
            
    all_stats.sort(key=lambda x: x['index'])
    return chosen_idx, all_stats

def find_worst_refactoring_index(stats_list):
    """
    Finds the index of the "worst" refactoring.
    Worst: largest absolute logprobs AND mean pass rate after >= mean pass rate before.
    """
    eligible_candidates = []
    for stat in stats_list:
        if not all(isinstance(stat.get(key), (int, float)) for key in ['logprob', 'rate_after', 'rate_before']):
            print(f"Skipping stat due to missing numeric data: {stat}")
            continue

        if stat['rate_after'] >= stat['rate_before']:
            eligible_candidates.append(stat)

    if not eligible_candidates:
        return -1

    worst_ref = max(eligible_candidates, key=lambda s: abs(s['logprob']))
    return worst_ref['index']

def get_problem_stems(original_dir):
    """
    Gets a sorted list of problem file stems from the original directory.
    """
    stems = []
    if not original_dir.is_dir():
        print(f"Error: Original directory {original_dir} not found.")
        return stems
        
    for f_path in sorted(original_dir.glob("node_*:cc_python_*.py")):
        stems.append(f_path.stem)
    if not stems:
        print(f"Warning: No problem files found in {original_dir}")
    return stems

def create_original_output(output_file, problem_stems, queries_dir, originals_dir):
    """
    Creates the original.txt file.
    """
    print(f"Creating {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, stem in enumerate(problem_stems):
            query_file_path = queries_dir / f"{stem}_query.txt"
            original_problem_path = originals_dir / f"{stem}.py"

            outfile.write(f"{SEPARATOR_QUERY_ORIGINAL}  query {stem}:\n")
            query_content = ""
            if query_file_path.exists():
                query_content = query_file_path.read_text(encoding='utf-8')
                outfile.write(query_content)
            if not query_content.endswith('\n'):
                outfile.write('\n')

            outfile.write(f"{SEPARATOR_QUERY_ORIGINAL} problem {stem}:\n")
            problem_content = ""
            if original_problem_path.exists():
                problem_content = original_problem_path.read_text(encoding='utf-8')
                outfile.write(problem_content)
            if not problem_content.endswith('\n'):
                outfile.write('\n')
    print(f"Finished creating {output_file}")


def create_refactoring_output(output_file, ref_idx, problem_stems, base_ref_dir_prefix):
    """
    Creates a refactoring output file (best_refactoring.txt or worst_refactoring.txt)
    with enhanced section titles and program names.
    """
    print(f"Creating {output_file} for refactoring index {ref_idx}...")
    ref_dir = BASE_DIR / f"{base_ref_dir_prefix}{ref_idx}"
    lib_helpers_path = ref_dir / "library_helpers.py"

    if not ref_dir.is_dir():
        print(f"Error: Refactoring directory {ref_dir} not found. Skipping {output_file}.")
        return

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 1. Library Helpers Section
        outfile.write(f"{TITLE_LIBRARY_HELPERS}\n")
        lib_content = ""
        if lib_helpers_path.exists():
            lib_content = lib_helpers_path.read_text(encoding='utf-8').strip()
            if lib_content: # Only write content if it's not empty after stripping
                outfile.write(lib_content)
                outfile.write('\n') # Add a newline after non-empty library content
            else: # If library helper file is empty or only whitespace
                outfile.write('\n') # Ensure at least one newline after the title
        else: # If library_helpers.py does not exist
            outfile.write("\n") # Ensure a newline after the title

        outfile.write("\n") # Extra newline for separation before program refactorings title

        # 2. Program Refactorings Section
        outfile.write(f"{TITLE_PROGRAM_REFACTORINGS}\n")
        
        for i, stem in enumerate(problem_stems):
            outfile.write("\n") # Newline before each program's title block (acts as separator)
            outfile.write(f"{TITLE_PROGRAM_PREFIX}{stem}{TITLE_PROGRAM_SUFFIX}\n")
            
            refactored_problem_path = ref_dir / f"{stem}_refactored.py"
            problem_content = ""
            if refactored_problem_path.exists():
                problem_content = refactored_problem_path.read_text(encoding='utf-8').strip()
                if problem_content: # Only write content if it's not empty after stripping
                    outfile.write(problem_content)
                    # No explicit newline here; the `\n` before the *next* program's title
                    # or the end of the file will handle separation. If it's the last problem,
                    # we don't want an extra trailing blank line.
            
            # If it's the last problem and its content was written, and that content didn't end with a newline,
            # it might be desirable to add one. However, `strip()` removes it.
            # Let's ensure a newline after problem content *if* it's not the last problem,
            # to make sure there's a blank line if the next thing is another program title.
            # The `\n` written *before* the next title should already provide this separation.
            # If this is the last problem, we don't want an extra `\n` at the very end of the file.
            # So, writing `problem_content` (stripped) and relying on the next loop's `\n` before title is likely correct.
            # If problem_content is written, its last line will be printed. The next thing will be `\n` then title.
            # This creates the desired:
            # ... problem content ...
            #
            # ########## PROGRAM: next_stem ##########

    print(f"Finished creating {output_file}")


def main():
    if not CHOSEN_REFACTORING_FILE.exists():
        print(f"Error: {CHOSEN_REFACTORING_FILE} not found. Exiting.")
        return

    chosen_idx, all_ref_stats = parse_refactoring_stats(CHOSEN_REFACTORING_FILE)

    if chosen_idx == -1:
        print("Error: Could not determine the chosen refactoring index. Exiting.")
        return
    if not all_ref_stats:
        print("Error: No valid refactoring statistics found. Exiting.")
        return
        
    print(f"Selected (Best) Refactoring Index: {chosen_idx}")

    worst_idx = find_worst_refactoring_index(all_ref_stats)
    if worst_idx == -1:
        print("Warning: Could not determine the worst refactoring index based on criteria.")
    else:
        print(f"Determined Worst Refactoring Index: {worst_idx}")

    problem_stems = get_problem_stems(ORIGINAL_DIR)
    if not problem_stems:
        print("Error: No problem stems found. Cannot proceed. Exiting.")
        return

    # 1. Create original.txt
    create_original_output(OUTPUT_ORIGINAL_FILE, problem_stems, PROBLEM_QUERIES_DIR, ORIGINAL_DIR)

    # 2. Create best_refactoring.txt
    create_refactoring_output(OUTPUT_BEST_REFACTORING_FILE, chosen_idx, problem_stems, REFACTORING_DIR_PREFIX)

    # 3. Create worst_refactoring.txt (if worst_idx was found)
    if worst_idx != -1:
        create_refactoring_output(OUTPUT_WORST_REFACTORING_FILE, worst_idx, problem_stems, REFACTORING_DIR_PREFIX)
    else:
        print(f"Skipping creation of {OUTPUT_WORST_REFACTORING_FILE} as worst index was not determined.")

    print("\nScript finished.")
    print(f"Generated files:")
    print(f"- {OUTPUT_ORIGINAL_FILE.resolve()}")
    print(f"- {OUTPUT_BEST_REFACTORING_FILE.resolve()}")
    if worst_idx != -1 :
        print(f"- {OUTPUT_WORST_REFACTORING_FILE.resolve()}")
    else:
        print(f"- {OUTPUT_WORST_REFACTORING_FILE} (not generated or placeholder)")

if __name__ == "__main__":
    main()