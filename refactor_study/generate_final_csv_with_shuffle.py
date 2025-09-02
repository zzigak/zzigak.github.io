#!/usr/bin/env python3
"""
Generate final CSV with participant links, pairs, and shuffle information.
"""

import json
import csv

def generate_detailed_csv_with_shuffle():
    """Generate CSV with detailed information including shuffle data"""
    
    # Load shuffled assignments
    with open('data/user_assignments_shuffled.json', 'r') as f:
        shuffled_assignments = json.load(f)
    
    # Load tuple data
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        tuples = json.load(f)
    
    # Create rows for CSV
    rows = []
    
    for user_id, assignments in shuffled_assignments.items():
        # Regular and debug links
        regular_link = f"https://zzigak.github.io/refactor_study/?id={user_id}"
        debug_link = f"https://zzigak.github.io/refactor_study/?id={user_id}&debugKey=nextstep123"
        
        # Process each assignment
        for position, assignment in enumerate(assignments, 1):
            idx = assignment['tuple_index']
            tuple_data = tuples[idx]
            
            # Parse the tuple name to extract problem names
            tuple_name = tuple_data['name']
            parts = tuple_name.split('/')[-1]  # Get the tuple part after cluster
            problem_parts = parts.replace('tuple_', '').split(':')[1:]  # Remove tuple_ prefix and split
            problems = ' + '.join(problem_parts)
            
            # Get cluster
            cluster = tuple_name.split('/')[0]
            
            # Create row with shuffle information
            row = {
                'User ID': user_id,
                'User Link': regular_link,
                'Debug Link': debug_link,
                'Position': position,
                'Tuple Index': idx,
                'Tuple Name': tuple_name,
                'Problems': problems,
                'Cluster': cluster,
                'Pair Type': assignment['pair_type'],
                'Original V1 Metric': assignment['original_v1_metric'],
                'Original V2 Metric': assignment['original_v2_metric'],
                'Swapped': 'Yes' if assignment['swap_versions'] else 'No',
                'Displayed V1 Metric': assignment['displayed_v1_metric'],
                'Displayed V2 Metric': assignment['displayed_v2_metric'],
                'V1 Shows': assignment['displayed_v1_metric'],
                'V2 Shows': assignment['displayed_v2_metric']
            }
            rows.append(row)
    
    # Write detailed CSV
    fieldnames = [
        'User ID', 'User Link', 'Debug Link', 'Position', 
        'Tuple Index', 'Tuple Name', 'Problems', 'Cluster', 
        'Pair Type', 'Original V1 Metric', 'Original V2 Metric',
        'Swapped', 'Displayed V1 Metric', 'Displayed V2 Metric',
        'V1 Shows', 'V2 Shows'
    ]
    
    with open('user_study_final_shuffled_assignments.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Generated user_study_final_shuffled_assignments.csv with {len(rows)} rows")
    print(f"Total participants: {len(shuffled_assignments)}")
    
    # Also generate a simple version with just ID and links
    with open('user_study_shuffled_links.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['study_id', 'link', 'debug_link'])
        for user_id in shuffled_assignments.keys():
            link = f"https://zzigak.github.io/refactor_study/?id={user_id}"
            debug_link = f"https://zzigak.github.io/refactor_study/?id={user_id}&debugKey=nextstep123"
            writer.writerow([user_id, link, debug_link])
    
    print("Generated user_study_shuffled_links.csv")
    
    # Analyze distribution
    analyze_distribution(shuffled_assignments)

def analyze_distribution(shuffled_assignments):
    """Analyze the distribution of shuffled assignments"""
    
    print("\n=== DISTRIBUTION ANALYSIS ===")
    
    # Count swaps per pair type
    pair_type_swaps = {}
    pair_type_totals = {}
    
    # Count metric positions
    metric_v1_count = {}
    metric_v2_count = {}
    
    for user_id, assignments in shuffled_assignments.items():
        for assignment in assignments:
            pair_type = assignment['pair_type']
            
            # Count totals per pair type
            if pair_type not in pair_type_totals:
                pair_type_totals[pair_type] = 0
                pair_type_swaps[pair_type] = 0
            pair_type_totals[pair_type] += 1
            
            if assignment['swap_versions']:
                pair_type_swaps[pair_type] += 1
            
            # Count metric positions
            v1_metric = assignment['displayed_v1_metric']
            v2_metric = assignment['displayed_v2_metric']
            
            if v1_metric not in metric_v1_count:
                metric_v1_count[v1_metric] = 0
            metric_v1_count[v1_metric] += 1
            
            if v2_metric not in metric_v2_count:
                metric_v2_count[v2_metric] = 0
            metric_v2_count[v2_metric] += 1
    
    print("\nSwap distribution by pair type:")
    for pair_type in sorted(pair_type_totals.keys()):
        total = pair_type_totals[pair_type]
        swapped = pair_type_swaps[pair_type]
        percent = (swapped / total) * 100 if total > 0 else 0
        print(f"  {pair_type}: {swapped}/{total} swapped ({percent:.1f}%)")
    
    print("\nMetrics appearing as V1:")
    for metric in sorted(metric_v1_count.keys()):
        count = metric_v1_count[metric]
        print(f"  {metric}: {count} times")
    
    print("\nMetrics appearing as V2:")
    for metric in sorted(metric_v2_count.keys()):
        count = metric_v2_count[metric]
        print(f"  {metric}: {count} times")

if __name__ == "__main__":
    generate_detailed_csv_with_shuffle()