// Random Tools JavaScript

// Global variables
let participants = [];
let wheelOptions = [];
let winnerHistory = [];

// Random Number Generator
function generateRandomNumbers() {
    const min = parseInt(document.getElementById('minNumber').value);
    const max = parseInt(document.getElementById('maxNumber').value);
    const count = parseInt(document.getElementById('countNumbers').value);
    
    if (min >= max) {
        document.getElementById('randomResult').innerHTML = 
            '<div class="alert alert-warning">Minimum value must be less than maximum!</div>';
        return;
    }
    
    const numbers = [];
    for (let i = 0; i < count; i++) {
        numbers.push(Math.floor(Math.random() * (max - min + 1)) + min);
    }
    
    document.getElementById('randomResult').innerHTML = `
        <div class="alert alert-success text-center">
            <h4>🎲 Random Numbers</h4>
            <div class="h2 text-primary">${numbers.join(', ')}</div>
        </div>
    `;
}

// Lucky Wheel Functions
function addWheelOption() {
    const option = document.getElementById('wheelOption').value.trim();
    if (!option) return;
    
    wheelOptions.push(option);
    document.getElementById('wheelOption').value = '';
    updateWheelDisplay();
    drawWheel();
}

function updateWheelDisplay() {
    const container = document.getElementById('wheelOptions');
    const showBtn = document.getElementById('showWheelBtn');
    const preview = document.getElementById('wheelPreview');
    
    container.innerHTML = wheelOptions.map((option, index) => `
        <div class="d-flex justify-content-between align-items-center mb-1 p-2 bg-light rounded">
            <span>${option}</span>
            <button class="btn btn-sm btn-danger" onclick="removeWheelOption(${index})">×</button>
        </div>
    `).join('');
    
    // Show/hide wheel button based on options
    if (wheelOptions.length >= 2) {
        showBtn.style.display = 'block';
        preview.querySelector('.alert').innerHTML = `
            <i class="fas fa-check-circle text-success"></i><br>
            ${wheelOptions.length} options added. You can view the wheel!
        `;
    } else {
        showBtn.style.display = 'none';
        preview.querySelector('.alert').innerHTML = `
            <i class="fas fa-info-circle"></i><br>
            Add at least 2 options
        `;
        hideWheel();
    }
}

function removeWheelOption(index) {
    wheelOptions.splice(index, 1);
    updateWheelDisplay();
    if (document.getElementById('wheelContainer').style.display === 'block') {
        if (wheelOptions.length >= 2) {
            drawWheel();
        } else {
            hideWheel();
        }
    }
}

function clearWheelOptions() {
    wheelOptions = [];
    updateWheelDisplay();
    hideWheel();
}

function showWheel() {
    if (wheelOptions.length < 2) {
        alert('Add at least 2 options!');
        return;
    }
    
    document.getElementById('wheelPreview').style.display = 'none';
    document.getElementById('wheelContainer').style.display = 'block';
    drawWheel();
}

function hideWheel() {
    document.getElementById('wheelPreview').style.display = 'block';
    document.getElementById('wheelContainer').style.display = 'none';
    document.getElementById('wheelResult').innerHTML = '';
}

function drawWheel() {
    const wheel = document.getElementById('wheel');
    if (wheelOptions.length === 0) {
        return;
    }
    
    const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'];
    const segmentAngle = 360 / wheelOptions.length;
    
    // Create SVG wheel
    const svgWheel = `
        <svg width="100%" height="100%" viewBox="0 0 200 200" style="transform: rotate(-90deg);">
            ${wheelOptions.map((option, index) => {
                const startAngle = index * segmentAngle;
                const endAngle = (index + 1) * segmentAngle;
                const color = colors[index % colors.length];
                
                const startAngleRad = (startAngle * Math.PI) / 180;
                const endAngleRad = (endAngle * Math.PI) / 180;
                
                const x1 = 100 + 90 * Math.cos(startAngleRad);
                const y1 = 100 + 90 * Math.sin(startAngleRad);
                const x2 = 100 + 90 * Math.cos(endAngleRad);
                const y2 = 100 + 90 * Math.sin(endAngleRad);
                
                const largeArcFlag = segmentAngle > 180 ? 1 : 0;
                
                const textAngle = startAngle + segmentAngle / 2;
                const textAngleRad = (textAngle * Math.PI) / 180;
                const textX = 100 + 50 * Math.cos(textAngleRad);
                const textY = 100 + 50 * Math.sin(textAngleRad);
                
                return `
                    <path d="M 100 100 L ${x1} ${y1} A 90 90 0 ${largeArcFlag} 1 ${x2} ${y2} Z" 
                          fill="${color}" stroke="white" stroke-width="2"/>
                    <text x="${textX}" y="${textY}" 
                          text-anchor="middle" dominant-baseline="middle" 
                          fill="white" font-weight="bold" font-size="11"
                          transform="rotate(${textAngle} ${textX} ${textY})">
                        ${option.length > 10 ? option.substring(0, 10) + '...' : option}
                    </text>
                `;
            }).join('')}
        </svg>
    `;
    
    wheel.innerHTML = svgWheel;
    
    // Reset wheel rotation
    wheel.style.transform = 'rotate(0deg)';
}

function spinWheel() {
    if (wheelOptions.length === 0) {
        alert('Please add options first!');
        return;
    }
    
    const wheel = document.getElementById('wheel');
    const spinBtn = document.getElementById('spinBtn');
    
    spinBtn.disabled = true;
    spinBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Spinning...';
    
    // Reset wheel and start new spin
    wheel.style.transition = 'none';
    wheel.style.transform = 'rotate(0deg)';
    
    // Start animation after short delay
    setTimeout(() => {
        // Get user-specified duration
        const duration = parseInt(document.getElementById('spinDuration').value) || 8;
        
        wheel.style.transition = `transform ${duration}s cubic-bezier(0.25, 0.46, 0.45, 0.94)`;
        
        // Stronger random - timestamp + crypto random
        const timestamp = Date.now();
        const cryptoRandom = crypto.getRandomValues(new Uint32Array(1))[0] / 4294967295;
        const baseRotation = Math.floor((Math.random() + cryptoRandom + (timestamp % 1000) / 1000) * 360);
        const randomRotation = baseRotation + (duration * 360) + Math.floor(Math.random() * 720); // Duration-based spins
        wheel.style.transform = `rotate(${randomRotation}deg)`;
        
        // Wait for duration
        setTimeout(() => {
            // Simple random winner - wheel is visual but winner is purely random
            const winnerIndex = Math.floor(Math.random() * wheelOptions.length);
            const winner = wheelOptions[winnerIndex];
            
            // Highlight winner segment
            highlightWinnerSegment(winnerIndex);
            
            // Fancy winner display
            showWinnerDisplay(winner);
            
            // Show regular result
            document.getElementById('wheelResult').innerHTML = `
                <div class="alert alert-success text-center">
                    <h4>🎉 Winner</h4>
                    <div class="h3 text-primary">${winner}</div>
                    <small class="text-muted">Randomly selected</small>
                </div>
            `;
            
            spinBtn.disabled = false;
            spinBtn.innerHTML = '<i class="fas fa-play"></i> Spin Wheel';
        }, duration * 1000);
    }, 50);
}

function showWinnerDisplay(winner) {
    // Clear previous popups
    closeWinnerDisplay();
    
    // Create fancy winner display
    const winnerDisplay = document.createElement('div');
    winnerDisplay.id = 'winnerPopup';
    winnerDisplay.style.cssText = `
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        background: rgba(0,0,0,0.9) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        z-index: 999999 !important;
        animation: fadeIn 0.5s ease-in;
    `;
    
    winnerDisplay.innerHTML = `
        <div style="
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            padding: 60px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 0 50px rgba(255, 215, 0, 0.8);
            animation: bounceIn 1s ease-out;
            border: 8px solid #fff;
            max-width: 90vw;
        ">
            <div style="font-size: 5rem; margin-bottom: 20px;">🎉</div>
            <div style="
                font-size: 3rem;
                font-weight: bold;
                color: #333;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                margin: 20px 0;
            ">WINNER</div>
            <div style="
                font-size: 4rem;
                font-weight: bold;
                color: #d4af37;
                text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
                margin: 30px 0;
                animation: pulse 2s infinite;
            ">${winner}</div>
            <div style="font-size: 3rem; margin: 20px 0;">🎊 🎈 🎁 🎊</div>
            <button onclick="closeWinnerDisplay()" style="
                background: #fff;
                border: 3px solid #333;
                padding: 15px 30px;
                font-size: 1.2rem;
                font-weight: bold;
                border-radius: 10px;
                cursor: pointer;
                margin-top: 20px;
            ">
                <i class="fas fa-times"></i> Close
            </button>
        </div>
    `;
    
    // Append to body
    document.body.appendChild(winnerDisplay);
    
    // Auto-close after 6 seconds
    setTimeout(() => {
        closeWinnerDisplay();
    }, 6000);
}

function closeWinnerDisplay() {
    const winnerDisplay = document.getElementById('winnerPopup');
    if (winnerDisplay) {
        winnerDisplay.remove();
    }
}

function highlightWinnerSegment(winnerIndex) {
    const wheel = document.getElementById('wheel');
    const paths = wheel.querySelectorAll('path');
    
    if (paths[winnerIndex]) {
        // Highlight winner segment
        paths[winnerIndex].classList.add('winner-segment');
        
        // Remove animation after 5 seconds
        setTimeout(() => {
            paths[winnerIndex].classList.remove('winner-segment');
        }, 5000);
    }
}

// Dice Roller Functions
function rollDice() {
    const count = parseInt(document.getElementById('diceCount').value);
    const container = document.getElementById('diceContainer');
    
    // Create dice elements
    container.innerHTML = '';
    const diceElements = [];
    
    for (let i = 0; i < count; i++) {
        const dice = document.createElement('div');
        dice.className = 'dice rolling';
        dice.textContent = '?';
        container.appendChild(dice);
        diceElements.push(dice);
    }
    
    // Animate and show results
    setTimeout(() => {
        const results = [];
        let total = 0;
        
        diceElements.forEach(dice => {
            const value = Math.floor(Math.random() * 6) + 1;
            dice.textContent = value;
            dice.classList.remove('rolling');
            results.push(value);
            total += value;
        });
        
        document.getElementById('diceResult').innerHTML = `
            <div class="alert alert-success">
                <h5>🎲 Result</h5>
                <p><strong>Dice:</strong> ${results.join(', ')}</p>
                <p><strong>Total:</strong> ${total}</p>
            </div>
        `;
    }, 1000);
}

// Professional Name Picker Functions
function addParticipant() {
    const name = document.getElementById('participantName').value.trim();
    if (!name) return;
    
    participants.push({
        id: Date.now() + Math.random(),
        name: name,
        addedAt: new Date()
    });
    
    document.getElementById('participantName').value = '';
    updateParticipantsList();
}

function addBulkParticipants() {
    const bulkText = document.getElementById('bulkNames').value.trim();
    if (!bulkText) return;
    
    const names = bulkText.split('\n').filter(name => name.trim());
    names.forEach(name => {
        participants.push({
            id: Date.now() + Math.random(),
            name: name.trim(),
            addedAt: new Date()
        });
    });
    
    document.getElementById('bulkNames').value = '';
    updateParticipantsList();
}

function removeParticipant(id) {
    participants = participants.filter(p => p.id !== id);
    updateParticipantsList();
}

function clearAllParticipants() {
    if (participants.length > 0 && !confirm('Are you sure you want to delete all participants?')) {
        return;
    }
    participants = [];
    updateParticipantsList();
}

function shuffleParticipants() {
    for (let i = participants.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [participants[i], participants[j]] = [participants[j], participants[i]];
    }
    updateParticipantsList();
}

function updateParticipantsList() {
    const container = document.getElementById('participantsList');
    const countElement = document.getElementById('participantCount');
    
    countElement.textContent = participants.length;
    
    if (participants.length === 0) {
        container.innerHTML = '<div class="text-muted text-center p-3">No participants added yet</div>';
        return;
    }
    
    container.innerHTML = participants.map(participant => `
        <div class="name-item">
            <span>${participant.name}</span>
            <button class="btn btn-sm btn-outline-danger" onclick="removeParticipant(${participant.id})">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `).join('');
}

function startLottery() {
    if (participants.length === 0) {
        alert('Please add participants first!');
        return;
    }
    
    const winnerCount = parseInt(document.getElementById('winnerCount').value);
    const allowDuplicates = document.getElementById('allowDuplicates').checked;
    
    if (winnerCount > participants.length && !allowDuplicates) {
        alert('The number of winners cannot exceed the number of participants!');
        return;
    }
    
    const winners = [];
    const availableParticipants = [...participants];
    
    // Lottery animation
    const resultContainer = document.getElementById('lotteryResult');
    resultContainer.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x"></i><br>Drawing lottery...</div>';
    
    setTimeout(() => {
        for (let i = 0; i < winnerCount; i++) {
            if (availableParticipants.length === 0 && !allowDuplicates) break;
            
            const randomIndex = Math.floor(Math.random() * (allowDuplicates ? participants.length : availableParticipants.length));
            const winner = allowDuplicates ? participants[randomIndex] : availableParticipants[randomIndex];
            
            winners.push({
                ...winner,
                position: i + 1,
                wonAt: new Date()
            });
            
            if (!allowDuplicates) {
                availableParticipants.splice(randomIndex, 1);
            }
        }
        
        // Add to history
        winnerHistory.push({
            date: new Date(),
            winners: winners,
            totalParticipants: participants.length
        });
        
        displayLotteryResults(winners);
        updateWinnerHistory();
    }, 2000);
}

function displayLotteryResults(winners) {
    const container = document.getElementById('lotteryResult');
    
    container.innerHTML = `
        <div class="alert alert-success">
            <h5><i class="fas fa-trophy"></i> Winners</h5>
            ${winners.map(winner => `
                <div class="winner-animation p-2 mb-2 rounded">
                    <strong>${winner.position}. ${winner.name}</strong>
                </div>
            `).join('')}
        </div>
    `;
}

function updateWinnerHistory() {
    const container = document.getElementById('winnerHistory');
    
    if (winnerHistory.length === 0) return;
    
    container.innerHTML = `
        <h6><i class="fas fa-history"></i> Lottery History</h6>
        <div style="max-height: 200px; overflow-y: auto;">
            ${winnerHistory.slice(-5).reverse().map((lottery, index) => `
                <div class="card mb-2">
                    <div class="card-body p-2">
                        <small class="text-muted">${lottery.date.toLocaleString('en-US')}</small>
                        <div>${lottery.winners.map(w => w.name).join(', ')}</div>
                        <small>(${lottery.totalParticipants} participants)</small>
                    </div>
                </div>
            `).join('')}
        </div>
        <button class="btn btn-sm btn-outline-warning" onclick="clearHistory()">Clear History</button>
    `;
}

function clearHistory() {
    winnerHistory = [];
    document.getElementById('winnerHistory').innerHTML = '';
}

// Initialize dice display
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dice display
    const diceModal = document.getElementById('diceModal');
    if (diceModal) {
        diceModal.addEventListener('shown.bs.modal', function() {
            rollDice(); // Show initial dice
        });
    }
    
    // Initialize wheel modal
    const wheelModal = document.getElementById('lucky-wheelModal');
    if (wheelModal) {
        wheelModal.addEventListener('shown.bs.modal', function() {
            updateWheelDisplay();
            hideWheel();
        });
        
        wheelModal.addEventListener('hidden.bs.modal', function() {
            hideWheel();
            document.getElementById('wheelResult').innerHTML = '';
        });
    }
    
    // Enter key support for inputs
    document.getElementById('participantName')?.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') addParticipant();
    });
    
    document.getElementById('wheelOption')?.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') addWheelOption();
    });
});