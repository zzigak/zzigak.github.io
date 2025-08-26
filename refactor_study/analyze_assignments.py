#!/usr/bin/env python3
"""
Analyze current user assignments to understand pair_type distribution
and create enhanced assignment data.
"""

import json
from collections import defaultdict
from pathlib import Path

def analyze_current_assignments():
    """Analyze the current user assignments and their pair_type distribution."""
    
    # Load user assignments
    with open('data/user_assignments_final.json', 'r') as f:
        user_assignments = json.load(f)
    
    # Load tuple data
    with open('data/tuples_v3.json', 'r') as f:
        tuples_data = json.load(f)
    
    # Create a mapping of tuple index to pair_type and metrics
    tuple_info = {}
    for idx, tuple_data in enumerate(tuples_data):
        tuple_info[idx] = {
            'tuple_name': tuple_data['tuple'],
            'cluster': tuple_data['cluster'],
            'pair_type': tuple_data['pair_type'],
            'v1_metric': tuple_data['v1_metric'],
            'v2_metric': tuple_data['v2_metric'],
            'v1_refactoring': tuple_data['v1_refactoring'],
            'v2_refactoring': tuple_data['v2_refactoring']
        }
    
    # Analyze each user's assignments
    user_analysis = {}
    overall_pair_type_counts = defaultdict(int)
    
    for user_id, tuple_indices in user_assignments.items():
        user_pair_types = defaultdict(int)
        user_metrics = defaultdict(int)
        user_details = []
        
        for position, tuple_idx in enumerate(tuple_indices, 1):
            if tuple_idx in tuple_info:
                info = tuple_info[tuple_idx]
                pair_type = info['pair_type']
                
                user_pair_types[pair_type] += 1
                overall_pair_type_counts[pair_type] += 1
                
                # Count individual metrics
                user_metrics[info['v1_metric']] += 1
                user_metrics[info['v2_metric']] += 1
                
                # Store detailed info for each assignment
                user_details.append({
                    'position': position,
                    'tuple_index': tuple_idx,
                    'tuple_name': info['tuple_name'],
                    'cluster': info['cluster'],
                    'pair_type': pair_type,
                    'v1_metric': info['v1_metric'],
                    'v2_metric': info['v2_metric'],
                    'v1_refactoring': info['v1_refactoring'],
                    'v2_refactoring': info['v2_refactoring']
                })
        
        user_analysis[user_id] = {
            'pair_type_counts': dict(user_pair_types),
            'metric_counts': dict(user_metrics),
            'assignments': user_details
        }
    
    # Calculate statistics
    print("=" * 60)
    print("CURRENT ASSIGNMENT ANALYSIS")
    print("=" * 60)
    
    print(f"\nTotal users: {len(user_assignments)}")
    print(f"Total tuple options: {len(tuples_data)}")
    
    print("\nOverall pair_type distribution:")
    total_assignments = sum(overall_pair_type_counts.values())
    for pair_type, count in sorted(overall_pair_type_counts.items()):
        percentage = (count / total_assignments) * 100
        print(f"  {pair_type}: {count} ({percentage:.1f}%)")
    
    # Check if users have balanced pair_types
    print("\nPer-user pair_type distribution:")
    imbalanced_users = []
    for user_id, analysis in user_analysis.items():
        pair_counts = analysis['pair_type_counts']
        if len(pair_counts) < 3 or min(pair_counts.values()) == 0:
            imbalanced_users.append(user_id)
    
    if imbalanced_users:
        print(f"  Users with imbalanced pair_types: {len(imbalanced_users)}")
        for user_id in imbalanced_users[:5]:  # Show first 5
            counts = user_analysis[user_id]['pair_type_counts']
            print(f"    {user_id}: {counts}")
    else:
        print("  All users have balanced pair_type distribution!")
    
    # Save enhanced assignment data
    output_file = Path('data/user_assignments_enhanced.json')
    with open(output_file, 'w') as f:
        json.dump(user_analysis, f, indent=2)
    
    print(f"\nEnhanced assignment data saved to {output_file}")
    
    return user_analysis

def create_mapping_for_pair_ids():
    """Create a numeric mapping for pair_types to use as pairId."""
    pair_type_to_id = {
        'mi_vs_logprob': 1,
        'mi_vs_tokens': 2,
        'logprob_vs_tokens': 3
    }
    
    print("\nPair Type to ID Mapping:")
    for pair_type, pair_id in pair_type_to_id.items():
        print(f"  {pair_type} -> pairId: {pair_id}")
    
    return pair_type_to_id

def create_balanced_assignments(num_users=100, assignments_per_user=10):
    """Create new balanced user assignments ensuring mix of pair types."""
    
    # Load tuple data
    with open('data/tuples_v3.json', 'r') as f:
        tuples_data = json.load(f)
    
    # Group tuples by pair_type
    tuples_by_pair_type = defaultdict(list)
    for idx, tuple_data in enumerate(tuples_data):
        pair_type = tuple_data['pair_type']
        tuples_by_pair_type[pair_type].append(idx)
    
    print("\nAvailable tuples by pair_type:")
    for pair_type, indices in tuples_by_pair_type.items():
        print(f"  {pair_type}: {len(indices)} tuples")
    
    # Create balanced assignments
    new_assignments = {}
    
    # Target distribution for 10 assignments: 3-3-4 or 3-4-3 or 4-3-3
    distributions = [
        [3, 3, 4],  # mi_vs_logprob, mi_vs_tokens, logprob_vs_tokens
        [3, 4, 3],
        [4, 3, 3]
    ]
    
    pair_types = ['mi_vs_logprob', 'mi_vs_tokens', 'logprob_vs_tokens']
    
    import random
    random.seed(42)  # For reproducibility
    
    for i in range(num_users):
        user_id = f"U{i:08X}"
        
        # Choose a distribution pattern
        dist = distributions[i % 3]
        
        user_assignments = []
        for pair_type, count in zip(pair_types, dist):
            # Randomly select tuples of this pair_type
            available = tuples_by_pair_type[pair_type].copy()
            selected = random.sample(available, min(count, len(available)))
            user_assignments.extend(selected)
        
        # Shuffle the order of assignments
        random.shuffle(user_assignments)
        
        new_assignments[user_id] = user_assignments[:assignments_per_user]
    
    # Save new balanced assignments
    output_file = Path('data/user_assignments_balanced.json')
    with open(output_file, 'w') as f:
        json.dump(new_assignments, f, indent=2)
    
    print(f"\nBalanced assignments created for {num_users} users")
    print(f"Saved to {output_file}")
    
    return new_assignments

if __name__ == "__main__":
    # Analyze current assignments
    user_analysis = analyze_current_assignments()
    
    # Create pair type ID mapping
    pair_type_to_id = create_mapping_for_pair_ids()
    
    # Example: Show first user's detailed assignments
    first_user = list(user_analysis.keys())[0]
    print(f"\nExample - {first_user}'s assignments:")
    for assignment in user_analysis[first_user]['assignments'][:3]:
        print(f"  Position {assignment['position']}:")
        print(f"    Tuple: {assignment['tuple_name']}")
        print(f"    Pair type: {assignment['pair_type']}")
        print(f"    V1: {assignment['v1_metric']} ({assignment['v1_refactoring']})")
        print(f"    V2: {assignment['v2_metric']} ({assignment['v2_refactoring']})")
    
    # Optionally create new balanced assignments
    # new_assignments = create_balanced_assignments()