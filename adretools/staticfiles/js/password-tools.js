// Password Tools JavaScript

// When page loads
document.addEventListener('DOMContentLoaded', function() {
    const lengthSlider = document.getElementById('passwordLength');
    const lengthValue = document.getElementById('lengthValue');
    
    lengthSlider.addEventListener('input', function() {
        lengthValue.textContent = this.value;
    });
    
    // Real-time check for password strength input
    const checkPasswordInput = document.getElementById('checkPassword');
    let checkTimeout;
    
    checkPasswordInput.addEventListener('input', function() {
        clearTimeout(checkTimeout);
        if (this.value.trim()) {
            checkTimeout = setTimeout(() => {
                checkPasswordStrength();
            }, 500);
        } else {
            document.getElementById('checkResult').style.display = 'none';
        }
    });
});

// Generate password
async function generatePassword() {
    const formData = new FormData();
    formData.append('length', document.getElementById('passwordLength').value);
    formData.append('uppercase', document.getElementById('includeUppercase').checked);
    formData.append('lowercase', document.getElementById('includeLowercase').checked);
    formData.append('numbers', document.getElementById('includeNumbers').checked);
    formData.append('symbols', document.getElementById('includeSymbols').checked);
    formData.append('exclude_similar', document.getElementById('excludeSimilar').checked);
    
    try {
        const response = await fetch('/password/generate/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            showGeneratedPassword(data);
        } else {
            const error = await response.json();
            alert('❌ Error: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Connection Issue: Django server might not be running. Please start the server.');
        } else {
            alert('⚠️ Unexpected Error: ' + error.message);
        }
    }
}

// Show generated password
function showGeneratedPassword(data) {
    document.getElementById('generatedPassword').value = data.password;
    updateStrengthDisplay('generated', data.strength);
    document.getElementById('generatedResult').style.display = 'block';
}

// Check password strength
async function checkPasswordStrength() {
    const password = document.getElementById('checkPassword').value.trim();
    
    if (!password) {
        document.getElementById('checkResult').style.display = 'none';
        return;
    }
    
    const formData = new FormData();
    formData.append('password', password);
    
    try {
        const response = await fetch('/password/check/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            showPasswordCheck(data.strength);
        } else {
            const error = await response.json();
            console.error('Check error:', error.error);
        }
    } catch (error) {
        console.error('Connection error:', error);
    }
}

// Show password check result
function showPasswordCheck(strength) {
    updateStrengthDisplay('check', strength);
    
    // Show details
    const details = strength.details;
    const detailsHtml = `
        <div class="row small">
            <div class="col-6">Length: ${details.length}</div>
            <div class="col-6">Uniqueness: %${details.unique_ratio}</div>
            <div class="col-6">Lowercase: ${details.has_lower ? '✓' : '✗'}</div>
            <div class="col-6">Uppercase: ${details.has_upper ? '✓' : '✗'}</div>
            <div class="col-6">Digits: ${details.has_digit ? '✓' : '✗'}</div>
            <div class="col-6">Symbols: ${details.has_symbol ? '✓' : '✗'}</div>
        </div>
    `;
    document.getElementById('passwordDetails').innerHTML = detailsHtml;
    
    // Show feedback
    const feedbackHtml = strength.feedback.map(feedback => 
        `<div class="feedback-item">${feedback}</div>`
    ).join('');
    document.getElementById('passwordFeedback').innerHTML = feedbackHtml || '<div class="feedback-item">Your password looks secure!</div>';
    
    document.getElementById('checkResult').style.display = 'block';
}

// Update strength display
function updateStrengthDisplay(type, strength) {
    const bar = document.getElementById(`${type}StrengthBar`);
    const level = document.getElementById(`${type}StrengthLevel`);
    const score = document.getElementById(`${type}StrengthScore`);
    
    bar.style.width = strength.score + '%';
    bar.className = `progress-bar strength-bar bg-${strength.color}`;
    level.textContent = strength.level;
    score.textContent = `${strength.score}/100`;
}

// Copy password
function copyPassword() {
    const passwordField = document.getElementById('generatedPassword');
    passwordField.select();
    document.execCommand('copy');
    alert('✅ Password copied!');
}

// Toggle password visibility
function togglePasswordVisibility(fieldId) {
    const field = document.getElementById(fieldId);
    const button = field.nextElementSibling.querySelector('button:last-child i');
    
    if (field.type === 'password') {
        field.type = 'text';
        button.className = 'fas fa-eye-slash';
    } else {
        field.type = 'password';
        button.className = 'fas fa-eye';
    }
}