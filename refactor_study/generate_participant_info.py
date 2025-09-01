#!/usr/bin/env python3
"""
Generate a comprehensive participant information file with links and pair details.
"""

import json

def load_assignments():
    """Load the no-duplicates assignments"""
    with open('data/user_assignments_no_duplicates.json', 'r') as f:
        return json.load(f)

def load_tuples_data():
    """Load the tuples data"""
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        return json.load(f)

def generate_participant_info():
    """Generate comprehensive participant information"""
    assignments = load_assignments()
    tuples_data = load_tuples_data()
    
    # Debug key (from deployment info)
    debug_key = "xR9mK2nP7qL4wZ8v"
    base_url = "https://zzigak.github.io/refactor_study/"
    
    participant_info = {
        "study_info": {
            "total_participants": len(assignments),
            "questions_per_participant": 10,
            "total_unique_tuples": len(tuples_data),
            "data_file": "data/tuples_v4_no_docs.json"
        },
        "participants": {}
    }
    
    # Sort user IDs for consistent ordering
    sorted_users = sorted(assignments.keys())
    
    for idx, user_id in enumerate(sorted_users, 1):
        tuple_indices = assignments[user_id]
        
        # Generate links
        normal_link = f"{base_url}?id={user_id}"
        debug_link = f"{base_url}?id={user_id}&debugKey={debug_key}"
        
        # Get detailed pair information
        pairs = []
        for position, tuple_idx in enumerate(tuple_indices, 1):
            tuple_info = tuples_data[tuple_idx]
            
            # Extract problem names from the tuple name
            tuple_name = tuple_info['name']
            # Format: "cluster_X/tuple_A:cc_python_A_B:cc_python_B_C:cc_python_C"
            parts = tuple_name.split('/')
            if len(parts) > 1:
                problem_parts = parts[1].split(':')
                if len(problem_parts) >= 2:
                    # Extract the actual problem names
                    problems = []
                    for part in problem_parts[1:]:  # Skip the first "tuple_X" part
                        prob_name = part.split('_')[:3]  # Get cc_python_XX
                        problems.append('_'.join(prob_name))
                    problems_str = " + ".join(problems)
                else:
                    problems_str = tuple_info['cluster']
            else:
                problems_str = tuple_info['cluster']
            
            pair_info = {
                "position": position,
                "tuple_index": tuple_idx,
                "cluster": tuple_info['cluster'],
                "problems": problems_str,
                "comparison_type": tuple_info['pair_type'],
                "v1_metric": tuple_info['v1_metric'],
                "v2_metric": tuple_info['v2_metric'],
                "v1_refactoring": tuple_info.get('v1_refactoring', 'N/A'),
                "v2_refactoring": tuple_info.get('v2_refactoring', 'N/A')
            }
            pairs.append(pair_info)
        
        participant_info["participants"][user_id] = {
            "participant_number": idx,
            "user_id": user_id,
            "links": {
                "normal": normal_link,
                "debug": debug_link
            },
            "pairs": pairs
        }
    
    # Save as JSON
    with open('participant_info_complete.json', 'w') as f:
        json.dump(participant_info, f, indent=2)
    
    # Also create a simplified text version for easy reading
    with open('participant_links_and_pairs.txt', 'w') as f:
        f.write("PARTICIPANT STUDY INFORMATION\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Participants: {len(assignments)}\n")
        f.write(f"Questions per Participant: 10\n")
        f.write(f"Data File: data/tuples_v4_no_docs.json\n")
        f.write("\n" + "=" * 80 + "\n\n")
        
        for user_id in sorted_users:
            info = participant_info["participants"][user_id]
            f.write(f"PARTICIPANT #{info['participant_number']}: {user_id}\n")
            f.write("-" * 60 + "\n")
            f.write("LINKS:\n")
            f.write(f"  Normal: {info['links']['normal']}\n")
            f.write(f"  Debug:  {info['links']['debug']}\n\n")
            f.write("PAIRS BEING COMPARED:\n")
            
            for pair in info['pairs']:
                f.write(f"  {pair['position']}. {pair['problems']}\n")
                f.write(f"     Cluster: {pair['cluster']}\n")
                f.write(f"     Comparison: {pair['v1_metric']} vs {pair['v2_metric']}\n")
                f.write(f"     Refactorings: {pair['v1_refactoring']} vs {pair['v2_refactoring']}\n\n")
            
            f.write("\n")
    
    # Create a CSV version for spreadsheet use
    import csv
    with open('participant_links_and_pairs.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Participant #', 'User ID', 'Normal Link', 'Debug Link', 
                        'Position', 'Cluster', 'Problems', 'Comparison Type', 
                        'V1 Metric', 'V2 Metric'])
        
        for user_id in sorted_users:
            info = participant_info["participants"][user_id]
            for pair in info['pairs']:
                writer.writerow([
                    info['participant_number'],
                    user_id,
                    info['links']['normal'],
                    info['links']['debug'],
                    pair['position'],
                    pair['cluster'],
                    pair['problems'],
                    pair['comparison_type'],
                    pair['v1_metric'],
                    pair['v2_metric']
                ])
    
    print("Generated files:")
    print("  - participant_info_complete.json (full details)")
    print("  - participant_links_and_pairs.txt (readable text format)")
    print("  - participant_links_and_pairs.csv (spreadsheet format)")

if __name__ == "__main__":
    generate_participant_info()