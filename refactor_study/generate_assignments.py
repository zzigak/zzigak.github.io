#!/usr/bin/env python3
"""
Generate user assignments for the refactoring study.
Each user sees 10 comparisons from 10 different clusters (original problems).
No user sees the same original problem twice.
"""

import json
import random
import string
from collections import defaultdict

def generate_user_id():
    """Generate a random user ID in the format UXXXXXXXX"""
    return 'U' + ''.join(random.choices(string.hexdigits.upper(), k=9))

def load_tuples_data():
    """Load the tuples data from v4"""
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        return json.load(f)

def organize_by_cluster(tuples_data):
    """Organize tuples by their cluster (original problem)"""
    clusters = defaultdict(list)
    for idx, tuple_data in enumerate(tuples_data):
        cluster = tuple_data['cluster']
        clusters[cluster].append({
            'index': idx,
            'data': tuple_data
        })
    return clusters

def generate_assignments(num_users=30):
    """Generate assignments ensuring each user sees 10 unique clusters"""
    tuples_data = load_tuples_data()
    clusters = organize_by_cluster(tuples_data)
    
    # Verify we have at least 10 clusters
    cluster_names = list(clusters.keys())
    if len(cluster_names) < 10:
        raise ValueError(f"Need at least 10 clusters, but only have {len(cluster_names)}")
    
    print(f"Found {len(cluster_names)} clusters: {cluster_names}")
    
    # Track how many times each tuple has been assigned
    tuple_usage_count = defaultdict(int)
    
    # Generate assignments for each user
    user_assignments = {}
    
    for i in range(num_users):
        user_id = generate_user_id()
        user_tuples = []
        
        # Select exactly 10 clusters for this user (all available clusters)
        selected_clusters = cluster_names[:10] if len(cluster_names) >= 10 else cluster_names
        
        for cluster_name in selected_clusters:
            # Get all tuples in this cluster
            cluster_tuples = clusters[cluster_name]
            
            # Sort by usage count to prefer less-used tuples
            sorted_tuples = sorted(cluster_tuples, 
                                 key=lambda x: tuple_usage_count[x['index']])
            
            # Select the least-used tuple from this cluster
            selected = sorted_tuples[0]
            user_tuples.append(selected['index'])
            tuple_usage_count[selected['index']] += 1
        
        # Shuffle the order of tuples for this user
        random.shuffle(user_tuples)
        user_assignments[user_id] = user_tuples
    
    return user_assignments, tuple_usage_count

def save_assignments(user_assignments, output_file='data/user_assignments_no_duplicates.json'):
    """Save the assignments to a JSON file"""
    with open(output_file, 'w') as f:
        json.dump(user_assignments, f, indent=2)
    print(f"Saved assignments to {output_file}")

def verify_assignments(user_assignments, tuples_data):
    """Verify that no user sees the same cluster twice"""
    print("\nVerifying assignments...")
    
    for user_id, tuple_indices in list(user_assignments.items())[:5]:  # Check first 5 users
        clusters_seen = []
        for idx in tuple_indices:
            cluster = tuples_data[idx]['cluster']
            clusters_seen.append(cluster)
        
        unique_clusters = set(clusters_seen)
        print(f"{user_id}: {len(tuple_indices)} tuples, {len(unique_clusters)} unique clusters")
        
        if len(clusters_seen) != len(unique_clusters):
            duplicates = [c for c in clusters_seen if clusters_seen.count(c) > 1]
            print(f"  WARNING: Duplicates found: {duplicates}")
        else:
            print(f"  ✓ No duplicates")

def main():
    random.seed(42)  # For reproducibility
    
    print("Generating user assignments for refactoring study...")
    
    # Load data
    tuples_data = load_tuples_data()
    print(f"Loaded {len(tuples_data)} tuples")
    
    # Generate assignments
    user_assignments, usage_count = generate_assignments(30)
    
    # Verify assignments
    verify_assignments(user_assignments, tuples_data)
    
    # Save assignments
    save_assignments(user_assignments)
    
    # Print usage statistics
    print(f"\nTuple usage statistics:")
    print(f"Min usage: {min(usage_count.values())}")
    print(f"Max usage: {max(usage_count.values())}")
    print(f"Average usage: {sum(usage_count.values()) / len(usage_count):.2f}")

if __name__ == "__main__":
    main()