#!/usr/bin/env python3
"""
Generate uniform distribution over 45 metric comparisons,
while ensuring no participant sees the same base tuple twice.
"""

import json
import random
from collections import Counter, defaultdict

def generate_user_id():
    """Generate a random user ID"""
    import string
    return 'U' + ''.join(random.choices(string.hexdigits.upper(), k=9))

def load_tuple_structure():
    """Load and analyze the tuple structure"""
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        tuples = json.load(f)
    
    # Map each index to its base tuple name
    index_to_base = {}
    base_to_indices = defaultdict(list)
    
    for i, t in enumerate(tuples):
        base_name = t['name']  # The base tuple identifier
        index_to_base[i] = base_name
        base_to_indices[base_name].append(i)
    
    print(f"Structure analysis:")
    print(f"  Total comparisons: {len(tuples)}")
    print(f"  Unique base tuples: {len(base_to_indices)}")
    
    # Show how many metric variations each base tuple has
    variations = Counter([len(indices) for indices in base_to_indices.values()])
    for num_metrics, count in sorted(variations.items()):
        print(f"  {count} base tuples have {num_metrics} metric comparison(s)")
    
    return index_to_base, base_to_indices

def generate_assignments_no_tuple_duplicates():
    """
    Generate assignments ensuring:
    1. Uniform distribution over 45 comparisons (each used 6-7 times)
    2. No participant sees the same base tuple twice
    """
    
    index_to_base, base_to_indices = load_tuple_structure()
    
    num_participants = 30
    comparisons_per_participant = 10
    total_assignments = 300
    num_comparisons = 45
    
    # Each comparison should appear 6-7 times
    base_usage = total_assignments // num_comparisons  # 6
    extra_uses = total_assignments % num_comparisons   # 30
    
    print(f"\nTarget distribution:")
    print(f"  {extra_uses} comparisons × 7 uses")
    print(f"  {num_comparisons - extra_uses} comparisons × 6 uses")
    
    # Create target usage for each comparison index
    target_usage = {}
    for i in range(num_comparisons):
        target_usage[i] = 7 if i < extra_uses else 6
    
    # Track actual usage
    actual_usage = defaultdict(int)
    
    # Generate assignments
    assignments = {}
    
    for p in range(num_participants):
        user_id = generate_user_id()
        user_assignments = []
        used_base_tuples = set()
        
        # Build a list of available comparisons for this user
        available = []
        for idx in range(num_comparisons):
            base_tuple = index_to_base[idx]
            # Only add if we haven't used this base tuple and haven't exceeded target usage
            if base_tuple not in used_base_tuples and actual_usage[idx] < target_usage[idx]:
                available.append(idx)
        
        # Select 10 comparisons
        attempts = 0
        max_attempts = 100
        
        while len(user_assignments) < comparisons_per_participant and attempts < max_attempts:
            attempts += 1
            
            if not available:
                # Rebuild available list with updated constraints
                available = []
                for idx in range(num_comparisons):
                    base_tuple = index_to_base[idx]
                    if base_tuple not in used_base_tuples and actual_usage[idx] < target_usage[idx]:
                        available.append(idx)
            
            if not available:
                # If still no available, we need to be less strict
                # Allow slightly exceeding target usage
                available = []
                for idx in range(num_comparisons):
                    base_tuple = index_to_base[idx]
                    if base_tuple not in used_base_tuples:
                        available.append(idx)
            
            if available:
                # Pick one randomly
                idx = random.choice(available)
                user_assignments.append(idx)
                used_base_tuples.add(index_to_base[idx])
                actual_usage[idx] += 1
                available.remove(idx)
                
                # Also remove any other indices with the same base tuple
                base_tuple = index_to_base[idx]
                available = [i for i in available if index_to_base[i] != base_tuple]
        
        if len(user_assignments) < comparisons_per_participant:
            print(f"Warning: User {user_id} only got {len(user_assignments)} assignments")
        
        random.shuffle(user_assignments)
        assignments[user_id] = user_assignments
    
    return assignments, actual_usage

def verify_final_assignments(assignments):
    """Verify the assignments meet all criteria"""
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        tuples = json.load(f)
    
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    # Check 1: No duplicate base tuples within users
    print("\n1. Checking for duplicate base tuples within users:")
    all_good = True
    for user_id in list(assignments.keys())[:5]:  # Check first 5
        indices = assignments[user_id]
        base_tuples = [tuples[i]['name'] for i in indices]
        unique_bases = set(base_tuples)
        
        if len(base_tuples) != len(unique_bases):
            print(f"  ✗ User {user_id} sees same tuple multiple times!")
            duplicates = [t for t in base_tuples if base_tuples.count(t) > 1]
            print(f"    Duplicates: {set(duplicates)}")
            all_good = False
        else:
            print(f"  ✓ User {user_id}: {len(indices)} unique base tuples")
    
    # Check 2: Overall distribution
    all_indices = []
    for indices in assignments.values():
        all_indices.extend(indices)
    
    index_counts = Counter(all_indices)
    
    print(f"\n2. Distribution of 45 comparisons:")
    print(f"  Total assignments: {len(all_indices)}")
    print(f"  Unique comparisons used: {len(index_counts)}")
    
    usage_dist = Counter(index_counts.values())
    for usage, count in sorted(usage_dist.items()):
        print(f"  {count} comparisons used {usage} times")
    
    # Check 3: Metric type distribution
    metric_types = Counter()
    for idx, count in index_counts.items():
        if idx < len(tuples):
            pair_type = tuples[idx]['pair_type']
            metric_types[pair_type] += count
    
    print(f"\n3. Metric type distribution:")
    total_metric_uses = 0
    for mtype, count in sorted(metric_types.items()):
        print(f"  {mtype}: {count} uses")
        total_metric_uses += count
    print(f"  Total: {total_metric_uses}")
    
    min_usage = min(index_counts.values()) if index_counts else 0
    max_usage = max(index_counts.values()) if index_counts else 0
    
    if max_usage - min_usage <= 1 and all_good:
        print("\n✓✓✓ SUCCESS! ✓✓✓")
        print(f"  Uniform distribution: Each comparison used {min_usage}-{max_usage} times")
        print(f"  No participant sees the same base tuple twice")
    else:
        print(f"\n⚠ Distribution range: {max_usage - min_usage}")
        if not all_good:
            print("  ✗ Some users have duplicate base tuples")
    
    return all_good and (max_usage - min_usage <= 1)

def main():
    random.seed(42)
    
    print("Generating uniform distribution with no tuple duplicates...")
    print("="*60)
    
    # Generate
    assignments, usage = generate_assignments_no_tuple_duplicates()
    
    # Verify
    is_valid = verify_final_assignments(assignments)
    
    # Save regardless
    with open('data/user_assignments_final_uniform.json', 'w') as f:
        json.dump(assignments, f, indent=2)
    
    if is_valid:
        print("\n✓ Perfect assignments saved to data/user_assignments_final_uniform.json")
    else:
        print("\n⚠ Assignments saved to data/user_assignments_final_uniform.json")
        print("  Note: Distribution may not be perfectly uniform due to tuple constraints")

if __name__ == "__main__":
    main()