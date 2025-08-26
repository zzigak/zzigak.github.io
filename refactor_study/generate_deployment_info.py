#!/usr/bin/env python3
"""
Generate comprehensive deployment information for the user study.
"""

import json
from pathlib import Path

def generate_deployment_info():
    """Generate complete deployment information with all user assignments."""
    
    # Load user assignments
    with open('data/user_assignments_final.json', 'r') as f:
        user_assignments = json.load(f)
    
    # Load enhanced assignments with details
    with open('data/user_assignments_enhanced.json', 'r') as f:
        user_enhanced = json.load(f)
    
    # Load tuple data
    with open('data/tuples_v4_no_docs.json', 'r') as f:
        tuples_data = json.load(f)
    
    deployment_info = {
        "deployment_info": {
            "study_url": "https://zzigak.github.io/refactor_study/",
            "debug_url": "https://zzigak.github.io/refactor_study/study_single_form.html?debugKey=xR9mK2nP7qL4wZ8v",
            "total_users": len(user_assignments),
            "questions_per_user": 10,
            "total_unique_tuples": len(tuples_data),
            "data_file": "data/tuples_v4_no_docs.json",
            "notes": [
                "Each user sees 10 different tuple comparisons",
                "Each comparison is between two refactoring methods",
                "Pair types: mi_vs_logprob (ID:1), mi_vs_tokens (ID:2), logprob_vs_tokens (ID:3)",
                "Users should focus on NEW functions only, not existing extracted functions",
                "Documentation/docstrings have been removed to focus on functionality"
            ]
        },
        "metric_definitions": {
            "mi": "Mutual Information - measures statistical dependency between code elements",
            "logprob": "Log Probability - based on language model probability scores",
            "tokens": "Token-based metric - based on token count and complexity"
        },
        "users": {}
    }
    
    # Process each user
    for user_id in sorted(user_assignments.keys()):
        tuple_indices = user_assignments[user_id]
        
        # Get enhanced info if available
        enhanced_info = user_enhanced.get(user_id, {})
        
        user_info = {
            "user_link": f"https://zzigak.github.io/refactor_study/?id={user_id}",
            "debug_link": f"https://zzigak.github.io/refactor_study/?id={user_id}&debugKey=xR9mK2nP7qL4wZ8v",
            "assigned_tuples": [],
            "pair_type_distribution": enhanced_info.get('pair_type_counts', {})
        }
        
        # Add detailed info for each assigned tuple
        for position, tuple_idx in enumerate(tuple_indices, 1):
            if tuple_idx < len(tuples_data):
                tuple_data = tuples_data[tuple_idx]
                
                tuple_info = {
                    "position": position,
                    "tuple_index": tuple_idx,
                    "tuple_name": tuple_data.get('tuple', 'N/A'),
                    "cluster": tuple_data.get('cluster', 'N/A'),
                    "pair_type": tuple_data.get('pair_type', 'N/A'),
                    "pair_id": {
                        'mi_vs_logprob': 1,
                        'mi_vs_tokens': 2,
                        'logprob_vs_tokens': 3
                    }.get(tuple_data.get('pair_type'), 0),
                    "v1_metric": tuple_data.get('v1_metric', 'N/A'),
                    "v1_refactoring": tuple_data.get('v1_refactoring', 'N/A'),
                    "v1_score": tuple_data.get('v1_score', 0),
                    "v2_metric": tuple_data.get('v2_metric', 'N/A'),
                    "v2_refactoring": tuple_data.get('v2_refactoring', 'N/A'),
                    "v2_score": tuple_data.get('v2_score', 0)
                }
                
                user_info["assigned_tuples"].append(tuple_info)
        
        deployment_info["users"][user_id] = user_info
    
    # Save deployment info
    output_file = Path('user_study_deployment_info.json')
    with open(output_file, 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    print(f"Deployment info saved to {output_file}")
    
    # Also create a simplified CSV for easy reference
    create_csv_summary(deployment_info)
    
    return deployment_info

def create_csv_summary(deployment_info):
    """Create a CSV summary of user assignments."""
    import csv
    
    csv_file = Path('user_study_assignments.csv')
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow([
            'User ID',
            'User Link',
            'Position',
            'Tuple Index',
            'Tuple Name',
            'Pair Type',
            'V1 Metric',
            'V2 Metric'
        ])
        
        # Write data for each user
        for user_id, user_info in deployment_info['users'].items():
            for tuple_info in user_info['assigned_tuples']:
                writer.writerow([
                    user_id,
                    user_info['user_link'],
                    tuple_info['position'],
                    tuple_info['tuple_index'],
                    tuple_info['tuple_name'].split(':')[-1] if ':' in tuple_info['tuple_name'] else tuple_info['tuple_name'],
                    tuple_info['pair_type'],
                    tuple_info['v1_metric'],
                    tuple_info['v2_metric']
                ])
    
    print(f"CSV summary saved to {csv_file}")

def create_readme():
    """Create a README file for deployment."""
    
    readme_content = """# Refactoring Study Deployment Guide

## Quick Start

1. **Deploy the files**: Push all files in the `refactor_study` directory to your GitHub Pages site.

2. **Share user links**: Each user has a unique link in `user_study_deployment_info.json`
   - Example: `https://zzigak.github.io/refactor_study/?id=U0AECDC46`

3. **Monitor progress**: Use the debug links to see what users are seeing
   - Debug URL adds: `&debugKey=xR9mK2nP7qL4wZ8v`

## Files to Deploy

Essential files:
- `index.html` - Landing page with instructions
- `study_single_form.html` - Main study interface
- `css/style.css` - Styling
- `js/study_single_form.js` - Study logic
- `js/app.js` - Landing page logic
- `data/tuples_v4_no_docs.json` - Study data (without docstrings)
- `data/user_assignments_final.json` - User assignments

## Data Collection

Results are saved in two ways:
1. **Google Form submission** - Primary method
2. **Local download** - Backup CSV and JSON files

## Analysis

After collecting responses:
```bash
python3 analyze_results.py study_responses_USER_ID.csv
```

## Important Notes

- Study requires desktop/laptop (mobile is blocked)
- Each user sees 10 tuple comparisons
- Users compare V1 vs V2 for each tuple
- Focus is on NEW functions, not existing extracted ones
- Documentation has been removed to focus on functionality

## User Distribution

- Total users: 30
- Questions per user: 10
- Total unique tuples: 45
- Pair types distributed evenly across users

## Support

For issues or questions about the deployment, check:
- `user_study_deployment_info.json` - Complete user assignments
- `user_study_assignments.csv` - Simplified CSV view
- Debug mode for troubleshooting
"""
    
    with open('DEPLOYMENT_README.md', 'w') as f:
        f.write(readme_content)
    
    print("Deployment README created")

if __name__ == "__main__":
    print("Generating deployment information...")
    deployment_info = generate_deployment_info()
    
    print(f"\nTotal users: {len(deployment_info['users'])}")
    print(f"Questions per user: 10")
    
    # Show sample user
    first_user = list(deployment_info['users'].keys())[0]
    print(f"\nSample user: {first_user}")
    print(f"Link: {deployment_info['users'][first_user]['user_link']}")
    print(f"Pair type distribution: {deployment_info['users'][first_user]['pair_type_distribution']}")
    
    create_readme()
    
    print("\n✅ Deployment files ready!")
    print("Files created:")
    print("  - user_study_deployment_info.json (complete assignment details)")
    print("  - user_study_assignments.csv (simplified CSV)")
    print("  - DEPLOYMENT_README.md (deployment guide)")