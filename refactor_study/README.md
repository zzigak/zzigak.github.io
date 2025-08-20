# Refactoring Preference User Study Website

A modern, minimalistic web application for conducting user studies on code refactoring preferences.

## Features

- **Clean Interface**: Side-by-side comparison of original code with two refactored versions
- **Smart Assignment**: Balanced tuple distribution across participants
- **Progress Tracking**: Real-time progress bar and timer
- **Keyboard Shortcuts**: Quick selection using keys 1, 2, and 0
- **Synchronized Scrolling**: Optional synchronized scrolling across code panels
- **Data Export**: Download responses as JSON or submit to Google Forms
- **Responsive Design**: Works on desktop and tablet devices
- **Syntax Highlighting**: Python code highlighting using Prism.js

## Quick Start

### Local Testing

1. Navigate to the docs directory:
```bash
cd docs
```

2. Start a local server:
```bash
python3 -m http.server 8000
```

3. Open in browser:
```
http://localhost:8000
```

## File Structure

```
docs/
├── index.html          # Landing page
├── study.html          # Main study interface
├── test.html           # Testing instructions
├── css/
│   └── style.css       # Modern minimalistic styles
├── js/
│   ├── app.js          # Landing page logic
│   └── study.js        # Study interface logic
└── data/
    └── tuples.json     # Code samples data
```

## Study Flow

1. Participant arrives at landing page
2. Clicks "Start Study" → generates unique ID
3. System assigns 10 tuples using balanced distribution
4. Participant reviews each tuple:
   - Original code (green border)
   - Version 1 refactoring
   - Version 2 refactoring
5. Selects preference (v1, v2, or no preference)
6. Navigates through all 10 questions
7. Submits responses and downloads data

## Customization

### Google Forms Integration

Edit `js/study.js` line ~240:
```javascript
const googleFormUrl = 'https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform';
// Add your form entry IDs
```

### Styling

Modern color scheme defined in CSS variables:
- Primary: #2563eb (blue)
- Success: #10b981 (green)
- Original code: #ecfdf5 (light green background)

## Deployment

### GitHub Pages

1. Push to repository
2. Settings → Pages → Source: /docs folder
3. Access at: `https://[username].github.io/[repo]/`

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Data Collection

Responses are stored in localStorage and include:
- Participant ID
- Tuple assignments
- Choice for each tuple
- Timestamps
- Session duration

## License

For research purposes - see main repository for details.