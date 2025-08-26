#!/usr/bin/env python3
"""
Analyze study results to determine which metrics won in each pair type.
"""

import json
import csv
from collections import defaultdict
from pathlib import Path

def analyze_study_results(results_file):
    """
    Analyze study results to determine metric performance.
    
    Args:
        results_file: Path to CSV or JSON file with study results
    """
    
    # Load tuple data for reference
    with open('data/tuples_v3.json', 'r') as f:
        tuples_data = json.load(f)
    
    # Create mapping of tuple index to data
    tuple_map = {i: data for i, data in enumerate(tuples_data)}
    
    # Load enhanced assignments for user reference
    enhanced_file = Path('data/user_assignments_enhanced.json')
    if enhanced_file.exists():
        with open(enhanced_file, 'r') as f:
            user_assignments = json.load(f)
    else:
        print("Warning: Enhanced assignments file not found. Run analyze_assignments.py first.")
        user_assignments = {}
    
    # Process results (this would come from actual study data)
    # For now, we'll create a sample analysis structure
    
    results_by_metric = {
        'mi': {'wins': 0, 'losses': 0, 'total': 0},
        'logprob': {'wins': 0, 'losses': 0, 'total': 0},
        'tokens': {'wins': 0, 'losses': 0, 'total': 0}
    }
    
    results_by_pair_type = {
        'mi_vs_logprob': {'mi_wins': 0, 'logprob_wins': 0, 'total': 0},
        'mi_vs_tokens': {'mi_wins': 0, 'tokens_wins': 0, 'total': 0},
        'logprob_vs_tokens': {'logprob_wins': 0, 'tokens_wins': 0, 'total': 0}
    }
    
    return results_by_metric, results_by_pair_type

def process_user_response(response, tuple_data):
    """
    Process a single user response to determine which metric won.
    
    Args:
        response: User's response dict with choice, tupleId, etc.
        tuple_data: The tuple data from tuples_v3.json
    
    Returns:
        Dict with winning metric, losing metric, and pair_type
    """
    choice = response.get('choice', '').upper()
    
    if choice == 'V1':
        winner = tuple_data['v1_metric']
        loser = tuple_data['v2_metric']
    elif choice == 'V2':
        winner = tuple_data['v2_metric']
        loser = tuple_data['v1_metric']
    else:
        return None
    
    return {
        'winner': winner,
        'loser': loser,
        'pair_type': tuple_data['pair_type'],
        'tuple': tuple_data['tuple'],
        'user_choice': choice
    }

def create_analysis_report(user_id, responses):
    """
    Create a detailed analysis report for a user's responses.
    
    Args:
        user_id: User identifier
        responses: List of user responses
    
    Returns:
        Dict with analysis results
    """
    
    # Load tuple data
    with open('data/tuples_v3.json', 'r') as f:
        tuples_data = json.load(f)
    
    analysis = {
        'user_id': user_id,
        'total_responses': len(responses),
        'metric_preferences': defaultdict(int),
        'pair_type_choices': defaultdict(lambda: defaultdict(int)),
        'detailed_choices': []
    }
    
    for response in responses:
        tuple_idx = response.get('tupleId')
        if tuple_idx is not None and tuple_idx < len(tuples_data):
            tuple_data = tuples_data[tuple_idx]
            result = process_user_response(response, tuple_data)
            
            if result:
                # Track overall metric preferences
                analysis['metric_preferences'][result['winner']] += 1
                
                # Track choices by pair type
                pair_type = result['pair_type']
                analysis['pair_type_choices'][pair_type][result['winner']] += 1
                
                # Store detailed choice info
                analysis['detailed_choices'].append({
                    'trial': response.get('trialNumber'),
                    'tuple': result['tuple'],
                    'pair_type': pair_type,
                    'choice': response.get('choice'),
                    'winner': result['winner'],
                    'loser': result['loser'],
                    'v1_was': tuple_data['v1_metric'],
                    'v2_was': tuple_data['v2_metric']
                })
    
    # Calculate preference percentages
    total = sum(analysis['metric_preferences'].values())
    if total > 0:
        analysis['metric_preference_pct'] = {
            metric: (count / total) * 100
            for metric, count in analysis['metric_preferences'].items()
        }
    
    return analysis

def generate_summary_report(all_analyses):
    """
    Generate a summary report across all users.
    
    Args:
        all_analyses: List of analysis dicts for all users
    
    Returns:
        Dict with summary statistics
    """
    summary = {
        'total_users': len(all_analyses),
        'total_responses': sum(a['total_responses'] for a in all_analyses),
        'overall_metric_wins': defaultdict(int),
        'pair_type_results': defaultdict(lambda: defaultdict(int)),
        'metric_win_rates': {}
    }
    
    # Aggregate results
    for analysis in all_analyses:
        # Sum up metric wins
        for metric, count in analysis['metric_preferences'].items():
            summary['overall_metric_wins'][metric] += count
        
        # Sum up pair type results
        for pair_type, choices in analysis['pair_type_choices'].items():
            for metric, count in choices.items():
                summary['pair_type_results'][pair_type][metric] += count
    
    # Calculate win rates
    for pair_type, results in summary['pair_type_results'].items():
        total = sum(results.values())
        if total > 0:
            summary['pair_type_results'][pair_type]['win_rates'] = {
                metric: (count / total) * 100
                for metric, count in results.items()
                if metric != 'win_rates'
            }
    
    # Overall win rates
    total_choices = sum(summary['overall_metric_wins'].values())
    if total_choices > 0:
        summary['metric_win_rates'] = {
            metric: (count / total_choices) * 100
            for metric, count in summary['overall_metric_wins'].items()
        }
    
    return summary

def print_analysis_report(analysis):
    """Print a formatted analysis report."""
    print("=" * 60)
    print(f"ANALYSIS FOR USER: {analysis['user_id']}")
    print("=" * 60)
    
    print(f"\nTotal responses: {analysis['total_responses']}")
    
    print("\nMetric Preferences:")
    for metric, pct in analysis.get('metric_preference_pct', {}).items():
        count = analysis['metric_preferences'][metric]
        print(f"  {metric}: {count} wins ({pct:.1f}%)")
    
    print("\nChoices by Pair Type:")
    for pair_type, choices in analysis['pair_type_choices'].items():
        print(f"  {pair_type}:")
        total = sum(choices.values())
        for metric, count in choices.items():
            pct = (count / total * 100) if total > 0 else 0
            print(f"    {metric}: {count} ({pct:.1f}%)")
    
    print("\nDetailed Choices (first 3):")
    for choice in analysis['detailed_choices'][:3]:
        print(f"  Trial {choice['trial']}: {choice['pair_type']}")
        print(f"    Chose: {choice['choice']} ({choice['winner']})")
        print(f"    V1 was: {choice['v1_was']}, V2 was: {choice['v2_was']}")

def print_summary_report(summary):
    """Print a formatted summary report."""
    print("\n" + "=" * 60)
    print("OVERALL STUDY SUMMARY")
    print("=" * 60)
    
    print(f"\nTotal users: {summary['total_users']}")
    print(f"Total responses: {summary['total_responses']}")
    
    print("\nOverall Metric Win Rates:")
    for metric, rate in summary['metric_win_rates'].items():
        wins = summary['overall_metric_wins'][metric]
        print(f"  {metric}: {wins} wins ({rate:.1f}%)")
    
    print("\nResults by Pair Type:")
    for pair_type, results in summary['pair_type_results'].items():
        print(f"\n  {pair_type}:")
        win_rates = results.get('win_rates', {})
        for metric, rate in win_rates.items():
            count = results[metric]
            print(f"    {metric}: {count} wins ({rate:.1f}%)")

# Example usage function
def analyze_sample_data():
    """Analyze sample data to demonstrate the analysis pipeline."""
    
    # Create sample responses (in real usage, this would come from actual study data)
    sample_responses = [
        {
            'tupleId': 0,
            'choice': 'V1',
            'trialNumber': 1,
            'pairType': 'mi_vs_logprob',
            'v1_metric': 'mi',
            'v2_metric': 'logprob'
        },
        {
            'tupleId': 1,
            'choice': 'V2',
            'trialNumber': 2,
            'pairType': 'mi_vs_tokens',
            'v1_metric': 'mi',
            'v2_metric': 'tokens'
        },
        {
            'tupleId': 2,
            'choice': 'V1',
            'trialNumber': 3,
            'pairType': 'logprob_vs_tokens',
            'v1_metric': 'logprob',
            'v2_metric': 'tokens'
        }
    ]
    
    # Analyze single user
    analysis = create_analysis_report('U0AECDC46', sample_responses)
    print_analysis_report(analysis)
    
    # Create summary across multiple users (using same data for demo)
    all_analyses = [
        create_analysis_report(f'User{i}', sample_responses)
        for i in range(3)
    ]
    
    summary = generate_summary_report(all_analyses)
    print_summary_report(summary)

def analyze_from_csv(csv_file):
    """Analyze results from a CSV file exported from the study."""
    import csv
    
    user_responses = defaultdict(list)
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = row['UserID']
            user_responses[user_id].append({
                'tupleId': int(row['TupleID']),
                'choice': row['Choice'],
                'trialNumber': int(row['TrialNumber']),
                'timestamp': row['Timestamp']
            })
    
    print(f"Loaded responses from {len(user_responses)} users")
    
    all_analyses = []
    for user_id, responses in user_responses.items():
        analysis = create_analysis_report(user_id, responses)
        all_analyses.append(analysis)
        
    summary = generate_summary_report(all_analyses)
    print_summary_report(summary)
    
    return all_analyses, summary

def analyze_from_localstorage_backup(json_file):
    """Analyze results from a JSON backup file from localStorage."""
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract responses
    responses = data.get('responses', data.get('allResponses', []))
    user_id = data.get('participantId', data.get('user_id', 'Unknown'))
    
    # Add metadata if missing
    for i, response in enumerate(responses):
        if 'pairType' not in response and 'tupleId' in response:
            # Load tuple data to get pair_type
            with open('data/tuples_v3.json', 'r') as f:
                tuples_data = json.load(f)
            if response['tupleId'] < len(tuples_data):
                tuple_data = tuples_data[response['tupleId']]
                response['pairType'] = tuple_data['pair_type']
                response['v1_metric'] = tuple_data['v1_metric']
                response['v2_metric'] = tuple_data['v2_metric']
    
    analysis = create_analysis_report(user_id, responses)
    print_analysis_report(analysis)
    
    return analysis

if __name__ == "__main__":
    import sys
    
    print("Study Results Analysis Tool")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # Analyze file provided as argument
        file_path = sys.argv[1]
        
        if file_path.endswith('.csv'):
            print(f"\nAnalyzing CSV file: {file_path}")
            analyze_from_csv(file_path)
        elif file_path.endswith('.json'):
            print(f"\nAnalyzing JSON file: {file_path}")
            analyze_from_localstorage_backup(file_path)
        else:
            print(f"Error: Unsupported file format. Use .csv or .json")
    else:
        print("\nUsage:")
        print("  python3 analyze_results.py <results_file>")
        print("\nExamples:")
        print("  python3 analyze_results.py study_responses_U0AECDC46_123456.csv")
        print("  python3 analyze_results.py study_responses_U0AECDC46_123456.json")
        print("\nRunning demo analysis...")
        print("-" * 60)
        
        analyze_sample_data()