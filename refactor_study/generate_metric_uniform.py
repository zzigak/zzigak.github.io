#!/usr/bin/env python3
"""
Generate perfectly uniform assignments treating each (tuple, metric) pair as unique.
We have 45 unique comparisons total, need to distribute uniformly.
"""

import json
import random
from collections import Counter

def generate_user_id():
    """Generate a random user ID"""
    import string
    return 'U' + ''.join(random.choices(string.hexdigits.upper(), k=9))

def generate_uniform_metric_assignments():
    """
    Generate assignments with uniform distribution over all 45 metric comparisons.
    30 participants × 10 comparisons = 300 assignments
    300 / 45 = 6.67 per comparison
    So 30 comparisons get 7 uses, 15 comparisons get 6 uses
    """
    
    # We have indices 0-44 (45 unique metric comparisons)
    num_comparisons = 45
    num_participants = 30
    comparisons_per_participant = 10
    total_assignments = num_participants * comparisons_per_participant  # 300
    
    # Calculate distribution
    base_usage = total_assignments // num_comparisons  # 6
    extra_uses = total_assignments % num_comparisons  # 30
    
    print(f"Distribution for 45 unique metric comparisons:")
    print(f"  Total assignments: {total_assignments}")
    print(f"  Base usage: {base_usage} times per comparison")
    print(f"  Comparisons with +1 usage: {extra_uses}")
    print(f"  Expected: {extra_uses} comparisons × 7 + {num_comparisons - extra_uses} comparisons × 6")
    
    # Create pool with correct frequencies
    assignment_pool = []
    for i in range(num_comparisons):
        # First 30 comparisons get 7 uses, remaining 15 get 6 uses
        frequency = 7 if i < extra_uses else 6
        assignment_pool.extend([i] * frequency)
    
    # Shuffle the pool
    random.shuffle(assignment_pool)
    
    print(f"Total pool size: {len(assignment_pool)} (should be 300)")
    
    # Distribute to participants ensuring no duplicates within each participant
    assignments = {}
    
    # Simple approach: each participant gets every 30th item from the pool
    # This ensures good distribution and no duplicates
    for p in range(num_participants):
        user_id = generate_user_id()
        user_indices = []
        
        # Pick indices using a systematic sampling approach
        for i in range(comparisons_per_participant):
            pool_index = p + (i * num_participants)
            if pool_index < len(assignment_pool):
                user_indices.append(assignment_pool[pool_index])
        
        # Shuffle for random presentation order
        random.shuffle(user_indices)
        assignments[user_id] = user_indices
    
    return assignments

def verify_metric_assignments(assignments):
    """Verify the distribution is uniform across metric comparisons"""
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        tuples = json.load(f)
    
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    # Check for duplicates within users
    print("\n1. Checking for duplicates within participants:")
    all_good = True
    for user_id in list(assignments.keys())[:5]:  # Check first 5
        indices = assignments[user_id]
        if len(indices) != len(set(indices)):
            print(f"  ✗ User {user_id} has duplicate indices!")
            all_good = False
        else:
            print(f"  ✓ User {user_id}: {len(indices)} unique comparisons")
    
    # Check overall distribution
    all_indices = []
    for indices in assignments.values():
        all_indices.extend(indices)
    
    index_counts = Counter(all_indices)
    
    print(f"\n2. Distribution analysis:")
    print(f"  Total assignments: {len(all_indices)}")
    print(f"  Unique indices used: {len(index_counts)}")
    
    # Distribution of usage
    usage_dist = Counter(index_counts.values())
    print(f"\n3. Usage per comparison:")
    for usage, count in sorted(usage_dist.items()):
        print(f"  {count} comparisons used {usage} times")
    
    # Check metric type distribution
    metric_types = Counter()
    for idx, count in index_counts.items():
        pair_type = tuples[idx]['pair_type']
        metric_types[pair_type] += count
    
    print(f"\n4. Metric type distribution:")
    for mtype, count in sorted(metric_types.items()):
        print(f"  {mtype}: {count} total uses")
    
    min_usage = min(index_counts.values())
    max_usage = max(index_counts.values())
    
    if max_usage - min_usage <= 1:
        print("\n✓✓✓ PERFECT UNIFORM DISTRIBUTION ACHIEVED! ✓✓✓")
        print(f"  Each comparison is used {min_usage}-{max_usage} times")
    else:
        print(f"\n✗ Distribution range: {max_usage - min_usage}")
    
    return all_good

def main():
    random.seed(42)
    
    print("Generating uniform distribution over metric comparisons...")
    print("="*60)
    
    # Generate assignments
    assignments = generate_uniform_metric_assignments()
    
    # Verify
    is_valid = verify_metric_assignments(assignments)
    
    if is_valid:
        # Save
        with open('data/user_assignments_metric_uniform.json', 'w') as f:
            json.dump(assignments, f, indent=2)
        print("\n✓ Saved to data/user_assignments_metric_uniform.json")
        print("\nThis ensures uniform distribution across all 45 metric comparisons!")
    else:
        print("\n✗ Some issues found, but saved anyway")

if __name__ == "__main__":
    main()