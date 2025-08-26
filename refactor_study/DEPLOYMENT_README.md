# Refactoring Study Deployment Guide

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
