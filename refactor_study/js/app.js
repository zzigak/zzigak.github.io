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
            
            // Get form data with error checking
            const participantIdElement = document.getElementById('participantId');
            const nameElement = document.getElementById('participantName');
            const emailElement = document.getElementById('participantEmail');
            const programmingExpElement = document.getElementById('programmingExperience');
            const pythonExpElement = document.getElementById('pythonExperience');
            
            if (!participantIdElement || !nameElement || !emailElement || !programmingExpElement || !pythonExpElement) {
                console.error('Missing form elements:', {
                    participantId: !!participantIdElement,
                    name: !!nameElement,
                    email: !!emailElement,
                    programmingExp: !!programmingExpElement,
                    pythonExp: !!pythonExpElement
                });
                alert('Error: Form elements not found. Please refresh the page.');
                return;
            }
            
            const participantId = participantIdElement.value.trim().toUpperCase();
            const name = nameElement.value.trim();
            const email = emailElement.value.trim();
            const programmingExperience = programmingExpElement.value;
            const pythonExperience = pythonExpElement.value;
            
            // Load user assignments
            let assignedTuples = null;
            
            // Try to load from user_assignments_final.json first
            try {
                const response = await fetch('data/user_assignments_final.json');
                const userAssignments = await response.json();
                
                if (userAssignments[participantId]) {
                    assignedTuples = userAssignments[participantId];
                }
            } catch (error) {
                console.log('user_assignments_final.json not found or error, trying v3 file');
            }
            
            // If not found in final, try user_assignments_v3.json
            if (!assignedTuples) {
                try {
                    const response = await fetch('data/user_assignments_v3.json');
                    const userAssignments = await response.json();
                    
                    if (userAssignments[participantId]) {
                        assignedTuples = userAssignments[participantId];
                    }
                } catch (error) {
                    console.log('user_assignments_v3.json not found or error, trying original file');
                }
            }
            
            // If not found in v3, try original user_assignments.json
            if (!assignedTuples) {
                try {
                    const response = await fetch('data/user_assignments.json');
                    const userAssignments = await response.json();
                    
                    if (userAssignments[participantId]) {
                        assignedTuples = userAssignments[participantId];
                    }
                } catch (error) {
                    console.log('user_assignments.json not found or error');
                }
            }
            
            // If still no assignments, use dynamic assignment
            if (!assignedTuples) {
                console.log(`No predefined assignments for ${participantId}, using dynamic assignment`);
                assignedTuples = assignTuples(participantId);
            }
            
            // Initialize session data
            const sessionData = {
                participantId: participantId,
                name: name,
                email: email,
                programmingExperience: programmingExperience,
                pythonExperience: pythonExperience,
                startTime: new Date().toISOString(),
                assignedTuples: assignedTuples,
                currentIndex: 0,
                responses: {},
                allResponses: []
            };
            
            // Save to localStorage
            localStorage.setItem('studySession', JSON.stringify(sessionData));
            
            // Redirect to single form study page
            window.location.href = 'study_single_form.html';
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
    
    // Initialize counts for 45 entries if not exists
    for (let i = 0; i < 45; i++) {
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