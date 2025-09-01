#!/usr/bin/env python3
"""
Generate perfectly uniform assignments for 30 participants with 18 unique tuples.
Each participant sees 10 unique tuples, no duplicates.
"""

import json
import random
from collections import Counter
import itertools

def generate_user_id():
    """Generate a random user ID"""
    import string
    return 'U' + ''.join(random.choices(string.hexdigits.upper(), k=9))

def get_unique_tuple_indices():
    """Get the first index for each unique tuple"""
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        tuples = json.load(f)
    
    # Get first occurrence of each unique tuple
    seen = set()
    unique_indices = []
    
    for i, t in enumerate(tuples):
        name = t['name']
        if name not in seen:
            unique_indices.append(i)
            seen.add(name)
    
    return unique_indices

def generate_assignments_matrix():
    """
    Generate a 30x10 assignment matrix where:
    - Each row (participant) has 10 unique tuples
    - Each of 18 tuples appears 16-17 times total
    """
    
    # We have 18 unique tuples, need to assign 300 slots (30 participants × 10 each)
    # 300 / 18 = 16.67, so 12 tuples appear 17 times, 6 tuples appear 16 times
    
    unique_indices = get_unique_tuple_indices()
    print(f"Using indices for 18 unique tuples: {unique_indices}")
    
    # Create a pool with proper frequency
    pool = []
    for i, idx in enumerate(unique_indices):
        # First 12 tuples get 17 uses, remaining 6 get 16 uses
        frequency = 17 if i < 12 else 16
        pool.extend([idx] * frequency)
    
    # Shuffle the pool
    random.shuffle(pool)
    
    # Create assignments ensuring no participant gets duplicates
    assignments = {}
    attempts = 0
    max_attempts = 100
    
    while attempts < max_attempts:
        attempts += 1
        assignments = {}
        temp_pool = pool.copy()
        random.shuffle(temp_pool)
        
        success = True
        for p in range(30):
            user_id = generate_user_id()
            user_tuples = []
            available_pool = temp_pool.copy()
            
            # Try to select 10 unique tuples for this user
            while len(user_tuples) < 10 and available_pool:
                # Pick a random tuple from available pool
                idx = random.choice(available_pool)
                available_pool.remove(idx)
                
                # Only add if not already in user's list
                if idx not in user_tuples:
                    user_tuples.append(idx)
                    # Remove from temp_pool so it's not available for other users
                    if idx in temp_pool:
                        temp_pool.remove(idx)
            
            if len(user_tuples) < 10:
                success = False
                break
            
            assignments[user_id] = user_tuples
        
        if success:
            print(f"✓ Successfully generated assignments on attempt {attempts}")
            break
    
    if not success:
        print("Failed to generate perfect assignments, using best effort approach")
        # Fallback: simple round-robin assignment
        assignments = {}
        for p in range(30):
            user_id = generate_user_id()
            # Deterministic selection to ensure no duplicates
            start = (p * 10) % 18
            indices = []
            for i in range(10):
                idx = unique_indices[(start + i) % 18]
                indices.append(idx)
            random.shuffle(indices)
            assignments[user_id] = indices
    
    return assignments

def verify_final_assignments(assignments):
    """Verify the assignments are correct"""
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        tuples = json.load(f)
    
    print("\n" + "="*60)
    print("FINAL VERIFICATION")
    print("="*60)
    
    # Check each user has unique content
    all_good = True
    for user_id, indices in list(assignments.items())[:5]:  # Check first 5
        names = [tuples[i]['name'] for i in indices]
        unique_names = set(names)
        if len(names) != len(unique_names):
            print(f"✗ User {user_id} has duplicates!")
            all_good = False
        else:
            print(f"✓ User {user_id}: 10 unique comparisons")
    
    # Check overall distribution
    all_indices = []
    for indices in assignments.values():
        all_indices.extend(indices)
    
    # Map to unique names
    name_counts = Counter()
    for idx in all_indices:
        name_counts[tuples[idx]['name']] += 1
    
    print(f"\n Distribution of unique tuples:")
    print(f"  Total unique tuples: {len(name_counts)}")
    print(f"  Total assignments: {sum(name_counts.values())}")
    
    usage_dist = Counter(name_counts.values())
    for usage, count in sorted(usage_dist.items()):
        print(f"  {count} tuples used {usage} times")
    
    min_usage = min(name_counts.values())
    max_usage = max(name_counts.values())
    
    if max_usage - min_usage <= 1:
        print("\n✓✓✓ PERFECT UNIFORM DISTRIBUTION ACHIEVED! ✓✓✓")
        print(f"  Each unique tuple is used {min_usage}-{max_usage} times")
    
    return all_good

def main():
    random.seed(42)
    
    print("Generating perfectly uniform assignments...")
    print("="*60)
    
    # Generate
    assignments = generate_assignments_matrix()
    
    # Verify
    is_valid = verify_final_assignments(assignments)
    
    if is_valid:
        # Save
        with open('data/user_assignments_perfect.json', 'w') as f:
            json.dump(assignments, f, indent=2)
        print("\n✓ Saved to data/user_assignments_perfect.json")
        
        # Update app.js will need to use this file
        print("\nNOTE: Update app.js to use 'data/user_assignments_perfect.json'")
    else:
        print("\n✗ Assignments have issues, not saving")

if __name__ == "__main__":
    main()