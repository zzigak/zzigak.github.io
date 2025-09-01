#!/usr/bin/env python3
"""
Generate CSV file with user assignments that have no duplicate clusters per user.
"""

import json
import csv

def load_assignments():
    """Load the no-duplicates assignments"""
    with open('data/user_assignments_no_duplicates.json', 'r') as f:
        return json.load(f)

def load_tuples_data():
    """Load the tuples data"""
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        return json.load(f)

def generate_csv():
    """Generate CSV with user assignments"""
    assignments = load_assignments()
    tuples_data = load_tuples_data()
    
    # Create CSV rows
    rows = []
    
    for user_id, tuple_indices in assignments.items():
        user_link = f"https://zzigak.github.io/refactor_study/?id={user_id}"
        
        for position, tuple_idx in enumerate(tuple_indices, 1):
            tuple_info = tuples_data[tuple_idx]
            
            # Extract the base problem name from the tuple name
            # Format is like: "tuple_17:cc_python_17_16:cc_python_16_19:cc_python_19"
            tuple_name = tuple_info['name']
            # Extract the main problem identifier (simplified)
            problem_parts = tuple_name.split('/')[-1].split(':')
            if len(problem_parts) > 1:
                # Get the first problem mentioned
                problem_name = problem_parts[1].split('_')[0:3]  # e.g., cc_python_17
                problem_name = '_'.join(problem_name)
            else:
                problem_name = tuple_info['cluster']
            
            row = {
                'User ID': user_id,
                'User Link': user_link,
                'Position': position,
                'Tuple Index': tuple_idx,
                'Tuple Name': problem_name,
                'Cluster': tuple_info['cluster'],
                'Pair Type': tuple_info['pair_type'],
                'V1 Metric': tuple_info['v1_metric'],
                'V2 Metric': tuple_info['v2_metric']
            }
            rows.append(row)
    
    # Write to CSV
    output_file = 'user_study_assignments_no_duplicates.csv'
    with open(output_file, 'w', newline='') as f:
        fieldnames = ['User ID', 'User Link', 'Position', 'Tuple Index', 
                     'Tuple Name', 'Cluster', 'Pair Type', 'V1 Metric', 'V2 Metric']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Generated {output_file} with {len(rows)} assignments")
    
    # Verify no duplicates per user
    print("\nVerifying no duplicate clusters per user:")
    for user_id in list(assignments.keys())[:3]:  # Check first 3 users
        user_rows = [r for r in rows if r['User ID'] == user_id]
        clusters = [r['Cluster'] for r in user_rows]
        unique_clusters = set(clusters)
        print(f"{user_id}: {len(clusters)} assignments, {len(unique_clusters)} unique clusters")
        if len(clusters) != len(unique_clusters):
            print(f"  WARNING: Duplicates found!")

if __name__ == "__main__":
    generate_csv()