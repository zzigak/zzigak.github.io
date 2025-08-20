#!/usr/bin/env python3
"""
Generate a comprehensive summary JSON with top passing refactorings for each metric.
"""

import os
import json

def main():
    base_dir = "./"
    summary_data = {
        "summary": "Top refactorings that maintain pass rates for each metric across all clusters",
        "clusters": {}
    }
    
    # Process each cluster
    for cluster_name in sorted(os.listdir(base_dir)):
        cluster_path = os.path.join(base_dir, cluster_name)
        if not (os.path.isdir(cluster_path) and cluster_name.startswith("cluster_")):
            continue
            
        json_file = os.path.join(cluster_path, f"{cluster_name}_rankings.json")
        if not os.path.exists(json_file):
            continue
            
        print(f"Processing {cluster_name}...")
        
        # Load cluster data
        with open(json_file, 'r') as f:
            cluster_data = json.load(f)
        
        cluster_summary = {
            "tuples": {}
        }
        
        # Process each tuple in the cluster
        for tuple_info in cluster_data['tuples']:
            tuple_name = tuple_info['tuple_name']
            
            # Get top passing refactorings for each metric
            if tuple_info.get('top_refactorings_passed'):
                top_passed = tuple_info['top_refactorings_passed']
                
                tuple_summary = {}
                
                # Extract top refactoring for each metric
                for metric in ['mi', 'logprob', 'tokens', 'cc']:
                    if metric in top_passed and top_passed[metric]:
                        refactoring_name = top_passed[metric]['name']
                        
                        # Find this specific refactoring to get its pass rate info
                        refactoring_data = None
                        for r in tuple_info['refactorings']:
                            if r['name'] == refactoring_name:
                                refactoring_data = r
                                break
                        
                        if refactoring_data:
                            tuple_summary[metric] = {
                                "refactoring_name": refactoring_name,
                                "rank": top_passed[metric]['rank'],
                                "score": top_passed[metric]['score'],
                                "pass_rate_before": refactoring_data['pass_rates']['before'],
                                "pass_rate_after": refactoring_data['pass_rates']['after'],
                                "maintains_pass_rate": refactoring_data['pass_rates']['maintained']
                            }
                        else:
                            tuple_summary[metric] = None
                    else:
                        tuple_summary[metric] = None
                
                # Add pass rate information for context
                passed_refactorings = [r for r in tuple_info['refactorings'] if r['pass_rates']['maintained'] is True]
                tuple_summary["total_refactorings"] = len(tuple_info['refactorings'])
                tuple_summary["passing_refactorings"] = len(passed_refactorings)
                tuple_summary["pass_rate_percentage"] = round((len(passed_refactorings) / len(tuple_info['refactorings'])) * 100, 1) if tuple_info['refactorings'] else 0
                
                cluster_summary["tuples"][tuple_name] = tuple_summary
            else:
                # No passing refactorings
                cluster_summary["tuples"][tuple_name] = {
                    "mi": None,
                    "logprob": None, 
                    "tokens": None,
                    "cc": None,
                    "total_refactorings": len(tuple_info['refactorings']),
                    "passing_refactorings": 0,
                    "pass_rate_percentage": 0.0
                }
        
        summary_data["clusters"][cluster_name] = cluster_summary
    
    # Write comprehensive summary
    output_file = "comprehensive_summary.json"
    with open(output_file, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    print(f"\nGenerated comprehensive summary: {output_file}")
    
    # Print some statistics
    total_tuples = sum(len(cluster["tuples"]) for cluster in summary_data["clusters"].values())
    tuples_with_passing = 0
    total_metrics = 0
    metrics_with_passing = 0
    
    for cluster in summary_data["clusters"].values():
        for tuple_data in cluster["tuples"].values():
            if tuple_data["passing_refactorings"] > 0:
                tuples_with_passing += 1
            
            for metric in ['mi', 'logprob', 'tokens', 'cc']:
                total_metrics += 1
                if tuple_data[metric] is not None:
                    metrics_with_passing += 1
    
    print(f"\nStatistics:")
    print(f"Total clusters: {len(summary_data['clusters'])}")
    print(f"Total tuples: {total_tuples}")
    print(f"Tuples with passing refactorings: {tuples_with_passing} ({tuples_with_passing/total_tuples*100:.1f}%)")
    print(f"Metrics with passing refactorings: {metrics_with_passing}/{total_metrics} ({metrics_with_passing/total_metrics*100:.1f}%)")

if __name__ == "__main__":
    main()
