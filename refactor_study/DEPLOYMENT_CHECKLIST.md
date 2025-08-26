# 🚀 Deployment Checklist for Refactoring Study

## ✅ Pre-Deployment Verification

### Core Files
- [x] `index.html` - Landing page with instructions
- [x] `study_single_form.html` - Main study interface  
- [x] `css/style.css` - Styling
- [x] `js/study_single_form.js` - Study logic (uses tuples_v4_no_docs.json)
- [x] `js/app.js` - Landing page logic

### Data Files
- [x] `data/tuples_v4_no_docs.json` - Study data WITHOUT docstrings
- [x] `data/user_assignments_final.json` - User-to-tuple mappings
- [x] `data/user_assignments_enhanced.json` - Detailed assignment info

### Documentation
- [x] `user_study_deployment_info.json` - Complete user assignments with metrics
- [x] `user_study_assignments.csv` - Simple CSV for reference
- [x] `DEPLOYMENT_README.md` - Deployment guide

## 📋 Key Features Implemented

### Study Interface
- [x] Side-by-side comparison of Original, V1, and V2 code
- [x] View switching (ALL, P1, P2, P3, Library)
- [x] No default selection (prevents bias)
- [x] Progress tracking (1-10 questions)
- [x] Font size adjustment
- [x] Mobile blocking (requires desktop)

### Data Collection
- [x] Google Form integration with pre-filled responses
- [x] Local backup (CSV and JSON download)
- [x] Session persistence (can go back/forward)
- [x] Completion validation (all 10 must be answered)

### Debug Mode
- [x] Hidden by default
- [x] Accessible only with secret key: `debugKey=xR9mK2nP7qL4wZ8v`
- [x] Shows tuple IDs, metrics, pair types
- [x] Final summary of all choices

### Important Updates
- [x] Docstrings removed from all library code
- [x] Comments preserved (# comments)
- [x] Instructions clarify to focus on NEW functions only
- [x] Instructions clarify to ignore documentation quality
- [x] Views reset to ALL when moving between questions

## 🔗 User Links Format

Regular user link:
```
https://zzigak.github.io/refactor_study/?id=USER_ID
```

Debug link (for testing):
```
https://zzigak.github.io/refactor_study/?id=USER_ID&debugKey=xR9mK2nP7qL4wZ8v
```

## 📊 Study Statistics

- **Total Users:** 30
- **Questions per User:** 10  
- **Total Unique Tuples:** 45
- **Pair Types:** 
  - mi_vs_logprob (comparing MI vs LogProb refactorings)
  - mi_vs_tokens (comparing MI vs Token-based refactorings)
  - logprob_vs_tokens (comparing LogProb vs Token-based refactorings)

## 🎯 Deployment Steps

1. **Push to GitHub:**
   ```bash
   git add refactor_study/
   git commit -m "Deploy refactoring study"
   git push origin main
   ```

2. **Verify deployment:**
   - Test a user link
   - Test debug mode
   - Complete a full 10-question run
   - Verify Google Form submission works

3. **Share links:**
   - Send each user their unique link from `user_study_deployment_info.json`
   - DO NOT share debug links with participants

## ⚠️ Important Reminders

1. **Users should focus on NEW functions only** - not existing extracted functions
2. **Documentation quality should be ignored** - focus on functionality
3. **Each user has a unique set of 10 tuples** - balanced across pair types
4. **Desktop/laptop required** - mobile devices are blocked
5. **Data is saved locally AND to Google Forms** - dual backup

## 📈 Post-Study Analysis

After collecting responses:
```bash
# Analyze individual user results
python3 analyze_results.py study_responses_USER_ID.csv

# Or analyze JSON backup
python3 analyze_results.py study_responses_USER_ID.json
```

## ✅ READY FOR DEPLOYMENT!

All systems checked and ready. The study can be deployed to:
`https://zzigak.github.io/refactor_study/`