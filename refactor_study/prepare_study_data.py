#!/usr/bin/env python3
"""
Prepare study data from tuple_human_evals for the website.
Creates 3 metric pairs per tuple (MI vs Logprob, MI vs Tokens, Logprob vs Tokens).
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def load_cluster_rankings(cluster_path: Path) -> Dict:
    """Load cluster rankings from JSON file."""
    rankings_file = cluster_path / f"{cluster_path.name}_rankings.json"
    if rankings_file.exists():
        with open(rankings_file, 'r') as f:
            return json.load(f)
    return None

def load_refactoring_files(tuple_path: Path, refactoring_name: str) -> Dict[str, str]:
    """Load all files for a specific refactoring."""
    refactoring_path = tuple_path / refactoring_name
    files = {}
    
    if not refactoring_path.exists():
        return files
    
    # Load library
    library_path = refactoring_path / 'library_helpers.py'
    if library_path.exists():
        with open(library_path, 'r') as f:
            files['library'] = f.read()
    else:
        files['library'] = ""
    
    # Load individual refactored programs
    programs = []
    for prog_file in sorted(refactoring_path.glob('*_refactored.py')):
        with open(prog_file, 'r') as f:
            node_name = prog_file.stem.replace('_refactored', '')
            programs.append((node_name, f.read()))
    
    files['programs'] = programs
    
    # Create combined content (library + all programs)
    combined = f"# Library Functions\n{files['library']}\n\n"
    combined += "# =" * 40 + "\n\n"
    
    for i, (node, content) in enumerate(programs, 1):
        combined += f"# Program {i}: {node}\n"
        combined += content
        if i < len(programs):
            combined += "\n\n" + "# -" * 40 + "\n\n"
    
    files['combined'] = combined
    
    return files

def load_original_files(tuple_path: Path) -> Dict[str, str]:
    """Load original program files and problem descriptions."""
    files = {}
    
    # Load combined original file
    original_file = tuple_path / 'original.py'
    if original_file.exists():
        with open(original_file, 'r') as f:
            files['original'] = f.read()
    
    # Load individual original programs
    original_dir = tuple_path / 'original'
    if original_dir.exists():
        programs = []
        for prog_file in sorted(original_dir.glob('*.py')):
            with open(prog_file, 'r') as f:
                node_name = prog_file.stem
                programs.append((node_name, f.read()))
        files['programs'] = programs
    
    return files

def create_tuple_data(cluster_path: Path, tuple_name: str, rankings: Dict) -> List[Dict]:
    """Create data entries for all metric pairs of a tuple."""
    tuple_path = cluster_path / tuple_name
    
    # Find the tuple's ranking data
    tuple_ranking = None
    for t in rankings.get('tuples', []):
        if t['tuple_name'] == tuple_name:
            tuple_ranking = t
            break
    
    if not tuple_ranking:
        print(f"Warning: No ranking data for {tuple_name}")
        return []
    
    # Get best refactorings for each metric (only considering passing refactorings)
    best_refactorings = tuple_ranking.get('top_refactorings_passed', 
                                         tuple_ranking.get('top_refactorings_overall', {}))
    
    if not best_refactorings:
        print(f"Warning: No top refactorings for {tuple_name}")
        return []
    
    # Load original files once (shared across all pairs)
    original_files = load_original_files(tuple_path)
    
    # Create pairs for different metrics
    metric_pairs = [
        ('mi', 'logprob', 'mi_vs_logprob'),
        ('mi', 'tokens', 'mi_vs_tokens'),
        ('logprob', 'tokens', 'logprob_vs_tokens')
    ]
    
    tuple_data = []
    
    for metric1, metric2, pair_type in metric_pairs:
        ref1 = best_refactorings.get(metric1, {})
        ref2 = best_refactorings.get(metric2, {})
        
        if not ref1 or not ref2:
            continue
            
        # Skip if both metrics chose the same refactoring
        if ref1.get('name') == ref2.get('name'):
            continue
        
        # Load refactoring files
        ref1_files = load_refactoring_files(tuple_path, ref1['name'])
        ref2_files = load_refactoring_files(tuple_path, ref2['name'])
        
        if not ref1_files or not ref2_files:
            continue
        
        # Create file structure for website
        files = {
            'original': original_files.get('original', ''),
            'v1': ref1_files.get('combined', ''),
            'v2': ref2_files.get('combined', ''),
            'library_v1': ref1_files.get('library', ''),
            'library_v2': ref2_files.get('library', ''),
        }
        
        # Add individual original programs
        if 'programs' in original_files:
            for i, (node_name, content) in enumerate(original_files['programs'], 1):
                files[f'original_p{i}'] = content
        
        # Add individual refactored programs
        if 'programs' in ref1_files:
            for i, (node_name, content) in enumerate(ref1_files['programs'], 1):
                files[f'p{i}_v1'] = content
        
        if 'programs' in ref2_files:
            for i, (node_name, content) in enumerate(ref2_files['programs'], 1):
                files[f'p{i}_v2'] = content
        
        # Create entry for this pair
        entry = {
            'cluster': cluster_path.name,
            'tuple': tuple_name,
            'name': f"{cluster_path.name}/{tuple_name}",
            'pair_type': pair_type,
            'v1_metric': metric1,
            'v2_metric': metric2,
            'v1_refactoring': ref1['name'],
            'v2_refactoring': ref2['name'],
            'v1_score': ref1.get('score', 0),
            'v2_score': ref2.get('score', 0),
            'files': files
        }
        
        tuple_data.append(entry)
    
    return tuple_data

def process_all_tuples() -> List[Dict]:
    """Process all tuples from tuple_human_evals directory."""
    base_path = Path('tuple_human_evals')
    all_data = []
    tuple_id = 0
    
    # Process each cluster
    for cluster_dir in sorted(base_path.glob('cluster_*')):
        if not cluster_dir.is_dir():
            continue
        
        print(f"Processing {cluster_dir.name}...")
        
        # Load cluster rankings
        rankings = load_cluster_rankings(cluster_dir)
        if not rankings:
            print(f"  Warning: No rankings found for {cluster_dir.name}")
            continue
        
        # Process each tuple in the cluster
        for tuple_dir in sorted(cluster_dir.glob('tuple_*')):
            if not tuple_dir.is_dir():
                continue
            
            tuple_name = tuple_dir.name
            print(f"  Processing {tuple_name}...")
            
            # Create data for all metric pairs
            tuple_data = create_tuple_data(cluster_dir, tuple_name, rankings)
            
            # Add ID to each entry
            for entry in tuple_data:
                entry['id'] = tuple_id
                tuple_id += 1
                all_data.append(entry)
            
            if tuple_data:
                print(f"    Created {len(tuple_data)} pairs")
            else:
                print(f"    No pairs created (possibly same refactoring for different metrics)")
    
    return all_data

def main():
    """Main function to generate study data."""
    print("Preparing study data from tuple_human_evals...")
    
    # Process all tuples
    study_data = process_all_tuples()
    
    # Save to JSON file
    output_file = Path('data/tuples_v3.json')
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(study_data, f, indent=2)
    
    # Print summary
    print(f"\nSummary:")
    print(f"Total pairs created: {len(study_data)}")
    
    # Count by pair type
    pair_types = {}
    tuples_processed = set()
    for entry in study_data:
        pair_type = entry['pair_type']
        pair_types[pair_type] = pair_types.get(pair_type, 0) + 1
        tuples_processed.add(entry['tuple'])
    
    print(f"Unique tuples: {len(tuples_processed)}")
    for pair_type, count in sorted(pair_types.items()):
        print(f"  {pair_type}: {count}")
    
    print(f"\nData saved to {output_file}")

if __name__ == "__main__":
    main()