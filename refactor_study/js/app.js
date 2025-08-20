// Landing page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const participantForm = document.getElementById('participantForm');
    
    // Get URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const urlUserId = urlParams.get('id');
    
    // If user ID is provided in URL, auto-populate and make read-only
    if (urlUserId) {
        const participantIdInput = document.getElementById('participantId');
        if (participantIdInput) {
            participantIdInput.value = urlUserId.toUpperCase();
            participantIdInput.readOnly = true;
            participantIdInput.style.backgroundColor = '#f3f4f6';
            participantIdInput.style.cursor = 'not-allowed';
            
            // Update the label to indicate it's pre-assigned
            const label = participantIdInput.previousElementSibling;
            if (label) {
                label.textContent = 'Study ID (pre-assigned):';
            }
            
            // Show helper text
            const helperText = document.getElementById('idHelperText');
            if (helperText) {
                helperText.style.display = 'block';
            }
        }
    }
    
    // Check for existing session
    const existingSession = localStorage.getItem('studySession');
    if (existingSession) {
        const session = JSON.parse(existingSession);
        
        // If session is completed, offer to clear it
        if (session.completed) {
            if (confirm('A previous study session was completed. Would you like to start a new study?')) {
                localStorage.removeItem('studySession');
                localStorage.removeItem('studyStarted');
            } else {
                // If they don't want to clear, redirect back to study page
                window.location.href = 'study_single_form.html';
                return;
            }
        } else if (session.currentIndex > 0) {
            // If session is in progress, ask if they want to continue or restart
            if (confirm('You have an ongoing study session. Would you like to continue where you left off?\n\nClick OK to continue, Cancel to start over.')) {
                window.location.href = 'study_single_form.html';
                return;
            } else {
                localStorage.removeItem('studySession');
                localStorage.removeItem('studyStarted');
            }
        }
    }
    
    if (participantForm) {
        participantForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Get form data
            const participantId = document.getElementById('participantId').value.trim().toUpperCase();
            const name = document.getElementById('participantName').value.trim();
            const email = document.getElementById('participantEmail').value.trim();
            const gender = document.getElementById('participantGender').value;
            const age = document.getElementById('participantAge').value;
            const programmingExperience = document.getElementById('programmingExperience').value;
            const pythonExperience = document.getElementById('pythonExperience').value;
            
            // Load user assignments
            try {
                const response = await fetch('data/user_assignments.json');
                const userAssignments = await response.json();
                
                // Check if the user ID exists
                if (!userAssignments[participantId]) {
                    alert('Invalid Study ID. Please check your ID and try again.');
                    return;
                }
                
                // Initialize session data
                const sessionData = {
                    participantId: participantId,
                    name: name,
                    email: email,
                    gender: gender,
                    age: age,
                    programmingExperience: programmingExperience,
                    pythonExperience: pythonExperience,
                    startTime: new Date().toISOString(),
                    assignedTuples: userAssignments[participantId],
                    currentIndex: 0,
                    responses: {},
                    allResponses: []
                };
                
                // Save to localStorage
                localStorage.setItem('studySession', JSON.stringify(sessionData));
                
                // Redirect to single form study page
                window.location.href = 'study_single_form.html';
            } catch (error) {
                console.error('Error loading user assignments:', error);
                alert('Error loading study configuration. Please refresh and try again.');
            }
        });
    }
});

function generateParticipantId() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let id = '';
    for (let i = 0; i < 6; i++) {
        id += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return id;
}

function assignTuples(participantId) {
    // Get tuple counts from localStorage or initialize
    let tupleCounts = JSON.parse(localStorage.getItem('globalTupleCounts') || '{}');
    
    // Initialize counts for 19 tuples if not exists
    for (let i = 0; i < 19; i++) {
        if (!(i in tupleCounts)) {
            tupleCounts[i] = 0;
        }
    }
    
    // Sort tuples by count (ascending) to get least viewed
    const sortedTuples = Object.entries(tupleCounts)
        .map(([id, count]) => ({id: parseInt(id), count}))
        .sort((a, b) => a.count - b.count);
    
    // Select first 10 least-viewed tuples
    const selected = sortedTuples.slice(0, 10).map(t => t.id);
    
    // Update counts
    selected.forEach(id => {
        tupleCounts[id]++;
    });
    
    // Save updated counts
    localStorage.setItem('globalTupleCounts', JSON.stringify(tupleCounts));
    
    // Shuffle the selected tuples for this participant
    return shuffle(selected);
}

function shuffle(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}