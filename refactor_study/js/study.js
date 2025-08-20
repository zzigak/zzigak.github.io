// Study page JavaScript
let tuplesData = [];
let sessionData = null;
let currentTupleId = null;
let timerInterval = null;
let startTime = null;

document.addEventListener('DOMContentLoaded', async function() {
    // Load session data
    sessionData = JSON.parse(localStorage.getItem('studySession'));
    
    if (!sessionData) {
        alert('No study session found. Redirecting to start page.');
        window.location.href = 'index.html';
        return;
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
});

async function loadTuplesData() {
    try {
        const response = await fetch('data/tuples.json');
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
    
    // Load code into panels
    document.getElementById('originalCode').textContent = tuple.original;
    document.getElementById('v1Code').textContent = tuple.v1;
    document.getElementById('v2Code').textContent = tuple.v2;
    
    // Apply syntax highlighting
    Prism.highlightAll();
    
    // Clear previous selection
    document.querySelectorAll('.choice-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // Load previous response if exists
    if (sessionData.responses[currentTupleId]) {
        const prevChoice = sessionData.responses[currentTupleId];
        document.querySelector(`[data-choice="${prevChoice}"]`).classList.add('selected');
        document.getElementById('nextBtn').disabled = false;
    } else {
        document.getElementById('nextBtn').disabled = true;
    }
    
    // Update navigation buttons
    document.getElementById('prevBtn').disabled = sessionData.currentIndex === 0;
    
    // Show submit button on last question
    if (sessionData.currentIndex === 9) {
        document.getElementById('nextBtn').style.display = 'none';
        document.getElementById('submitBtn').style.display = 'inline-block';
        document.getElementById('submitBtn').disabled = !sessionData.responses[currentTupleId];
    } else {
        document.getElementById('nextBtn').style.display = 'inline-block';
        document.getElementById('submitBtn').style.display = 'none';
    }
    
    // Reset scroll positions
    document.querySelectorAll('.code-wrapper').forEach(wrapper => {
        wrapper.scrollTop = 0;
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
    document.getElementById('googleFormBtn').addEventListener('click', () => {
        submitToGoogleForm();
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
        } else if (e.key === '0') {
            selectChoice('none');
        } else if (e.key === 'Enter' && !document.getElementById('nextBtn').disabled) {
            if (sessionData.currentIndex < 9) {
                document.getElementById('nextBtn').click();
            } else {
                document.getElementById('submitBtn').click();
            }
        }
    });
}

function selectChoice(choice) {
    // Update UI
    document.querySelectorAll('.choice-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    document.querySelector(`[data-choice="${choice}"]`).classList.add('selected');
    
    // Save response
    sessionData.responses[currentTupleId] = choice;
    saveSession();
    
    // Enable next/submit button
    if (sessionData.currentIndex === 9) {
        document.getElementById('submitBtn').disabled = false;
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
    document.getElementById('submitModal').style.display = 'flex';
}

function submitToGoogleForm() {
    // Prepare data for Google Form
    const formData = {
        participantId: sessionData.participantId,
        responses: JSON.stringify(sessionData.responses),
        assignedTuples: sessionData.assignedTuples.join(','),
        completionTime: new Date().toISOString()
    };
    
    // Create Google Form URL with pre-filled data
    // You'll need to replace these entry IDs with your actual Google Form field IDs
    const googleFormUrl = 'https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform';
    const params = new URLSearchParams({
        'entry.1234567890': formData.participantId,
        'entry.2345678901': formData.responses,
        'entry.3456789012': formData.assignedTuples,
        'entry.4567890123': formData.completionTime
    });
    
    // Open Google Form in new tab
    window.open(`${googleFormUrl}?${params}`, '_blank');
    
    // Clear session data
    localStorage.removeItem('studySession');
    
    // Show completion message
    alert('Thank you for completing the study! Please fill out the demographics survey in the new tab.');
}

function downloadResponses() {
    const data = {
        participantId: sessionData.participantId,
        startTime: sessionData.startTime,
        completionTime: new Date().toISOString(),
        assignedTuples: sessionData.assignedTuples,
        responses: sessionData.responses,
        tupleDetails: sessionData.assignedTuples.map(id => ({
            tupleId: id,
            tupleName: tuplesData[id]?.name || 'Unknown',
            choice: sessionData.responses[id] || 'No response'
        }))
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `study_responses_${sessionData.participantId}_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function setupFontSizeControls() {
    let currentFontSize = 12; // Default font size in px
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
        // Update all code panels
        document.querySelectorAll('.code-wrapper pre').forEach(pre => {
            pre.style.fontSize = `${size}px`;
        });
        
        // Update display
        fontSizeDisplay.textContent = `${size}px`;
        
        // Save to localStorage
        localStorage.setItem('codeFontSize', size);
        
        // Update button states
        decreaseBtn.disabled = size <= minSize;
        increaseBtn.disabled = size >= maxSize;
    }
}