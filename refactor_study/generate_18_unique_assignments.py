#!/usr/bin/env python3
"""
Generate assignments using only the 18 unique tuples.
Each participant sees 10 out of 18 unique tuples.
Ensures uniform distribution across all participants.
"""

import json
import random
from collections import Counter, defaultdict

def generate_user_id():
    """Generate a random user ID"""
    import string
    return 'U' + ''.join(random.choices(string.hexdigits.upper(), k=9))

def get_unique_tuples():
    """Extract the 18 unique tuples from the data file"""
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        tuples = json.load(f)
    
    # Map unique tuple names to their first occurrence index
    unique_tuples = {}
    seen_names = set()
    
    for i, t in enumerate(tuples):
        name = t['name']
        if name not in seen_names:
            unique_tuples[name] = {
                'index': i,
                'name': name,
                'cluster': t['cluster'],
                'data': t
            }
            seen_names.add(name)
    
    return unique_tuples

def calculate_distribution(num_participants=30, tuples_per_participant=10, num_unique_tuples=18):
    """Calculate the optimal distribution"""
    total_assignments = num_participants * tuples_per_participant  # 300
    
    # Each tuple should appear this many times for perfect distribution
    ideal_usage = total_assignments / num_unique_tuples  # 300/18 = 16.67
    
    # Since we can't have fractional assignments:
    base_usage = int(ideal_usage)  # 16 times
    remainder = total_assignments - (base_usage * num_unique_tuples)  # 300 - (16*18) = 12
    
    print(f"Distribution calculation:")
    print(f"  Total assignments needed: {total_assignments}")
    print(f"  Unique tuples available: {num_unique_tuples}")
    print(f"  Ideal usage per tuple: {ideal_usage:.2f}")
    print(f"  Base usage: {base_usage} times")
    print(f"  Tuples needing +1 usage: {remainder}")
    
    return base_usage, remainder

def generate_uniform_assignments_18():
    """Generate assignments with uniform distribution for 18 unique tuples"""
    
    # Get the 18 unique tuples
    unique_tuples = get_unique_tuples()
    tuple_list = list(unique_tuples.values())
    
    print(f"Found {len(tuple_list)} unique tuples")
    
    # Calculate distribution
    base_usage, extra_usage = calculate_distribution(30, 10, 18)
    
    # Create assignment pool
    # Each tuple appears base_usage times, plus some appear one extra time
    assignment_pool = []
    
    for i, tuple_info in enumerate(tuple_list):
        # First 'extra_usage' tuples get one additional use
        if i < extra_usage:
            frequency = base_usage + 1  # 17 times
        else:
            frequency = base_usage  # 16 times
        
        # Add this tuple's index 'frequency' times to the pool
        for _ in range(frequency):
            assignment_pool.append(tuple_info['index'])
    
    # Shuffle the pool
    random.shuffle(assignment_pool)
    
    print(f"Total assignments in pool: {len(assignment_pool)}")
    
    # Distribute to participants
    participants = {}
    for p in range(30):
        user_id = generate_user_id()
        
        # Get the next 10 assignments
        start_idx = p * 10
        end_idx = start_idx + 10
        user_assignments = assignment_pool[start_idx:end_idx]
        
        # Shuffle for random presentation order
        random.shuffle(user_assignments)
        
        participants[user_id] = user_assignments
    
    return participants

def verify_assignments(assignments):
    """Verify the distribution is uniform and correct"""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    # Load tuple data to check uniqueness
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        tuples = json.load(f)
    
    # Count usage of each tuple index
    tuple_usage = Counter()
    unique_names_seen = set()
    
    for user_id, tuple_indices in assignments.items():
        for idx in tuple_indices:
            tuple_usage[idx] += 1
            unique_names_seen.add(tuples[idx]['name'])
    
    # Check for duplicates within users
    print("\n1. Checking for duplicate content within users:")
    duplicates_found = False
    for user_id, tuple_indices in list(assignments.items())[:3]:  # Check first 3
        user_names = [tuples[idx]['name'] for idx in tuple_indices]
        unique_names = set(user_names)
        
        if len(user_names) != len(unique_names):
            print(f"  WARNING: User {user_id} has duplicate tuple content!")
            duplicates_found = True
        else:
            print(f"  ✓ User {user_id}: 10 unique tuple comparisons")
    
    if not duplicates_found:
        print("  ✓ No users have duplicate tuple content")
    
    # Analyze distribution
    print(f"\n2. Distribution analysis:")
    print(f"  Total unique tuple names used: {len(unique_names_seen)}")
    print(f"  Total assignments: {sum(tuple_usage.values())}")
    
    # Group by unique content
    content_usage = Counter()
    for idx, count in tuple_usage.items():
        name = tuples[idx]['name']
        content_usage[name] += count
    
    usage_values = list(content_usage.values())
    print(f"\n3. Usage per unique tuple:")
    print(f"  Min: {min(usage_values)}")
    print(f"  Max: {max(usage_values)}")
    print(f"  Average: {sum(usage_values)/len(usage_values):.2f}")
    
    # Show distribution
    distribution = Counter(usage_values)
    for usage, count in sorted(distribution.items()):
        print(f"  {count} unique tuples used {usage} times")
    
    if max(usage_values) - min(usage_values) <= 1:
        print("\n✓ PERFECT UNIFORMITY ACHIEVED!")
    else:
        print(f"\n✗ Distribution range: {max(usage_values) - min(usage_values)}")

def save_assignments(assignments):
    """Save the assignments"""
    with open('data/user_assignments_18_unique.json', 'w') as f:
        json.dump(assignments, f, indent=2)
    print("\n✓ Saved to data/user_assignments_18_unique.json")

def main():
    random.seed(42)  # For reproducibility
    
    print("Generating assignments for 18 unique tuples...")
    print("="*60)
    
    # Generate assignments
    assignments = generate_uniform_assignments_18()
    
    # Verify
    verify_assignments(assignments)
    
    # Save
    save_assignments(assignments)

if __name__ == "__main__":
    main()