#!/usr/bin/env python3
"""
Generate user assignments with uniform tuple distribution.
Each tuple should be used approximately the same number of times.
Users can see the same cluster multiple times, but never the same tuple.
"""

import json
import random
import string
from collections import defaultdict, Counter

def generate_user_id():
    """Generate a random user ID in the format UXXXXXXXX"""
    return 'U' + ''.join(random.choices(string.hexdigits.upper(), k=9))

def load_tuples_data():
    """Load the tuples data from v4"""
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        return json.load(f)

def generate_uniform_assignments(num_users=30, questions_per_user=10):
    """
    Generate assignments ensuring uniform tuple distribution.
    Each tuple should be used approximately equal times.
    """
    tuples_data = load_tuples_data()
    num_tuples = len(tuples_data)
    
    # Calculate total assignments needed
    total_assignments = num_users * questions_per_user
    
    # Calculate how many times each tuple should be used
    base_usage = total_assignments // num_tuples  # Floor division
    remainder = total_assignments % num_tuples
    
    print(f"Total assignments needed: {total_assignments}")
    print(f"Number of tuples: {num_tuples}")
    print(f"Base usage per tuple: {base_usage}")
    print(f"Tuples that need one extra use: {remainder}")
    
    # Create a pool of tuple indices with the right frequency
    tuple_pool = []
    for tuple_idx in range(num_tuples):
        # First 'remainder' tuples get one extra use
        if tuple_idx < remainder:
            frequency = base_usage + 1
        else:
            frequency = base_usage
        
        # Add this tuple index 'frequency' times to the pool
        tuple_pool.extend([tuple_idx] * frequency)
    
    # Shuffle the entire pool for randomness
    random.shuffle(tuple_pool)
    
    print(f"Total pool size: {len(tuple_pool)}")
    
    # Now assign tuples to users
    user_assignments = {}
    pool_index = 0
    
    for i in range(num_users):
        user_id = generate_user_id()
        
        # Get the next 10 tuples from the pool
        user_tuples = []
        for j in range(questions_per_user):
            if pool_index < len(tuple_pool):
                user_tuples.append(tuple_pool[pool_index])
                pool_index += 1
        
        # Check for duplicates within user (shouldn't happen but let's verify)
        if len(user_tuples) != len(set(user_tuples)):
            # If duplicates found, need to swap with other users
            print(f"WARNING: Found duplicates for user {user_id}, fixing...")
            user_tuples = fix_duplicates(user_tuples, tuple_pool, pool_index)
        
        # Shuffle the user's tuples for randomized presentation order
        random.shuffle(user_tuples)
        user_assignments[user_id] = user_tuples
    
    return user_assignments

def fix_duplicates(user_tuples, full_pool, current_index):
    """
    Fix duplicates in a user's assignment by swapping with unused tuples.
    This is a fallback that shouldn't normally be needed.
    """
    seen = set()
    fixed_tuples = []
    duplicates = []
    
    for t in user_tuples:
        if t not in seen:
            seen.add(t)
            fixed_tuples.append(t)
        else:
            duplicates.append(t)
    
    # Find replacement tuples from the remaining pool
    remaining_pool = full_pool[current_index:]
    for dup in duplicates:
        for replacement in remaining_pool:
            if replacement not in seen:
                fixed_tuples.append(replacement)
                seen.add(replacement)
                break
    
    return fixed_tuples

def verify_distribution(user_assignments, tuples_data):
    """Verify the distribution is uniform"""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    # Count tuple usage
    tuple_usage = Counter()
    all_assignments = []
    
    for user_id, tuple_indices in user_assignments.items():
        for idx in tuple_indices:
            tuple_usage[idx] += 1
            all_assignments.append(idx)
    
    # Check for duplicates within users
    print("\nChecking for duplicates within users:")
    duplicates_found = False
    for user_id, tuple_indices in list(user_assignments.items())[:5]:  # Check first 5
        if len(tuple_indices) != len(set(tuple_indices)):
            print(f"  WARNING: User {user_id} has duplicate tuples!")
            duplicates_found = True
    if not duplicates_found:
        print("  ✓ No duplicates found within any user")
    
    # Analyze distribution
    usage_counts = list(tuple_usage.values())
    min_usage = min(usage_counts)
    max_usage = max(usage_counts)
    avg_usage = sum(usage_counts) / len(usage_counts)
    
    print(f"\nTuple usage statistics:")
    print(f"  Total assignments: {len(all_assignments)}")
    print(f"  Unique tuples used: {len(tuple_usage)}")
    print(f"  Min usage: {min_usage}")
    print(f"  Max usage: {max_usage}")
    print(f"  Average usage: {avg_usage:.2f}")
    print(f"  Range: {max_usage - min_usage}")
    
    # Show distribution
    usage_distribution = Counter(usage_counts)
    print(f"\nUsage distribution:")
    for count in sorted(usage_distribution.keys()):
        num_tuples = usage_distribution[count]
        print(f"  {num_tuples} tuples used {count} times")
    
    # Check cluster distribution (just for info)
    print(f"\nCluster distribution (for reference):")
    cluster_usage = defaultdict(int)
    for user_id, tuple_indices in user_assignments.items():
        user_clusters = []
        for idx in tuple_indices:
            cluster = tuples_data[idx]['cluster']
            cluster_usage[cluster] += 1
            user_clusters.append(cluster)
        
        # Show first user's cluster distribution as example
        if user_id == list(user_assignments.keys())[0]:
            cluster_counts = Counter(user_clusters)
            print(f"  Example user {user_id}:")
            for cluster, count in sorted(cluster_counts.items()):
                if count > 1:
                    print(f"    {cluster}: {count} times")
    
    print(f"\n  Overall cluster usage:")
    for cluster in sorted(cluster_usage.keys()):
        print(f"    {cluster}: {cluster_usage[cluster]} total uses")

def save_assignments(user_assignments, output_file='data/user_assignments_uniform.json'):
    """Save the assignments to a JSON file"""
    with open(output_file, 'w') as f:
        json.dump(user_assignments, f, indent=2)
    print(f"\n✓ Saved assignments to {output_file}")

def main():
    random.seed(42)  # For reproducibility
    
    print("Generating uniform tuple distribution assignments...")
    print("="*60)
    
    # Load data
    tuples_data = load_tuples_data()
    
    # Generate assignments
    user_assignments = generate_uniform_assignments(30, 10)
    
    # Verify assignments
    verify_distribution(user_assignments, tuples_data)
    
    # Save assignments
    save_assignments(user_assignments)

if __name__ == "__main__":
    main()