#!/usr/bin/env python3
"""
Generate 30 encrypted user IDs with uniform distribution of pairs.
Check for duplicate refactorings in pairs.
"""

import json
import random
import hashlib
from pathlib import Path
from collections import Counter, defaultdict

def generate_encrypted_user_id(index, salt="refactor_study_2024"):
    """Generate an encrypted user ID."""
    # Create a unique string for this user
    user_string = f"user_{index}_{salt}"
    # Generate SHA256 hash
    hash_obj = hashlib.sha256(user_string.encode())
    # Take first 8 characters of hex digest and convert to uppercase
    user_id = hash_obj.hexdigest()[:8].upper()
    return f"U{user_id}"

def check_duplicate_refactorings():
    """Check if any pairs are comparing the same refactorings."""
    # Load the data
    with open('data/tuples_v3.json', 'r') as f:
        data = json.load(f)
    
    print("\n=== Checking for Duplicate Refactorings in Pairs ===\n")
    
    duplicates = []
    for entry in data:
        if entry['v1_refactoring'] == entry['v2_refactoring']:
            duplicates.append({
                'id': entry['id'],
                'cluster': entry['cluster'],
                'tuple': entry['tuple'],
                'pair_type': entry['pair_type'],
                'duplicate_refactoring': entry['v1_refactoring']
            })
    
    if duplicates:
        print(f"⚠️  Found {len(duplicates)} pairs with duplicate refactorings:")
        for dup in duplicates:
            print(f"  - ID {dup['id']}: {dup['cluster']}/{dup['tuple']}")
            print(f"    Pair type: {dup['pair_type']}")
            print(f"    Both metrics selected: {dup['duplicate_refactoring']}\n")
    else:
        print("✅ No duplicate refactorings found - all pairs compare different refactorings!")
    
    return len(duplicates) == 0

def generate_uniform_assignments(num_users=30, pairs_per_user=10):
    """Generate uniform assignments for users."""
    # Load the data to get total number of pairs
    with open('data/tuples_v3.json', 'r') as f:
        data = json.load(f)
    
    total_pairs = len(data)
    print(f"\n=== Generating User Assignments ===\n")
    print(f"Total pairs available: {total_pairs}")
    print(f"Users to generate: {num_users}")
    print(f"Pairs per user: {pairs_per_user}")
    print(f"Total assignments needed: {num_users * pairs_per_user}")
    
    # Calculate how many times each pair needs to be repeated
    total_needed = num_users * pairs_per_user
    repetitions_per_pair = total_needed // total_pairs
    remainder = total_needed % total_pairs
    
    print(f"\nDistribution strategy:")
    print(f"  - Each pair will appear at least {repetitions_per_pair} times")
    print(f"  - {remainder} pairs will appear {repetitions_per_pair + 1} times")
    
    # Create pool of pair IDs with appropriate repetitions
    pair_pool = []
    for pair_id in range(total_pairs):
        # Add base repetitions
        pair_pool.extend([pair_id] * repetitions_per_pair)
    
    # Add extra repetitions for remainder
    extra_pairs = random.sample(range(total_pairs), remainder)
    pair_pool.extend(extra_pairs)
    
    # Shuffle the pool
    random.shuffle(pair_pool)
    
    # Verify the pool
    print(f"\nPool verification:")
    print(f"  - Total items in pool: {len(pair_pool)}")
    counter = Counter(pair_pool)
    min_count = min(counter.values())
    max_count = max(counter.values())
    print(f"  - Min appearances: {min_count}")
    print(f"  - Max appearances: {max_count}")
    
    # Assign to users
    assignments = {}
    for i in range(num_users):
        # Take the next 10 pairs from the pool
        user_pairs = pair_pool[i * pairs_per_user:(i + 1) * pairs_per_user]
        # Generate encrypted user ID
        user_id = generate_encrypted_user_id(i)
        assignments[user_id] = user_pairs
    
    return assignments

def analyze_assignments(assignments):
    """Analyze the distribution of assignments."""
    print("\n=== Assignment Analysis ===\n")
    
    # Count how many times each pair is assigned
    pair_counts = Counter()
    for user_pairs in assignments.values():
        for pair_id in user_pairs:
            pair_counts[pair_id] += 1
    
    # Load data to get pair details
    with open('data/tuples_v3.json', 'r') as f:
        data = json.load(f)
    
    # Analyze by pair type
    pair_type_counts = defaultdict(int)
    for pair_id, count in pair_counts.items():
        if pair_id < len(data):
            pair_type = data[pair_id]['pair_type']
            pair_type_counts[pair_type] += count
    
    print("Distribution by pair type:")
    for pair_type, count in sorted(pair_type_counts.items()):
        avg = count / len([d for d in data if d['pair_type'] == pair_type])
        print(f"  - {pair_type}: {count} total assignments (avg {avg:.1f} per pair)")
    
    print(f"\nPair assignment frequency:")
    freq_counter = Counter(pair_counts.values())
    for frequency, count in sorted(freq_counter.items()):
        print(f"  - {count} pairs assigned {frequency} times")

def main():
    """Main function."""
    random.seed(42)  # For reproducibility
    
    # Check for duplicate refactorings
    no_duplicates = check_duplicate_refactorings()
    
    # Generate assignments
    assignments = generate_uniform_assignments(num_users=30, pairs_per_user=10)
    
    # Analyze the assignments
    analyze_assignments(assignments)
    
    # Save assignments
    output_file = Path('data/user_assignments_final.json')
    with open(output_file, 'w') as f:
        json.dump(assignments, f, indent=2, sort_keys=True)
    
    print(f"\n✅ User assignments saved to {output_file}")
    
    # Print sample user IDs
    print("\n=== Sample User IDs (first 10) ===")
    for i, (user_id, pairs) in enumerate(list(assignments.items())[:10]):
        print(f"  {user_id}: {pairs[:3]}... (showing first 3 of {len(pairs)})")
    
    print(f"\n📋 Total users generated: {len(assignments)}")
    print("🔒 User IDs are encrypted using SHA256 hashing")

if __name__ == "__main__":
    main()