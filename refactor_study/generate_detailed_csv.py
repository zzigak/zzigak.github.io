#!/usr/bin/env python3
"""
Generate detailed CSV in the same format as user_study_uniform_assignments.csv
"""

import json
import csv

def generate_detailed_csv():
    """Generate CSV with detailed information for each assignment"""
    
    # Load assignments
    with open('data/user_assignments_final_uniform.json', 'r') as f:
        assignments = json.load(f)
    
    # Load tuple data
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        tuples = json.load(f)
    
    # Create rows for CSV
    rows = []
    
    for user_id, indices in assignments.items():
        # Regular and debug links
        regular_link = f"https://zzigak.github.io/refactor_study/?id={user_id}"
        debug_link = f"https://zzigak.github.io/refactor_study/?id={user_id}&debugKey=nextstep123"
        
        # Process each assignment
        for position, idx in enumerate(indices, 1):
            tuple_data = tuples[idx]
            
            # Parse the tuple name to extract problem names
            tuple_name = tuple_data['name']
            parts = tuple_name.split('/')[-1]  # Get the tuple part after cluster
            problem_parts = parts.replace('tuple_', '').split(':')[1:]  # Remove tuple_ prefix and split
            problems = ' + '.join(problem_parts)
            
            # Get cluster
            cluster = tuple_name.split('/')[0]
            
            # Parse pair type to get metrics
            pair_type = tuple_data['pair_type']
            v1_metric, v2_metric = '', ''
            
            if pair_type == 'mi_vs_logprob':
                v1_metric = 'mi'
                v2_metric = 'logprob'
            elif pair_type == 'mi_vs_tokens':
                v1_metric = 'mi'
                v2_metric = 'tokens'
            elif pair_type == 'logprob_vs_tokens':
                v1_metric = 'logprob'
                v2_metric = 'tokens'
            
            # Create row
            row = {
                'User ID': user_id,
                'User Link': regular_link,
                'Debug Link': debug_link,
                'Position': position,
                'Tuple Index': idx,
                'Tuple Name': tuple_name,
                'Problems': problems,
                'Cluster': cluster,
                'Pair Type': pair_type,
                'V1 Metric': v1_metric,
                'V2 Metric': v2_metric
            }
            rows.append(row)
    
    # Write CSV
    fieldnames = [
        'User ID', 'User Link', 'Debug Link', 'Position', 
        'Tuple Index', 'Tuple Name', 'Problems', 'Cluster', 
        'Pair Type', 'V1 Metric', 'V2 Metric'
    ]
    
    with open('user_study_final_assignments.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Generated user_study_final_assignments.csv with {len(rows)} rows")
    print(f"Total participants: {len(assignments)}")

if __name__ == "__main__":
    generate_detailed_csv()