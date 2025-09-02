#!/usr/bin/env python3
"""
Generate assignments with shuffled v1/v2 metric positions.
This prevents bias from always showing the same metric on the same side.
"""

import json
import random
import csv

def generate_shuffled_assignments():
    """Generate new assignments with randomized v1/v2 positions"""
    
    # Load current assignments
    with open('data/user_assignments_final_uniform.json', 'r') as f:
        assignments = json.load(f)
    
    # Load tuple data
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        tuples = json.load(f)
    
    # Create shuffled version mapping for each user's assignments
    shuffled_assignments = {}
    
    for user_id, indices in assignments.items():
        user_shuffles = []
        
        for idx in indices:
            tuple_data = tuples[idx]
            
            # Randomly decide whether to swap v1/v2 (50% chance)
            swap = random.choice([True, False])
            
            assignment_entry = {
                'tuple_index': idx,
                'tuple_name': tuple_data['name'],
                'pair_type': tuple_data['pair_type'],
                'original_v1_metric': tuple_data['v1_metric'],
                'original_v2_metric': tuple_data['v2_metric'],
                'swap_versions': swap,
                'displayed_v1_metric': tuple_data['v2_metric'] if swap else tuple_data['v1_metric'],
                'displayed_v2_metric': tuple_data['v1_metric'] if swap else tuple_data['v2_metric'],
                'displayed_v1_refactoring': tuple_data['v2_refactoring'] if swap else tuple_data['v1_refactoring'],
                'displayed_v2_refactoring': tuple_data['v1_refactoring'] if swap else tuple_data['v2_refactoring']
            }
            
            user_shuffles.append(assignment_entry)
        
        shuffled_assignments[user_id] = user_shuffles
    
    # Save the shuffled assignments
    with open('data/user_assignments_shuffled.json', 'w') as f:
        json.dump(shuffled_assignments, f, indent=2)
    
    print("Generated shuffled assignments")
    
    # Analyze the distribution
    analyze_shuffle_distribution(shuffled_assignments)
    
    # Generate CSV for easy viewing
    generate_shuffled_csv(shuffled_assignments)
    
    return shuffled_assignments

def analyze_shuffle_distribution(shuffled_assignments):
    """Analyze how metrics are distributed across v1/v2 positions"""
    
    metrics_in_v1 = {'mi': 0, 'logprob': 0, 'tokens': 0}
    metrics_in_v2 = {'mi': 0, 'logprob': 0, 'tokens': 0}
    
    total_swaps = 0
    total_assignments = 0
    
    for user_id, user_shuffles in shuffled_assignments.items():
        for assignment in user_shuffles:
            total_assignments += 1
            if assignment['swap_versions']:
                total_swaps += 1
            
            v1_metric = assignment['displayed_v1_metric']
            v2_metric = assignment['displayed_v2_metric']
            
            if v1_metric in metrics_in_v1:
                metrics_in_v1[v1_metric] += 1
            if v2_metric in metrics_in_v2:
                metrics_in_v2[v2_metric] += 1
    
    print("\n=== SHUFFLE ANALYSIS ===")
    print(f"Total assignments: {total_assignments}")
    print(f"Swapped versions: {total_swaps} ({total_swaps/total_assignments*100:.1f}%)")
    print(f"Original order kept: {total_assignments - total_swaps} ({(total_assignments - total_swaps)/total_assignments*100:.1f}%)")
    
    print("\nMetrics appearing as V1:")
    for metric, count in sorted(metrics_in_v1.items()):
        print(f"  {metric}: {count} times ({count/total_assignments*100:.1f}%)")
    
    print("\nMetrics appearing as V2:")
    for metric, count in sorted(metrics_in_v2.items()):
        print(f"  {metric}: {count} times ({count/total_assignments*100:.1f}%)")

def generate_shuffled_csv(shuffled_assignments):
    """Generate CSV with shuffled assignment details"""
    
    rows = []
    
    for user_id, user_shuffles in shuffled_assignments.items():
        for position, assignment in enumerate(user_shuffles, 1):
            row = {
                'User ID': user_id,
                'Position': position,
                'Tuple Index': assignment['tuple_index'],
                'Tuple Name': assignment['tuple_name'],
                'Pair Type': assignment['pair_type'],
                'Swapped': 'Yes' if assignment['swap_versions'] else 'No',
                'V1 Shows': assignment['displayed_v1_metric'],
                'V2 Shows': assignment['displayed_v2_metric'],
                'Original V1': assignment['original_v1_metric'],
                'Original V2': assignment['original_v2_metric']
            }
            rows.append(row)
    
    with open('user_study_shuffled_assignments.csv', 'w', newline='') as f:
        fieldnames = ['User ID', 'Position', 'Tuple Index', 'Tuple Name', 'Pair Type', 
                     'Swapped', 'V1 Shows', 'V2 Shows', 'Original V1', 'Original V2']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\nGenerated user_study_shuffled_assignments.csv with {len(rows)} rows")

if __name__ == "__main__":
    # Set seed for reproducibility (remove in production for true randomization)
    random.seed(42)
    generate_shuffled_assignments()