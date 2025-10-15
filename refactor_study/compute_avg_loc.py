#!/usr/bin/env python3
"""
Script to compute the average lines of code (LOC) for programs in logo_train_200.json
"""

import json
import os

def count_lines_of_code(program_code):
    """
    Count the lines of code in a program string.
    Splits by newlines and counts non-empty lines after stripping whitespace.
    """
    lines = program_code.strip().split('\n')
    # Count non-empty lines (after stripping whitespace)
    non_empty_lines = [line for line in lines if line.strip()]
    return len(non_empty_lines)

def compute_average_loc(json_file_path):
    """
    Compute the average lines of code for all programs in the JSON file.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = []
            # Read line by line since each line is a separate JSON object
            for line in f:
                line = line.strip()
                if line:
                    data.append(json.loads(line))
        
        if not data:
            print("No data found in the file.")
            return
        
        total_loc = 0
        program_count = len(data)
        loc_list = []
        
        print(f"Analyzing {program_count} programs...")
        print("-" * 50)
        
        for i, entry in enumerate(data, 1):
            if 'program' in entry:
                program_code = entry['program']
                loc = count_lines_of_code(program_code)
                total_loc += loc
                loc_list.append(loc)
                
                # Show first few examples
                if i <= 5:
                    print(f"Program {i}: {loc} lines")
                    print(f"  Code: {program_code[:60]}{'...' if len(program_code) > 60 else ''}")
                    print()
        
        if loc_list:
            avg_loc = total_loc / len(loc_list)
            min_loc = min(loc_list)
            max_loc = max(loc_list)
            
            print("=" * 50)
            print("RESULTS:")
            print(f"Total programs analyzed: {len(loc_list)}")
            print(f"Total lines of code: {total_loc}")
            print(f"Average LOC per program: {avg_loc:.2f}")
            print(f"Minimum LOC: {min_loc}")
            print(f"Maximum LOC: {max_loc}")
            print("=" * 50)
            
            # Show distribution
            loc_ranges = {
                "1-5 lines": len([x for x in loc_list if 1 <= x <= 5]),
                "6-10 lines": len([x for x in loc_list if 6 <= x <= 10]),
                "11-15 lines": len([x for x in loc_list if 11 <= x <= 15]),
                "16-20 lines": len([x for x in loc_list if 16 <= x <= 20]),
                "21+ lines": len([x for x in loc_list if x > 20])
            }
            
            print("\nLOC Distribution:")
            for range_name, count in loc_ranges.items():
                percentage = (count / len(loc_list)) * 100
                print(f"  {range_name}: {count} programs ({percentage:.1f}%)")
        
        else:
            print("No programs found with 'program' field.")
            
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Path to the JSON file
    json_file = "/Users/zzigak/dev/websites/zzigak.github.io/refactor_study/logo_train_200.json"
    
    if os.path.exists(json_file):
        compute_average_loc(json_file)
    else:
        print(f"File not found: {json_file}")
        print("Please make sure the file exists in the expected location.")
