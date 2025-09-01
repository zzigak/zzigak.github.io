#!/usr/bin/env python3
"""
Generate CSV and participant info files for uniform assignments.
"""

import json
import csv

def load_assignments():
    """Load the uniform assignments"""
    with open('data/user_assignments_uniform.json', 'r') as f:
        return json.load(f)

def load_tuples_data():
    """Load the tuples data"""
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        return json.load(f)

def generate_csv_and_info():
    """Generate CSV with user assignments and participant info"""
    assignments = load_assignments()
    tuples_data = load_tuples_data()
    
    # Debug key
    debug_key = "xR9mK2nP7qL4wZ8v"
    base_url = "https://zzigak.github.io/refactor_study/"
    
    # Create CSV rows
    csv_rows = []
    
    # Create participant info
    participant_info = {
        "study_info": {
            "total_participants": len(assignments),
            "questions_per_participant": 10,
            "total_unique_tuples": len(tuples_data),
            "data_file": "data/tuples_v4_no_docs.json",
            "assignment_type": "uniform_tuple_distribution"
        },
        "participants": {}
    }
    
    # Sort user IDs for consistent ordering
    sorted_users = sorted(assignments.keys())
    
    for user_num, user_id in enumerate(sorted_users, 1):
        tuple_indices = assignments[user_id]
        
        # Generate links
        user_link = f"{base_url}?id={user_id}"
        debug_link = f"{base_url}?id={user_id}&debugKey={debug_key}"
        
        # Process each tuple
        pairs = []
        for position, tuple_idx in enumerate(tuple_indices, 1):
            tuple_info = tuples_data[tuple_idx]
            
            # Extract problem names
            tuple_name = tuple_info['name']
            parts = tuple_name.split('/')
            if len(parts) > 1:
                problem_parts = parts[1].split(':')
                if len(problem_parts) >= 2:
                    problems = []
                    for part in problem_parts[1:]:
                        prob_name = part.split('_')[:3]
                        problems.append('_'.join(prob_name))
                    problems_str = " + ".join(problems)
                else:
                    problems_str = tuple_info['cluster']
            else:
                problems_str = tuple_info['cluster']
            
            # Add to CSV
            csv_row = {
                'User ID': user_id,
                'User Link': user_link,
                'Debug Link': debug_link,
                'Position': position,
                'Tuple Index': tuple_idx,
                'Tuple Name': tuple_info.get('name', f'tuple_{tuple_idx}'),
                'Problems': problems_str,
                'Cluster': tuple_info['cluster'],
                'Pair Type': tuple_info['pair_type'],
                'V1 Metric': tuple_info['v1_metric'],
                'V2 Metric': tuple_info['v2_metric']
            }
            csv_rows.append(csv_row)
            
            # Add to participant info
            pairs.append({
                "position": position,
                "tuple_index": tuple_idx,
                "cluster": tuple_info['cluster'],
                "problems": problems_str,
                "comparison_type": tuple_info['pair_type'],
                "v1_metric": tuple_info['v1_metric'],
                "v2_metric": tuple_info['v2_metric']
            })
        
        participant_info["participants"][user_id] = {
            "participant_number": user_num,
            "user_id": user_id,
            "links": {
                "normal": user_link,
                "debug": debug_link
            },
            "pairs": pairs
        }
    
    # Write CSV
    output_csv = 'user_study_uniform_assignments.csv'
    with open(output_csv, 'w', newline='') as f:
        fieldnames = ['User ID', 'User Link', 'Debug Link', 'Position', 'Tuple Index', 
                     'Tuple Name', 'Problems', 'Cluster', 'Pair Type', 'V1 Metric', 'V2 Metric']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
    
    print(f"Generated {output_csv} with {len(csv_rows)} assignments")
    
    # Write participant info JSON
    with open('participant_info_uniform.json', 'w') as f:
        json.dump(participant_info, f, indent=2)
    
    print(f"Generated participant_info_uniform.json")
    
    # Write readable text version
    with open('participant_links_uniform.txt', 'w') as f:
        f.write("UNIFORM DISTRIBUTION PARTICIPANT STUDY\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Participants: {len(assignments)}\n")
        f.write(f"Questions per Participant: 10\n")
        f.write(f"Distribution: Each tuple used 6-7 times (perfectly uniform)\n")
        f.write("\n" + "=" * 80 + "\n\n")
        
        for user_id in sorted_users[:5]:  # Show first 5 as examples
            info = participant_info["participants"][user_id]
            f.write(f"PARTICIPANT #{info['participant_number']}: {user_id}\n")
            f.write("-" * 60 + "\n")
            f.write("LINKS:\n")
            f.write(f"  Normal: {info['links']['normal']}\n")
            f.write(f"  Debug:  {info['links']['debug']}\n\n")
            f.write("PAIRS:\n")
            
            for pair in info['pairs']:
                f.write(f"  {pair['position']}. Tuple {pair['tuple_index']} ({pair['cluster']}): {pair['v1_metric']} vs {pair['v2_metric']}\n")
            
            f.write("\n")
        
        f.write("... (25 more participants)\n")
    
    print(f"Generated participant_links_uniform.txt")
    
    # Verify distribution
    print("\nVerifying tuple distribution:")
    from collections import Counter
    tuple_usage = Counter()
    for user_id, tuple_list in assignments.items():
        for t in tuple_list:
            tuple_usage[t] += 1
    
    usage_counts = Counter(tuple_usage.values())
    print(f"Distribution: {dict(usage_counts)}")
    print(f"  {usage_counts[6]} tuples used 6 times")
    print(f"  {usage_counts[7]} tuples used 7 times")

if __name__ == "__main__":
    generate_csv_and_info()