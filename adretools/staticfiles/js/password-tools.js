// Şifre Araçları JavaScript

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', function() {
    const lengthSlider = document.getElementById('passwordLength');
    const lengthValue = document.getElementById('lengthValue');
    
    lengthSlider.addEventListener('input', function() {
        lengthValue.textContent = this.value;
    });
    
    // Şifre kontrol input'u için gerçek zamanlı kontrol
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

// Şifre üret
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
            alert('❌ Hata: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Bağlantı Sorunu: Django sunucusu çalışmıyor olabilir. Lütfen sunucuyu başlatın.');
        } else {
            alert('⚠️ Beklenmeyen Hata: ' + error.message);
        }
    }
}

// Üretilen şifreyi göster
function showGeneratedPassword(data) {
    document.getElementById('generatedPassword').value = data.password;
    updateStrengthDisplay('generated', data.strength);
    document.getElementById('generatedResult').style.display = 'block';
}

// Şifre güvenlik kontrolü
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
            console.error('Kontrol hatası:', error.error);
        }
    } catch (error) {
        console.error('Bağlantı hatası:', error);
    }
}

// Şifre kontrol sonucunu göster
function showPasswordCheck(strength) {
    updateStrengthDisplay('check', strength);
    
    // Detayları göster
    const details = strength.details;
    const detailsHtml = `
        <div class="row small">
            <div class="col-6">Uzunluk: ${details.length}</div>
            <div class="col-6">Benzersizlik: %${details.unique_ratio}</div>
            <div class="col-6">Küçük Harf: ${details.has_lower ? '✓' : '✗'}</div>
            <div class="col-6">Büyük Harf: ${details.has_upper ? '✓' : '✗'}</div>
            <div class="col-6">Rakam: ${details.has_digit ? '✓' : '✗'}</div>
            <div class="col-6">Sembol: ${details.has_symbol ? '✓' : '✗'}</div>
        </div>
    `;
    document.getElementById('passwordDetails').innerHTML = detailsHtml;
    
    // Önerileri göster
    const feedbackHtml = strength.feedback.map(feedback => 
        `<div class="feedback-item">${feedback}</div>`
    ).join('');
    document.getElementById('passwordFeedback').innerHTML = feedbackHtml || '<div class="feedback-item">Şifreniz güvenli görünüyor!</div>';
    
    document.getElementById('checkResult').style.display = 'block';
}

// Güç göstergesini güncelle
function updateStrengthDisplay(type, strength) {
    const bar = document.getElementById(`${type}StrengthBar`);
    const level = document.getElementById(`${type}StrengthLevel`);
    const score = document.getElementById(`${type}StrengthScore`);
    
    bar.style.width = strength.score + '%';
    bar.className = `progress-bar strength-bar bg-${strength.color}`;
    level.textContent = strength.level;
    score.textContent = `${strength.score}/100`;
}

// Şifre kopyala
function copyPassword() {
    const passwordField = document.getElementById('generatedPassword');
    passwordField.select();
    document.execCommand('copy');
    alert('✅ Şifre kopyalandı!');
}

// Şifre görünürlüğünü değiştir
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