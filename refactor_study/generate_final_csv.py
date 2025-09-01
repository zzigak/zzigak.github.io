#!/usr/bin/env python3
"""
Generate final CSV with participant links and pair information.
"""

import json
import csv

def generate_participant_csv():
    """Generate CSV with participant links and assigned pairs"""
    
    # Load assignments
    with open('data/user_assignments_final_uniform.json', 'r') as f:
        assignments = json.load(f)
    
    # Load tuple data
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        tuples = json.load(f)
    
    # Create CSV
    rows = []
    
    for user_id, indices in assignments.items():
        # Regular link (use lowercase for domain)
        regular_link = f"https://zzigak.github.io/refactor_study/?id={user_id}"
        
        # Debug link
        debug_link = f"https://zzigak.github.io/refactor_study/?id={user_id}&debugKey=nextstep123"
        
        # Get tuple information
        tuple_names = []
        pair_types = []
        for idx in indices:
            tuple_names.append(tuples[idx]['name'])
            pair_types.append(tuples[idx]['pair_type'])
        
        # Create row
        row = {
            'user_id': user_id,
            'regular_link': regular_link,
            'debug_link': debug_link,
            'tuples': ', '.join(tuple_names),
            'pair_types': ', '.join(pair_types)
        }
        rows.append(row)
    
    # Write CSV
    with open('participant_links_final.csv', 'w', newline='') as f:
        fieldnames = ['user_id', 'regular_link', 'debug_link', 'tuples', 'pair_types']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Generated CSV with {len(rows)} participants")
    
    # Also generate a compact version with just ID and links
    with open('user_study_assignments_final.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['study_id', 'link'])
        for user_id in assignments.keys():
            link = f"https://zzigak.github.io/refactor_study/?id={user_id}"
            writer.writerow([user_id, link])
    
    print("Generated user_study_assignments_final.csv")
    
    # Analyze distribution
    print("\nDistribution Analysis:")
    tuple_counts = {}
    metric_counts = {}
    
    for indices in assignments.values():
        for idx in indices:
            tuple_name = tuples[idx]['name']
            pair_type = tuples[idx]['pair_type']
            
            if tuple_name not in tuple_counts:
                tuple_counts[tuple_name] = 0
            tuple_counts[tuple_name] += 1
            
            if pair_type not in metric_counts:
                metric_counts[pair_type] = 0
            metric_counts[pair_type] += 1
    
    print("\nBase Tuple Usage:")
    for name, count in sorted(tuple_counts.items()):
        print(f"  {name}: {count} uses")
    
    print("\nMetric Comparison Distribution:")
    for metric, count in sorted(metric_counts.items()):
        print(f"  {metric}: {count} uses")

if __name__ == "__main__":
    generate_participant_csv()