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
                const urlParams = new URLSearchParams(window.location.search);
                const debugKey = urlParams.get('debugKey');
                const debugParam = debugKey ? `?debugKey=${debugKey}` : '';
                window.location.href = 'study_single_form.html' + debugParam;
                return;
            }
        } else if (session.currentIndex > 0) {
            // If session is in progress, ask if they want to continue or restart
            if (confirm('You have an ongoing study session. Would you like to continue where you left off?\n\nClick OK to continue, Cancel to start over.')) {
                const urlParams = new URLSearchParams(window.location.search);
                const debugKey = urlParams.get('debugKey');
                const debugParam = debugKey ? `?debugKey=${debugKey}` : '';
                window.location.href = 'study_single_form.html' + debugParam;
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
            
            // Load user assignments with shuffled versions
            let assignedTuples = null;
            let shuffleInfo = null;
            
            try {
                // Try to load shuffled assignments first (includes version swap info)
                try {
                    const shuffleResponse = await fetch('data/user_assignments_shuffled.json');
                    const shuffledAssignments = await shuffleResponse.json();
                    
                    if (shuffledAssignments[participantId]) {
                        shuffleInfo = shuffledAssignments[participantId];
                        assignedTuples = shuffleInfo.map(item => item.tuple_index);
                        console.log(`Loaded shuffled assignments for ${participantId}`);
                    }
                } catch (shuffleError) {
                    console.log('Shuffled assignments not found, using original');
                }
                
                // Fallback to original assignments if shuffled not found
                if (!assignedTuples) {
                    const response = await fetch('data/user_assignments_final_uniform.json');
                    const userAssignments = await response.json();
                    
                    if (userAssignments[participantId]) {
                        assignedTuples = userAssignments[participantId];
                        console.log(`Loaded original assignments for ${participantId}`);
                    } else {
                        alert(`No assignments found for participant ID: ${participantId}. Please check your ID.`);
                        return;
                    }
                }
            } catch (error) {
                console.error('Error loading assignments:', error);
                alert('Error loading study assignments. Please contact the study administrator.');
                return;
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
                shuffleInfo: shuffleInfo,  // Store shuffle info for version swapping
                currentIndex: 0,
                responses: {},
                allResponses: []
            };
            
            // Save to localStorage
            localStorage.setItem('studySession', JSON.stringify(sessionData));
            
            // Redirect to single form study page, preserving debug key if present
            const urlParams = new URLSearchParams(window.location.search);
            const debugKey = urlParams.get('debugKey');
            const debugParam = debugKey ? `?debugKey=${debugKey}` : '';
            window.location.href = 'study_single_form.html' + debugParam;
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

async function assignTuplesWithUniqueOriginals(participantId) {
    // Load tuples data to get cluster information
    let tuplesData;
    try {
        const response = await fetch('data/tuples_v4_no_docs.json');
        tuplesData = await response.json();
    } catch (error) {
        console.error('Error loading tuples data:', error);
        // Fallback to simple assignment if can't load data
        return assignTuplesSimple(participantId);
    }
    
    // Get tuple counts from localStorage or initialize
    let tupleCounts = JSON.parse(localStorage.getItem('globalTupleCounts') || '{}');
    
    // Group tuples by cluster
    const clusterGroups = {};
    tuplesData.forEach((tuple, index) => {
        const cluster = tuple.cluster;
        if (!clusterGroups[cluster]) {
            clusterGroups[cluster] = [];
        }
        clusterGroups[cluster].push({
            id: index,
            count: tupleCounts[index] || 0
        });
    });
    
    // Select one tuple from each cluster (10 clusters total)
    const selected = [];
    const clusters = Object.keys(clusterGroups);
    
    // Ensure we have 10 unique clusters
    const numClusters = Math.min(clusters.length, 10);
    
    for (let i = 0; i < numClusters; i++) {
        const cluster = clusters[i];
        const tuplesInCluster = clusterGroups[cluster];
        
        // Sort by view count (ascending) to get least viewed
        tuplesInCluster.sort((a, b) => a.count - b.count);
        
        // Select the least viewed tuple from this cluster
        if (tuplesInCluster.length > 0) {
            selected.push(tuplesInCluster[0].id);
        }
    }
    
    // Update counts
    selected.forEach(id => {
        if (!(id in tupleCounts)) {
            tupleCounts[id] = 0;
        }
        tupleCounts[id]++;
    });
    
    // Save updated counts
    localStorage.setItem('globalTupleCounts', JSON.stringify(tupleCounts));
    
    // Shuffle the selected tuples for this participant
    return shuffle(selected);
}

function assignTuplesSimple(participantId) {
    // Fallback to original simple assignment logic
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

// Keep original function name for compatibility but make it use the new logic
async function assignTuples(participantId) {
    return await assignTuplesWithUniqueOriginals(participantId);
}

function shuffle(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}