// Single form submission version of the study
let tuplesData = [];
let sessionData = null;
let currentTupleId = null;
let timerInterval = null;
let startTime = null;
let currentViews = {
    'original': 'p1',
    'v1': 'p1',
    'v2': 'p1'
};

document.addEventListener('DOMContentLoaded', async function() {
    // Load session data
    sessionData = JSON.parse(localStorage.getItem('studySession'));
    
    if (!sessionData) {
        alert('No study session found. Redirecting to start page.');
        window.location.href = 'index.html';
        return;
    }
    
    // Initialize detailed responses array if not exists
    if (!sessionData.allResponses) {
        sessionData.allResponses = [];
    }
    
    // Display participant ID
    document.getElementById('participantId').textContent = sessionData.participantId;
    
    // Start timer
    startTimer();
    
    // Load tuples data
    await loadTuplesData();
    
    // Load current tuple
    loadCurrentTuple();
    
    // Setup event listeners
    setupEventListeners();
    
    // Setup keyboard shortcuts
    setupKeyboardShortcuts();
    
    // Setup synchronized scrolling
    setupSyncScroll();
    
    // Setup view buttons
    setupViewButtons();
});

async function loadTuplesData() {
    try {
        const response = await fetch('data/tuples_v2.json');
        tuplesData = await response.json();
        document.getElementById('loading').style.display = 'none';
    } catch (error) {
        console.error('Error loading tuples data:', error);
        alert('Error loading study data. Please refresh the page.');
    }
}

function loadCurrentTuple() {
    if (sessionData.currentIndex >= sessionData.assignedTuples.length) {
        showCompletionModal();
        return;
    }
    
    currentTupleId = sessionData.assignedTuples[sessionData.currentIndex];
    const tuple = tuplesData[currentTupleId];
    
    if (!tuple) {
        console.error('Tuple not found:', currentTupleId);
        return;
    }
    
    // Update progress
    const currentQuestion = sessionData.currentIndex + 1;
    document.getElementById('currentQuestion').textContent = currentQuestion;
    document.getElementById('progressFill').style.width = `${(currentQuestion / 10) * 100}%`;
    
    // Load default views for each panel
    updateCodePanel('original', currentViews.original, tuple);
    updateCodePanel('v1', currentViews.v1, tuple);
    updateCodePanel('v2', currentViews.v2, tuple);
    
    // Clear previous selection
    document.querySelectorAll('.choice-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // Load previous response if exists
    const existingResponse = sessionData.allResponses.find(r => r.tupleId === currentTupleId);
    if (existingResponse) {
        document.querySelector(`[data-choice="${existingResponse.choice.toLowerCase()}"]`).classList.add('selected');
        document.getElementById('nextBtn').disabled = false;
    } else {
        document.getElementById('nextBtn').disabled = true;
    }
    
    // Update navigation buttons
    document.getElementById('prevBtn').disabled = sessionData.currentIndex === 0;
    
    // Show submit button on last question
    if (sessionData.currentIndex === 9) {
        document.getElementById('nextBtn').style.display = 'none';
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.style.display = 'inline-block';
        submitBtn.disabled = !existingResponse;
        // Remove primary styling if disabled
        if (!existingResponse) {
            submitBtn.classList.remove('btn-primary');
            submitBtn.classList.add('btn-disabled');
        } else {
            submitBtn.classList.remove('btn-disabled');
            submitBtn.classList.add('btn-primary');
        }
    } else {
        document.getElementById('nextBtn').style.display = 'inline-block';
        document.getElementById('submitBtn').style.display = 'none';
    }
}

function updateCodePanel(panel, view, tuple) {
    let codeElementId;
    let content = '';
    
    // Determine which code element to update
    if (panel === 'original') {
        codeElementId = 'originalCode';
    } else if (panel === 'v1') {
        codeElementId = 'v1Code';
    } else {
        codeElementId = 'v2Code';
    }
    
    // Get the appropriate content based on view
    if (panel === 'original') {
        // Original panel only has p1, p2, p3
        if (view === 'p1') {
            content = tuple.files.original_p1 || tuple.files.original || '';
        } else if (view === 'p2') {
            content = tuple.files.original_p2 || tuple.files.original || '';
        } else if (view === 'p3') {
            content = tuple.files.original_p3 || tuple.files.original || '';
        }
    } else {
        // v1 and v2 panels have all, library, p1, p2, p3
        const versionKey = panel;
        if (view === 'all') {
            content = tuple.files[versionKey] || '';
        } else if (view === 'library') {
            content = tuple.files[`library_${versionKey}`] || '';
        } else if (view === 'p1') {
            content = tuple.files[`p1_${versionKey}`] || '';
        } else if (view === 'p2') {
            content = tuple.files[`p2_${versionKey}`] || '';
        } else if (view === 'p3') {
            content = tuple.files[`p3_${versionKey}`] || '';
        }
    }
    
    // Update the code element
    const codeElement = document.getElementById(codeElementId);
    codeElement.textContent = content;
    
    // Apply syntax highlighting
    Prism.highlightElement(codeElement);
    
    // Reset scroll position
    const wrapper = codeElement.closest('.code-wrapper');
    if (wrapper) {
        wrapper.scrollTop = 0;
    }
}

function setupViewButtons() {
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const panel = this.dataset.panel;
            const view = this.dataset.view;
            
            // Update active state for buttons in this panel
            document.querySelectorAll(`.view-btn[data-panel="${panel}"]`).forEach(b => {
                b.classList.remove('active');
            });
            this.classList.add('active');
            
            // Update current view
            currentViews[panel] = view;
            
            // Update code display
            const tuple = tuplesData[currentTupleId];
            if (tuple) {
                updateCodePanel(panel, view, tuple);
            }
        });
    });
}

function setupEventListeners() {
    // Choice buttons
    document.querySelectorAll('.choice-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const choice = this.dataset.choice;
            selectChoice(choice);
        });
    });
    
    // Navigation buttons
    document.getElementById('prevBtn').addEventListener('click', () => {
        if (sessionData.currentIndex > 0) {
            sessionData.currentIndex--;
            saveSession();
            loadCurrentTuple();
        }
    });
    
    document.getElementById('nextBtn').addEventListener('click', () => {
        if (sessionData.currentIndex < 9) {
            sessionData.currentIndex++;
            saveSession();
            loadCurrentTuple();
        }
    });
    
    document.getElementById('submitBtn').addEventListener('click', () => {
        showCompletionModal();
    });
    
    // Modal buttons
    document.getElementById('openFormBtn').addEventListener('click', () => {
        openPrefilledGoogleForm();
    });
    
    document.getElementById('downloadBtn').addEventListener('click', () => {
        downloadResponses();
    });
    
    // Font size controls
    setupFontSizeControls();
}

function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        if (e.key === '1') {
            selectChoice('v1');
        } else if (e.key === '2') {
            selectChoice('v2');
        } else if (e.key === 'Enter' && !document.getElementById('nextBtn').disabled) {
            if (sessionData.currentIndex < 9) {
                document.getElementById('nextBtn').click();
            } else if (document.getElementById('submitBtn') && !document.getElementById('submitBtn').disabled) {
                document.getElementById('submitBtn').click();
            }
        }
    });
}

function selectChoice(choice) {
    // Update UI to show selection
    document.querySelectorAll('.choice-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    const selectedBtn = document.querySelector(`[data-choice="${choice}"]`);
    if (selectedBtn) {
        selectedBtn.classList.add('selected');
    }
    
    // Update or add response
    const existingIndex = sessionData.allResponses.findIndex(r => r.tupleId === currentTupleId);
    const responseData = {
        tupleId: currentTupleId,
        choice: choice.toUpperCase(),
        trialNumber: sessionData.currentIndex + 1,
        timestamp: new Date().toISOString()
    };
    
    if (existingIndex >= 0) {
        sessionData.allResponses[existingIndex] = responseData;
    } else {
        sessionData.allResponses.push(responseData);
    }
    
    saveSession();
    
    // Enable next/submit button
    if (sessionData.currentIndex === 9) {
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = false;
        submitBtn.classList.remove('btn-disabled');
        submitBtn.classList.add('btn-primary');
    } else {
        document.getElementById('nextBtn').disabled = false;
    }
}

function setupSyncScroll() {
    const syncCheckbox = document.getElementById('syncScroll');
    const codeWrappers = document.querySelectorAll('.code-wrapper');
    
    let isScrolling = false;
    
    codeWrappers.forEach(wrapper => {
        wrapper.addEventListener('scroll', function() {
            if (!syncCheckbox.checked || isScrolling) return;
            
            isScrolling = true;
            const scrollPercent = this.scrollTop / (this.scrollHeight - this.clientHeight);
            
            codeWrappers.forEach(otherWrapper => {
                if (otherWrapper !== this) {
                    otherWrapper.scrollTop = scrollPercent * (otherWrapper.scrollHeight - otherWrapper.clientHeight);
                }
            });
            
            setTimeout(() => { isScrolling = false; }, 10);
        });
    });
}

function startTimer() {
    startTime = Date.now();
    timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        document.getElementById('timer').textContent = 
            `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }, 1000);
}

function saveSession() {
    localStorage.setItem('studySession', JSON.stringify(sessionData));
}

function showCompletionModal() {
    clearInterval(timerInterval);
    
    // Ensure all 10 responses are collected
    if (sessionData.allResponses.length < 10) {
        alert('Please complete all 10 questions before submitting.');
        return;
    }
    
    // Show modal
    document.getElementById('submitModal').style.display = 'flex';
}

function openPrefilledGoogleForm() {
    // Google Form base URL
    const FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSfY4IV_NLRYtkEr8mYFxfXzgZPHcHoYego6yQ7GStpHbfHWUA/viewform';
    
    // Actual entry IDs from the Google Form
    const ENTRY_IDS = {
        userId: 'entry.1958938177',  // UserID field
        email: 'entry.792270821',    // Email field  
        name: 'entry.1585743737',    // Name field
        // Trial 1
        trial1_tupleId: 'entry.1538445591',
        trial1_pairId: 'entry.306224226',
        trial1_choice: 'entry.1092031299',
        // Trial 2
        trial2_tupleId: 'entry.487065090',
        trial2_pairId: 'entry.165561073',
        trial2_choice: 'entry.812388703',
        // Trial 3
        trial3_tupleId: 'entry.1277091152',
        trial3_pairId: 'entry.325557872',
        trial3_choice: 'entry.2000752445',
        // Trial 4
        trial4_tupleId: 'entry.2140505775',
        trial4_pairId: 'entry.1718924254',
        trial4_choice: 'entry.720209224',
        // Trial 5
        trial5_tupleId: 'entry.4308478',
        trial5_pairId: 'entry.198690717',
        trial5_choice: 'entry.136166959',
        // Trial 6
        trial6_tupleId: 'entry.1717139691',
        trial6_pairId: 'entry.1130745721',
        trial6_choice: 'entry.1756691659',
        // Trial 7
        trial7_tupleId: 'entry.795772895',
        trial7_pairId: 'entry.600609903',
        trial7_choice: 'entry.547640540',
        // Trial 8
        trial8_tupleId: 'entry.778698876',
        trial8_pairId: 'entry.1778742953',
        trial8_choice: 'entry.659602518',
        // Trial 9
        trial9_tupleId: 'entry.2132146432',
        trial9_pairId: 'entry.2038252166',
        trial9_choice: 'entry.1305399604',
        // Trial 10
        trial10_tupleId: 'entry.867453469',
        trial10_pairId: 'entry.499398113',
        trial10_choice: 'entry.529410553',
        // Other fields
        trialNumber: 'entry.435207678',  // Trial Number field
        timestamp: 'entry.141633008'     // Timestamp field
    };
    
    // Build URL parameters
    const params = new URLSearchParams();
    
    // Add user info
    params.append(ENTRY_IDS.userId, sessionData.participantId);
    params.append(ENTRY_IDS.email, sessionData.email || '');
    params.append(ENTRY_IDS.name, sessionData.name || '');
    
    // Sort responses by trial number
    const sortedResponses = sessionData.allResponses.sort((a, b) => a.trialNumber - b.trialNumber);
    
    // Add each trial's data
    sortedResponses.forEach((response, index) => {
        const trialNum = index + 1;
        
        // Add TupleID for this trial
        if (ENTRY_IDS[`trial${trialNum}_tupleId`]) {
            params.append(ENTRY_IDS[`trial${trialNum}_tupleId`], response.tupleId.toString());
        }
        
        // Add PairID (always 1 since we're comparing v1 vs v2)
        if (ENTRY_IDS[`trial${trialNum}_pairId`]) {
            params.append(ENTRY_IDS[`trial${trialNum}_pairId`], '1');
        }
        
        // Add Choice (V1 or V2)
        if (ENTRY_IDS[`trial${trialNum}_choice`]) {
            params.append(ENTRY_IDS[`trial${trialNum}_choice`], response.choice);
        }
    });
    
    // Add timestamp
    if (ENTRY_IDS.timestamp) {
        params.append(ENTRY_IDS.timestamp, new Date().toISOString());
    }
    
    // Open the pre-filled form
    const fullUrl = `${FORM_URL}?${params.toString()}`;
    
    // Show alert with instructions
    alert('A new tab will open with your responses pre-filled in the Google Form.\n\n' +
          'Please review your responses and click the Submit button at the bottom of the form.');
    
    window.open(fullUrl, '_blank');
    
    // Also save a backup
    downloadResponses();
}

function downloadResponses() {
    // Prepare CSV data
    const csvRows = [
        ['UserID', 'Name', 'Email', 'TrialNumber', 'TupleID', 'Choice', 'Timestamp']
    ];
    
    sessionData.allResponses
        .sort((a, b) => a.trialNumber - b.trialNumber)
        .forEach(response => {
            csvRows.push([
                sessionData.participantId,
                sessionData.name || '',
                sessionData.email || '',
                response.trialNumber,
                response.tupleId,
                response.choice,
                response.timestamp
            ]);
        });
    
    const csvContent = csvRows.map(row => 
        row.map(cell => {
            const cellStr = String(cell);
            return cellStr.includes(',') ? `"${cellStr}"` : cellStr;
        }).join(',')
    ).join('\n');
    
    // Download CSV
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `study_responses_${sessionData.participantId}_${Date.now()}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    // Also download JSON backup
    const jsonData = {
        participantId: sessionData.participantId,
        name: sessionData.name || '',
        email: sessionData.email || '',
        startTime: sessionData.startTime,
        completionTime: new Date().toISOString(),
        responses: sessionData.allResponses
    };
    
    const jsonBlob = new Blob([JSON.stringify(jsonData, null, 2)], { type: 'application/json' });
    const jsonUrl = URL.createObjectURL(jsonBlob);
    const jsonLink = document.createElement('a');
    jsonLink.href = jsonUrl;
    jsonLink.download = `study_responses_${sessionData.participantId}_${Date.now()}.json`;
    document.body.appendChild(jsonLink);
    jsonLink.click();
    document.body.removeChild(jsonLink);
    URL.revokeObjectURL(jsonUrl);
}

function setupFontSizeControls() {
    let currentFontSize = 14; // Default font size in px
    const minSize = 10;
    const maxSize = 20;
    
    const fontSizeDisplay = document.getElementById('fontSize');
    const decreaseBtn = document.getElementById('fontDecrease');
    const increaseBtn = document.getElementById('fontIncrease');
    
    // Load saved font size from localStorage
    const savedSize = localStorage.getItem('codeFontSize');
    if (savedSize) {
        currentFontSize = parseInt(savedSize);
    }
    
    updateFontSize(currentFontSize);
    
    decreaseBtn.addEventListener('click', () => {
        if (currentFontSize > minSize) {
            currentFontSize--;
            updateFontSize(currentFontSize);
        }
    });
    
    increaseBtn.addEventListener('click', () => {
        if (currentFontSize < maxSize) {
            currentFontSize++;
            updateFontSize(currentFontSize);
        }
    });
    
    function updateFontSize(size) {
        // Update all code elements
        document.querySelectorAll('.code-wrapper pre').forEach(pre => {
            pre.style.fontSize = `${size}px`;
        });
        
        // Update display
        fontSizeDisplay.textContent = `${size}px`;
        
        // Update button states
        decreaseBtn.disabled = size <= minSize;
        increaseBtn.disabled = size >= maxSize;
        
        // Save preference
        localStorage.setItem('codeFontSize', size.toString());
    }
}