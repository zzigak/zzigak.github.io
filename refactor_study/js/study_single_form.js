// Single form submission version of the study
let tuplesData = [];
let sessionData = null;
let currentTupleId = null;
let timerInterval = null;
let startTime = null;
let currentViews = {
    'original': 'all',
    'v1': 'all',
    'v2': 'all'
};

// Check if debug mode is enabled via URL parameter with secret key
const urlParams = new URLSearchParams(window.location.search);
const debugKey = urlParams.get('debugKey');
const DEBUG_SECRET = 'xR9mK2nP7qL4wZ8v'; // Secret key for debug access
const debugMode = debugKey === DEBUG_SECRET;

document.addEventListener('DOMContentLoaded', async function() {
    // Show debug elements if debug mode is enabled
    if (debugMode) {
        const debugInfo = document.getElementById('debugInfo');
        if (debugInfo) {
            debugInfo.style.display = 'block';
        }
        console.log('Debug mode enabled');
    }
    
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
    
    // Setup view buttons
    setupViewButtons();
    
    // Setup tab navigation
    setupTabNavigation();
});

async function loadTuplesData() {
    try {
        const response = await fetch('data/tuples_v4_no_docs.json');
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
    
    // Reset views to 'all' when transitioning to a new tuple
    currentViews = {
        'original': 'all',
        'v1': 'all',
        'v2': 'all'
    };
    
    // Reset view buttons to 'all' state
    document.querySelectorAll('.view-btn').forEach(btn => {
        if (btn.dataset.view === 'all') {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Update progress
    const currentQuestion = sessionData.currentIndex + 1;
    document.getElementById('currentQuestion').textContent = currentQuestion;
    document.getElementById('progressFill').style.width = `${(currentQuestion / 10) * 100}%`;
    
    // Update debug info only if in debug mode
    if (debugMode) {
        const debugInfo = document.getElementById('debugInfo');
        if (debugInfo) {
            // Map pair_type to numeric pairId
            const pairTypeToId = {
                'mi_vs_logprob': 1,
                'mi_vs_tokens': 2,
                'logprob_vs_tokens': 3
            };
            
            document.getElementById('debugTupleId').textContent = currentTupleId;
            document.getElementById('debugTupleName').textContent = tuple.tuple || 'N/A';
            document.getElementById('debugCluster').textContent = tuple.cluster || 'N/A';
            document.getElementById('debugPairType').textContent = tuple.pair_type || 'N/A';
            document.getElementById('debugPairId').textContent = pairTypeToId[tuple.pair_type] || 'N/A';
            document.getElementById('debugV1Metric').textContent = tuple.v1_metric || 'N/A';
            document.getElementById('debugV1Refactoring').textContent = tuple.v1_refactoring || 'N/A';
            document.getElementById('debugV2Metric').textContent = tuple.v2_metric || 'N/A';
            document.getElementById('debugV2Refactoring').textContent = tuple.v2_refactoring || 'N/A';
            console.log('Debug info updated:', tuple);
        }
    }
    
    // Load default views for each panel (now always 'all')
    updateCodePanel('original', currentViews.original, tuple);
    updateCodePanel('v1', currentViews.v1, tuple);
    updateCodePanel('v2', currentViews.v2, tuple);
    
    // Extract and display existing functions
    extractAndDisplayExistingFunctions(tuple);
    
    // Clear previous selection and ensure no default selection
    document.querySelectorAll('.choice-btn').forEach(btn => {
        btn.classList.remove('selected');
        btn.blur(); // Remove any focus
    });
    
    // Clear argument text area
    document.getElementById('argumentText').value = '';
    
    // Load previous response if exists
    const existingResponse = sessionData.allResponses.find(r => r.tupleId === currentTupleId);
    if (existingResponse) {
        const btnToSelect = document.querySelector(`[data-choice="${existingResponse.choice.toLowerCase()}"]`);
        if (btnToSelect) {
            btnToSelect.classList.add('selected');
        }
        // Restore argument text if exists
        if (existingResponse.argument) {
            document.getElementById('argumentText').value = existingResponse.argument;
        }
        checkIfCanProceed();
    } else {
        // Ensure no selection and next button is disabled for new questions
        document.getElementById('nextBtn').disabled = true;
        if (debugMode) {
            console.log('No existing response for tuple', currentTupleId, '- buttons should be unselected');
        }
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
        // Original panel has all, p1, p2, p3
        if (view === 'all') {
            content = tuple.files.original || '';
        } else if (view === 'p1') {
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
            // For ALL view, exclude retrieved functions
            const fullCode = tuple.files[versionKey] || '';
            if (fullCode) {
                const lines = fullCode.split('\n');
                const filteredLines = [];
                let inRetrievedSection = false;
                
                for (const line of lines) {
                    // Check for section markers
                    if (line.includes('RETRIEVED HELPER FUNCTIONS') || line.includes('Retrieved Helper Functions')) {
                        inRetrievedSection = true;
                    } else if (line.includes('NEW HELPER FUNCTIONS') || line.includes('New Helper Functions') || 
                               line.includes('NEW FUNCTIONS') || line.includes('New Functions') ||
                               line.includes('# P1:') || line.includes('# P2:') || line.includes('# P3:') ||
                               line.includes('# Problem 1') || line.includes('# Problem 2') || line.includes('# Problem 3')) {
                        inRetrievedSection = false;
                        filteredLines.push(line);
                    } else if (!inRetrievedSection) {
                        filteredLines.push(line);
                    }
                }
                
                content = filteredLines.join('\n');
            } else {
                content = '';
            }
        } else if (view === 'library') {
            // Extract only NEW functions, excluding RETRIEVED functions
            const libraryCode = tuple.files[`library_${versionKey}`] || '';
            if (libraryCode) {
                const lines = libraryCode.split('\n');
                let inNewSection = false;
                const newFunctionLines = [];
                
                for (const line of lines) {
                    // Check for section markers
                    if (line.includes('NEW HELPER FUNCTIONS') || line.includes('New Helper Functions') || 
                        line.includes('NEW FUNCTIONS') || line.includes('New Functions')) {
                        inNewSection = true;
                        newFunctionLines.push(line);
                    } else if (line.includes('RETRIEVED HELPER FUNCTIONS') || line.includes('Retrieved Helper Functions')) {
                        inNewSection = false;
                    } else if (inNewSection) {
                        newFunctionLines.push(line);
                    }
                }
                
                content = newFunctionLines.join('\n');
            } else {
                content = '';
            }
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
    
    // Argument text area listener
    document.getElementById('argumentText').addEventListener('input', () => {
        checkIfCanProceed();
    });
    
    // Navigation buttons
    document.getElementById('prevBtn').addEventListener('click', () => {
        if (sessionData.currentIndex > 0) {
            saveChoice();  // Save current choice and argument before going back
            sessionData.currentIndex--;
            saveSession();
            loadCurrentTuple();
        }
    });
    
    document.getElementById('nextBtn').addEventListener('click', () => {
        if (sessionData.currentIndex < 9) {
            saveChoice();  // Save the choice and argument before moving on
            sessionData.currentIndex++;
            saveSession();
            loadCurrentTuple();
        }
    });
    
    document.getElementById('submitBtn').addEventListener('click', () => {
        saveChoice();  // Save the choice and argument before submitting
        showCompletionModal();
    });
    
    // Modal buttons
    document.getElementById('openFormBtn').addEventListener('click', () => {
        openPrefilledGoogleForm();
    });
    
    // Font size controls
    setupFontSizeControls();
    
    // Instructions modal
    setupInstructionsModal();
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
    
    // Check if both choice and argument are provided
    checkIfCanProceed();
}

function checkIfCanProceed() {
    const selectedChoice = document.querySelector('.choice-btn.selected');
    const argumentText = document.getElementById('argumentText').value.trim();
    
    // Enable next/submit button only if both choice and argument are provided
    if (selectedChoice && argumentText.length > 0) {
        if (sessionData.currentIndex === 9) {
            const submitBtn = document.getElementById('submitBtn');
            submitBtn.disabled = false;
            submitBtn.classList.remove('btn-disabled');
            submitBtn.classList.add('btn-primary');
        } else {
            document.getElementById('nextBtn').disabled = false;
        }
    } else {
        // Disable buttons if requirements not met
        if (sessionData.currentIndex === 9) {
            const submitBtn = document.getElementById('submitBtn');
            submitBtn.disabled = true;
            submitBtn.classList.remove('btn-primary');
            submitBtn.classList.add('btn-disabled');
        } else {
            document.getElementById('nextBtn').disabled = true;
        }
    }
}

function saveChoice() {
    const selectedBtn = document.querySelector('.choice-btn.selected');
    if (!selectedBtn) return;
    
    const choice = selectedBtn.dataset.choice;
    const argumentText = document.getElementById('argumentText').value.trim();
    
    // Get current tuple data
    const tuple = tuplesData[currentTupleId];
    
    // Map pair_type to numeric pairId
    const pairTypeToId = {
        'mi_vs_logprob': 1,
        'mi_vs_tokens': 2,
        'logprob_vs_tokens': 3
    };
    
    // Update or add response
    const existingIndex = sessionData.allResponses.findIndex(r => r.tupleId === currentTupleId);
    const responseData = {
        tupleId: currentTupleId,
        choice: choice.toUpperCase(),
        argument: argumentText,  // Store the argument text
        pairType: tuple.pair_type,
        pairId: pairTypeToId[tuple.pair_type] || 1,
        v1_metric: tuple.v1_metric,
        v2_metric: tuple.v2_metric,
        trialNumber: sessionData.currentIndex + 1,
        timestamp: new Date().toISOString()
    };
    
    if (existingIndex >= 0) {
        sessionData.allResponses[existingIndex] = responseData;
    } else {
        sessionData.allResponses.push(responseData);
    }
    
    saveSession();
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
    
    // Count unique tuple responses (to handle case where user went back and changed answers)
    const uniqueTuples = new Set(sessionData.allResponses.map(r => r.tupleId));
    const allTuplesAnswered = sessionData.assignedTuples.every(tupleId => 
        sessionData.allResponses.some(r => r.tupleId === tupleId)
    );
    
    // Ensure all 10 questions have been answered
    if (uniqueTuples.size < 10 || !allTuplesAnswered) {
        alert('Please complete all 10 questions before submitting.');
        return;
    }
    
    // Mark session as completed
    sessionData.completed = true;
    saveSession();
    
    // Generate debug summary only in debug mode
    if (debugMode) {
        generateDebugSummary();
        const debugContainer = document.getElementById('debugSummaryContainer');
        if (debugContainer) {
            debugContainer.style.display = 'block';
        }
    }
    
    // Show modal
    document.getElementById('submitModal').style.display = 'flex';
}

function generateDebugSummary() {
    const summaryDiv = document.getElementById('debugSummary');
    if (!summaryDiv) return;
    
    // Sort responses by trial number
    const sortedResponses = [...sessionData.allResponses].sort((a, b) => a.trialNumber - b.trialNumber);
    
    let summaryHTML = '<table style="width: 100%; border-collapse: collapse;">';
    summaryHTML += '<tr style="border-bottom: 2px solid #0284c7;">';
    summaryHTML += '<th style="text-align: left; padding: 5px;">Trial</th>';
    summaryHTML += '<th style="text-align: left; padding: 5px;">Choice</th>';
    summaryHTML += '<th style="text-align: left; padding: 5px;">Winner</th>';
    summaryHTML += '<th style="text-align: left; padding: 5px;">Tuple</th>';
    summaryHTML += '<th style="text-align: left; padding: 5px;">Pair Type</th>';
    summaryHTML += '<th style="text-align: left; padding: 5px;">V1</th>';
    summaryHTML += '<th style="text-align: left; padding: 5px;">V2</th>';
    summaryHTML += '</tr>';
    
    sortedResponses.forEach(response => {
        const tuple = tuplesData[response.tupleId];
        const winnerMetric = response.choice === 'V1' ? response.v1_metric : response.v2_metric;
        const rowColor = response.trialNumber % 2 === 0 ? '#f0f9ff' : '#ffffff';
        
        summaryHTML += `<tr style="background: ${rowColor};">`;
        summaryHTML += `<td style="padding: 5px;">${response.trialNumber}</td>`;
        summaryHTML += `<td style="padding: 5px; font-weight: bold; color: ${response.choice === 'V1' ? '#dc2626' : '#2563eb'};">${response.choice}</td>`;
        summaryHTML += `<td style="padding: 5px; font-weight: bold;">${winnerMetric || 'N/A'}</td>`;
        summaryHTML += `<td style="padding: 5px; font-size: 10px;">${tuple ? tuple.tuple.split(':').pop() : response.tupleId}</td>`;
        summaryHTML += `<td style="padding: 5px;">${response.pairType || 'N/A'}</td>`;
        summaryHTML += `<td style="padding: 5px; color: #dc2626;">${response.v1_metric || 'N/A'}</td>`;
        summaryHTML += `<td style="padding: 5px; color: #2563eb;">${response.v2_metric || 'N/A'}</td>`;
        summaryHTML += '</tr>';
    });
    
    summaryHTML += '</table>';
    
    // Add summary statistics
    const metricWins = {};
    sortedResponses.forEach(response => {
        const winnerMetric = response.choice === 'V1' ? response.v1_metric : response.v2_metric;
        if (winnerMetric) {
            metricWins[winnerMetric] = (metricWins[winnerMetric] || 0) + 1;
        }
    });
    
    summaryHTML += '<div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #0284c7;">';
    summaryHTML += '<strong>Metric Wins:</strong> ';
    Object.entries(metricWins).forEach(([metric, count]) => {
        summaryHTML += `<span style="margin-right: 15px;">${metric}: ${count}</span>`;
    });
    summaryHTML += '</div>';
    
    summaryDiv.innerHTML = summaryHTML;
}

function openPrefilledGoogleForm() {
    // Google Form base URL
    const FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSfY4IV_NLRYtkEr8mYFxfXzgZPHcHoYego6yQ7GStpHbfHWUA/viewform';
    
    // Actual entry IDs from the Google Form (updated with reason fields)
    const ENTRY_IDS = {
        userId: 'entry.1958938177',  // UserID field
        email: 'entry.792270821',    // Email field  
        name: 'entry.1585743737',    // Name field
        programmingExp: 'entry.331754450',  // Programming experience field
        pythonExp: 'entry.1839075244',  // Python experience field
        // Trial 1
        trial1_tupleId: 'entry.1538445591',
        trial1_pairId: 'entry.306224226',
        trial1_choice: 'entry.1092031299',
        trial1_reason: 'entry.1023698889',
        // Trial 2
        trial2_tupleId: 'entry.487065090',
        trial2_pairId: 'entry.165561073',
        trial2_choice: 'entry.812388703',
        trial2_reason: 'entry.2013501725',
        // Trial 3
        trial3_tupleId: 'entry.1277091152',
        trial3_pairId: 'entry.325557872',
        trial3_choice: 'entry.2000752445',
        trial3_reason: 'entry.1647651375',
        // Trial 4
        trial4_tupleId: 'entry.2140505775',
        trial4_pairId: 'entry.1718924254',
        trial4_choice: 'entry.720209224',
        trial4_reason: 'entry.529680361',
        // Trial 5
        trial5_tupleId: 'entry.4308478',
        trial5_pairId: 'entry.198690717',
        trial5_choice: 'entry.136166959',
        trial5_reason: 'entry.413363029',
        // Trial 6
        trial6_tupleId: 'entry.1717139691',
        trial6_pairId: 'entry.1130745721',
        trial6_choice: 'entry.1756691659',
        trial6_reason: 'entry.1553296185',
        // Trial 7
        trial7_tupleId: 'entry.795772895',
        trial7_pairId: 'entry.600609903',
        trial7_choice: 'entry.547640540',
        trial7_reason: 'entry.1479666726',
        // Trial 8
        trial8_tupleId: 'entry.778698876',
        trial8_pairId: 'entry.1778742953',
        trial8_choice: 'entry.659602518',
        trial8_reason: 'entry.704499563',
        // Trial 9
        trial9_tupleId: 'entry.2132146432',
        trial9_pairId: 'entry.2038252166',
        trial9_choice: 'entry.1305399604',
        trial9_reason: 'entry.181619158',
        // Trial 10
        trial10_tupleId: 'entry.867453469',
        trial10_pairId: 'entry.499398113',
        trial10_choice: 'entry.529410553',
        trial10_reason: 'entry.1565690313',
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
    params.append(ENTRY_IDS.programmingExp, sessionData.programmingExperience || '');
    params.append(ENTRY_IDS.pythonExp, sessionData.pythonExperience || '');
    
    // Sort responses by trial number
    const sortedResponses = sessionData.allResponses.sort((a, b) => a.trialNumber - b.trialNumber);
    
    // Add each trial's data
    sortedResponses.forEach((response, index) => {
        const trialNum = index + 1;
        
        // Add TupleID for this trial
        if (ENTRY_IDS[`trial${trialNum}_tupleId`]) {
            params.append(ENTRY_IDS[`trial${trialNum}_tupleId`], response.tupleId.toString());
        }
        
        // Add PairID based on pair_type
        if (ENTRY_IDS[`trial${trialNum}_pairId`]) {
            params.append(ENTRY_IDS[`trial${trialNum}_pairId`], response.pairId || '1');
        }
        
        // Add Choice (V1 or V2)
        if (ENTRY_IDS[`trial${trialNum}_choice`]) {
            params.append(ENTRY_IDS[`trial${trialNum}_choice`], response.choice);
        }
        
        // Add Reason/Argument for this trial
        if (ENTRY_IDS[`trial${trialNum}_reason`] && response.argument) {
            params.append(ENTRY_IDS[`trial${trialNum}_reason`], response.argument);
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
        ['UserID', 'Name', 'Email', 'Programming Experience', 'Python Experience', 'TrialNumber', 'TupleID', 'Choice', 'Timestamp']
    ];
    
    sessionData.allResponses
        .sort((a, b) => a.trialNumber - b.trialNumber)
        .forEach(response => {
            csvRows.push([
                sessionData.participantId,
                sessionData.name || '',
                sessionData.email || '',
                sessionData.programmingExperience || '',
                sessionData.pythonExperience || '',
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
        programmingExperience: sessionData.programmingExperience || '',
        pythonExperience: sessionData.pythonExperience || '',
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

function restartStudy() {
    // Clear all session data
    localStorage.removeItem('studySession');
    localStorage.removeItem('studyStarted');
    
    // Redirect to start page
    window.location.href = 'index.html';
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

function setupInstructionsModal() {
    const modal = document.getElementById('instructionsModal');
    const btn = document.getElementById('instructionsBtn');
    const closeBtn1 = document.getElementById('closeInstructionsBtn');
    const closeBtn2 = document.getElementById('closeInstructionsBtn2');
    
    if (!modal || !btn) return;
    
    // Open modal when button is clicked
    btn.addEventListener('click', () => {
        modal.style.display = 'flex';
    });
    
    // Close modal functions
    const closeModal = () => {
        modal.style.display = 'none';
    };
    
    // Close when X button is clicked
    if (closeBtn1) {
        closeBtn1.addEventListener('click', closeModal);
    }
    
    // Close when "Got it" button is clicked
    if (closeBtn2) {
        closeBtn2.addEventListener('click', closeModal);
    }
    
    // Close when clicking outside the modal
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            closeModal();
        }
    });
}

function setupTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.dataset.tab;
            
            // Update button states
            tabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update content visibility
            tabContents.forEach(content => {
                content.classList.remove('active');
            });
            
            if (targetTab === 'original') {
                document.getElementById('originalTab').classList.add('active');
            } else if (targetTab === 'refactorings') {
                document.getElementById('refactoringsTab').classList.add('active');
            }
        });
    });
}

function extractAndDisplayExistingFunctions(tuple) {
    // Extract existing functions from library_v1 or library_v2
    // These are the functions marked as "RETRIEVED HELPER FUNCTIONS"
    
    let existingFunctions = '';
    
    // Try to get from library_v1 first, then library_v2
    const libraryCode = tuple.files.library_v1 || tuple.files.library_v2 || '';
    
    if (libraryCode) {
        // Look for the RETRIEVED HELPER FUNCTIONS section
        const lines = libraryCode.split('\n');
        let inRetrievedSection = false;
        let inNewSection = false;
        const existingLines = [];
        
        for (const line of lines) {
            // Check for section markers
            if (line.includes('RETRIEVED HELPER FUNCTIONS') || line.includes('Retrieved Helper Functions')) {
                inRetrievedSection = true;
                inNewSection = false;
                existingLines.push(line);
            } else if (line.includes('NEW HELPER FUNCTIONS') || line.includes('New Helper Functions') || 
                       line.includes('NEW FUNCTIONS') || line.includes('New Functions')) {
                inRetrievedSection = false;
                inNewSection = true;
            } else if (inRetrievedSection && !inNewSection) {
                existingLines.push(line);
            }
        }
        
        existingFunctions = existingLines.join('\n');
        
        // If no retrieved section found, try to extract imports and helper functions before NEW section
        if (!existingFunctions || existingFunctions.trim() === '') {
            const beforeNewSection = [];
            for (const line of lines) {
                if (line.includes('NEW HELPER FUNCTIONS') || line.includes('New Helper Functions') ||
                    line.includes('NEW FUNCTIONS') || line.includes('New Functions')) {
                    break;
                }
                beforeNewSection.push(line);
            }
            existingFunctions = beforeNewSection.join('\n');
        }
    }
    
    // If still no existing functions, show a message
    if (!existingFunctions || existingFunctions.trim() === '') {
        existingFunctions = '# No existing/retrieved functions for this example\n# All functions are newly proposed';
    }
    
    // Update the existing functions code panel
    const existingFunctionsElement = document.getElementById('existingFunctionsCode');
    if (existingFunctionsElement) {
        existingFunctionsElement.textContent = existingFunctions;
        Prism.highlightElement(existingFunctionsElement);
    }
}