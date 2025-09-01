#!/usr/bin/env python3
"""
Generate user assignments with perfectly uniform tuple distribution.
Uses a round-robin approach to ensure even distribution and no duplicates.
"""

import json
import random
import string
from collections import Counter, defaultdict

def generate_user_id():
    """Generate a random user ID in the format UXXXXXXXX"""
    return 'U' + ''.join(random.choices(string.hexdigits.upper(), k=9))

def load_tuples_data():
    """Load the tuples data from v4"""
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        return json.load(f)

def generate_perfect_uniform_assignments(num_users=30, questions_per_user=10):
    """
    Generate assignments with perfectly uniform tuple distribution.
    Uses a systematic approach to ensure each tuple is used equally.
    """
    tuples_data = load_tuples_data()
    num_tuples = len(tuples_data)
    
    # Calculate how many complete rounds we need
    total_assignments = num_users * questions_per_user  # 300
    complete_rounds = total_assignments // num_tuples  # 6
    remaining_assignments = total_assignments % num_tuples  # 30
    
    print(f"Total assignments needed: {total_assignments}")
    print(f"Number of tuples: {num_tuples}")
    print(f"Complete rounds: {complete_rounds} (each tuple used {complete_rounds} times)")
    print(f"Additional assignments: {remaining_assignments}")
    
    # Create assignment sequence
    assignment_sequence = []
    
    # Add complete rounds (each tuple appears 'complete_rounds' times)
    for _ in range(complete_rounds):
        round_tuples = list(range(num_tuples))
        random.shuffle(round_tuples)
        assignment_sequence.extend(round_tuples)
    
    # Add partial round for remaining assignments
    if remaining_assignments > 0:
        partial_round = list(range(num_tuples))
        random.shuffle(partial_round)
        assignment_sequence.extend(partial_round[:remaining_assignments])
    
    print(f"Assignment sequence length: {len(assignment_sequence)}")
    
    # Now distribute to users ensuring no duplicates within each user
    user_assignments = {}
    
    # Create a matrix approach: each row is a user, we'll fill columns
    assignment_matrix = []
    for i in range(num_users):
        assignment_matrix.append([])
    
    # Distribute tuples in a way that minimizes duplicates
    for i, tuple_idx in enumerate(assignment_sequence):
        user_idx = i % num_users
        assignment_matrix[user_idx].append(tuple_idx)
    
    # Check and fix any duplicates within users
    for user_idx in range(num_users):
        user_tuples = assignment_matrix[user_idx]
        
        # Check for duplicates
        if len(user_tuples) != len(set(user_tuples)):
            # Fix duplicates by swapping with other users
            assignment_matrix[user_idx] = fix_user_duplicates(
                user_idx, assignment_matrix, num_users
            )
    
    # Create final assignments with random user IDs
    for i in range(num_users):
        user_id = generate_user_id()
        user_tuples = assignment_matrix[i]
        
        # Shuffle for random presentation order
        random.shuffle(user_tuples)
        user_assignments[user_id] = user_tuples
    
    return user_assignments

def fix_user_duplicates(user_idx, matrix, num_users):
    """
    Fix duplicates in a user's assignments by swapping with other users.
    """
    user_tuples = matrix[user_idx]
    
    # Find duplicates
    seen = set()
    duplicates = []
    unique_tuples = []
    
    for t in user_tuples:
        if t in seen:
            duplicates.append(t)
        else:
            seen.add(t)
            unique_tuples.append(t)
    
    if not duplicates:
        return user_tuples
    
    # Try to swap duplicates with other users
    for dup in duplicates:
        swapped = False
        
        # Look for another user who can swap
        for other_idx in range(num_users):
            if other_idx == user_idx:
                continue
            
            other_tuples = matrix[other_idx]
            
            # Find a tuple in other user that we don't have
            for i, other_tuple in enumerate(other_tuples):
                if other_tuple not in seen and dup not in set(other_tuples):
                    # Swap
                    matrix[other_idx][i] = dup
                    unique_tuples.append(other_tuple)
                    seen.add(other_tuple)
                    swapped = True
                    break
            
            if swapped:
                break
        
        if not swapped:
            # If can't swap, just keep it (this should be rare)
            unique_tuples.append(dup)
    
    return unique_tuples

def verify_distribution(user_assignments, tuples_data):
    """Verify the distribution is uniform"""
    print("\n" + "="*60)
    print("VERIFICATION RESULTS")
    print("="*60)
    
    # Count tuple usage
    tuple_usage = Counter()
    
    for user_id, tuple_indices in user_assignments.items():
        for idx in tuple_indices:
            tuple_usage[idx] += 1
    
    # Check for duplicates within users
    print("\n1. Checking for duplicates within users:")
    duplicates_found = 0
    for user_id, tuple_indices in user_assignments.items():
        if len(tuple_indices) != len(set(tuple_indices)):
            duplicates_found += 1
            print(f"  WARNING: User {user_id} has duplicate tuples!")
            print(f"    Tuples: {sorted(tuple_indices)}")
            print(f"    Unique: {sorted(set(tuple_indices))}")
    
    if duplicates_found == 0:
        print("  ✓ No duplicates found within any user")
    else:
        print(f"  ✗ {duplicates_found} users have duplicates")
    
    # Analyze distribution
    usage_counts = list(tuple_usage.values())
    min_usage = min(usage_counts) if usage_counts else 0
    max_usage = max(usage_counts) if usage_counts else 0
    avg_usage = sum(usage_counts) / len(usage_counts) if usage_counts else 0
    
    print(f"\n2. Tuple usage statistics:")
    print(f"  Total assignments: {sum(usage_counts)}")
    print(f"  Unique tuples used: {len(tuple_usage)} out of {len(tuples_data)}")
    print(f"  Min usage: {min_usage}")
    print(f"  Max usage: {max_usage}")
    print(f"  Average usage: {avg_usage:.2f}")
    print(f"  Range: {max_usage - min_usage}")
    
    # Show distribution
    usage_distribution = Counter(usage_counts)
    print(f"\n3. Usage distribution:")
    for count in sorted(usage_distribution.keys()):
        num_tuples = usage_distribution[count]
        print(f"  {num_tuples} tuples used {count} times")
    
    # Perfect uniformity check
    if max_usage - min_usage <= 1:
        print("\n✓ PERFECT UNIFORMITY ACHIEVED!")
        print("  All tuples are used either 6 or 7 times (optimal distribution)")
    else:
        print(f"\n✗ Distribution range is {max_usage - min_usage} (target: ≤1)")

def save_assignments(user_assignments, output_file='data/user_assignments_uniform.json'):
    """Save the assignments to a JSON file"""
    with open(output_file, 'w') as f:
        json.dump(user_assignments, f, indent=2)
    print(f"\n✓ Saved assignments to {output_file}")

def main():
    random.seed(42)  # For reproducibility
    
    print("Generating perfectly uniform tuple distribution...")
    print("="*60)
    
    # Load data
    tuples_data = load_tuples_data()
    
    # Generate assignments
    user_assignments = generate_perfect_uniform_assignments(30, 10)
    
    # Verify assignments
    verify_distribution(user_assignments, tuples_data)
    
    # Save assignments
    save_assignments(user_assignments)

if __name__ == "__main__":
    main()