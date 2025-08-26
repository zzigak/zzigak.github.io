#!/usr/bin/env python3
"""
Remove docstrings from library files in the tuples data.
"""

import json
import re
import ast
import textwrap

def remove_docstrings_from_code(code):
    """Remove docstrings from Python code while preserving comments and other strings."""
    if not code:
        return code
    
    # Use regex to remove only triple-quoted docstrings
    # This preserves comments that start with #
    
    lines = code.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Check if this line starts a triple-quoted string
        if '"""' in stripped or "'''" in stripped:
            # Determine if this is likely a docstring
            # (appears after def, class, or at module level)
            prev_line = lines[i-1].strip() if i > 0 else ""
            
            # Check if previous line is a function/class definition
            is_after_def = prev_line.startswith(('def ', 'class ', 'async def '))
            is_after_colon = prev_line.endswith(':')
            
            # Check if it's at the module level (beginning of file or after imports)
            is_module_level = i == 0 or all(
                l.strip() == '' or l.strip().startswith(('import ', 'from ', '#'))
                for l in lines[:i]
            )
            
            if (is_after_def and is_after_colon) or is_module_level:
                # This looks like a docstring, skip it
                quote_type = '"""' if '"""' in stripped else "'''"
                
                # If it's a single-line docstring
                if stripped.count(quote_type) >= 2:
                    # Skip this line
                    i += 1
                    continue
                
                # Multi-line docstring - skip until closing quotes
                i += 1
                while i < len(lines):
                    if quote_type in lines[i]:
                        i += 1
                        break
                    i += 1
                continue
        
        # Not a docstring, keep the line (including comments)
        result_lines.append(line)
        i += 1
    
    return '\n'.join(result_lines)

def process_tuples_data(input_file='data/tuples_v3.json', output_file='data/tuples_v4_no_docs.json'):
    """Process tuples data to remove docstrings from all library files."""
    
    print(f"Loading data from {input_file}...")
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    print(f"Processing {len(data)} tuples...")
    
    modified_count = 0
    for i, tuple_data in enumerate(data):
        if i % 10 == 0:
            print(f"  Processing tuple {i+1}/{len(data)}...")
        
        files = tuple_data.get('files', {})
        modified = False
        
        # Process library files
        library_keys = ['library_v1', 'library_v2']
        for key in library_keys:
            if key in files and files[key]:
                original = files[key]
                cleaned = remove_docstrings_from_code(original)
                if cleaned != original:
                    files[key] = cleaned
                    modified = True
        
        # Process combined files (v1 and v2) which include library code
        combined_keys = ['v1', 'v2']
        for key in combined_keys:
            if key in files and files[key]:
                original = files[key]
                # The combined files have library + programs, need to handle carefully
                cleaned = remove_docstrings_from_code(original)
                if cleaned != original:
                    files[key] = cleaned
                    modified = True
        
        # Process individual program files that might have library code
        for key in files.keys():
            if key.startswith('p') and key.endswith(('_v1', '_v2')):
                original = files[key]
                cleaned = remove_docstrings_from_code(original)
                if cleaned != original:
                    files[key] = cleaned
                    modified = True
        
        if modified:
            modified_count += 1
    
    print(f"\nModified {modified_count} tuples")
    
    # Save the processed data
    print(f"Saving to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Done!")
    return data

def verify_changes(original_file='data/tuples_v3.json', processed_file='data/tuples_v4_no_docs.json'):
    """Verify the changes made by comparing a sample."""
    
    with open(original_file, 'r') as f:
        original = json.load(f)
    
    with open(processed_file, 'r') as f:
        processed = json.load(f)
    
    # Check the first tuple with library code
    for i in range(min(5, len(original))):
        orig_lib_v1 = original[i]['files'].get('library_v1', '')
        proc_lib_v1 = processed[i]['files'].get('library_v1', '')
        
        if orig_lib_v1 != proc_lib_v1:
            print(f"\n--- Example changes in tuple {i} (library_v1) ---")
            
            # Count docstrings removed
            orig_docstring_count = orig_lib_v1.count('"""') + orig_lib_v1.count("'''")
            proc_docstring_count = proc_lib_v1.count('"""') + proc_lib_v1.count("'''")
            
            print(f"Original docstring markers: {orig_docstring_count}")
            print(f"Processed docstring markers: {proc_docstring_count}")
            print(f"Removed: {orig_docstring_count - proc_docstring_count}")
            
            # Show first 500 chars of each
            print("\nOriginal (first 500 chars):")
            print(orig_lib_v1[:500])
            print("\nProcessed (first 500 chars):")
            print(proc_lib_v1[:500])
            
            break

if __name__ == "__main__":
    # Process the data
    process_tuples_data()
    
    # Verify the changes
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    verify_changes()