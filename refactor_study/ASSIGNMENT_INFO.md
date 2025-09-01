# User Study Assignment System

## Overview
The refactoring study uses `tuples_v4_no_docs.json` which contains 45 tuple comparisons organized into 10 clusters (original problems).

## Current Implementation

### Data Files
- **Tuple Data**: `data/tuples_v4_no_docs.json` (45 tuples, 10 clusters)
- **User Assignments (No Duplicates)**: `data/user_assignments_no_duplicates.json`
- **CSV Export**: `user_study_assignments_no_duplicates.csv`

### Key Features
1. **30 Participants**: Each with a unique ID (e.g., UE064AED19)
2. **10 Comparisons per User**: Each user sees exactly 10 tuple comparisons
3. **No Duplicate Clusters**: Each user sees one comparison from each of the 10 clusters
4. **Balanced Distribution**: Tuples are distributed evenly across participants

### Assignment Algorithm
The `generate_assignments.py` script:
1. Groups all 45 tuples by their cluster (10 clusters total)
2. For each participant:
   - Selects one tuple from each cluster
   - Prioritizes less-used tuples for balance
   - Shuffles the order randomly
3. Ensures no participant sees the same original problem twice

### Cluster Distribution
- **cluster_0**: Tree algorithms (cc_python_29, cc_python_19, cc_python_13)
- **cluster_1**: String operations (cc_python_2, cc_python_27, cc_python_5)
- **cluster_2**: Data structures (cc_python_5, cc_python_26, cc_python_22)
- **cluster_3**: Graph algorithms (cc_python_16, cc_python_19, cc_python_23, etc.)
- **cluster_4**: Dynamic programming (cc_python_28, cc_python_4, cc_python_11)
- **cluster_5**: Recursion problems
- **cluster_6**: Array operations
- **cluster_7**: Math problems
- **cluster_8**: Search algorithms
- **cluster_9**: Sorting algorithms

### Loading Priority in app.js
1. `user_assignments_no_duplicates.json` (primary - ensures unique clusters)
2. `user_assignments_final.json` (fallback)
3. `user_assignments_v3.json` (fallback)
4. `user_assignments.json` (fallback)
5. Dynamic assignment (last resort - also ensures unique clusters)

## Usage

### Generate New Assignments
```bash
python3 generate_assignments.py
python3 generate_csv_assignments.py
```

### Access Study
Users access the study via: `https://zzigak.github.io/refactor_study/?id=USER_ID`

Example: `https://zzigak.github.io/refactor_study/?id=UE064AED19`

## Verification
Each user's assignments are verified to have:
- Exactly 10 tuple comparisons
- 10 unique clusters (no duplicate original problems)
- Proper randomization of presentation order