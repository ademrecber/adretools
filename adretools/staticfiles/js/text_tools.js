// Text Tools JavaScript

function analyzeText() {
    const text = document.getElementById('text-input').value;
    if (!text.trim()) {
        alert('Lütfen analiz edilecek metni girin.');
        return;
    }
    
    const formData = new FormData();
    formData.append('text', text);
    
    fetch('/text/analyze/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('char-count').textContent = data.char_count;
        document.getElementById('char-no-spaces').textContent = data.char_no_spaces;
        document.getElementById('word-count').textContent = data.word_count;
        document.getElementById('line-count').textContent = data.line_count;
        document.getElementById('paragraph-count').textContent = data.paragraph_count;
        document.getElementById('digit-count').textContent = data.digit_count;
        document.getElementById('longest-word').textContent = data.longest_word || '-';
        document.getElementById('avg-word-length').textContent = data.avg_word_length;
        
        document.getElementById('analysis-results').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Analiz sırasında hata oluştu.');
    });
}

function transformText() {
    const text = document.getElementById('transform-input').value;
    const type = document.getElementById('transform-type').value;
    
    if (!text.trim()) {
        alert('Lütfen dönüştürülecek metni girin.');
        return;
    }
    
    const formData = new FormData();
    formData.append('text', text);
    formData.append('type', type);
    
    fetch('/text/transform/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('transform-result').value = data.result;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Dönüştürme sırasında hata oluştu.');
    });
}

function encodeText() {
    const text = document.getElementById('encode-input').value;
    const type = document.getElementById('encode-type').value;
    
    if (!text.trim()) {
        alert('Lütfen kodlanacak metni girin.');
        return;
    }
    
    const formData = new FormData();
    formData.append('text', text);
    formData.append('type', type);
    
    fetch('/text/encode/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('encode-result').value = data.result;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Kodlama sırasında hata oluştu.');
    });
}

function formatJSON() {
    const text = document.getElementById('json-input').value;
    const type = document.getElementById('json-type').value;
    
    if (!text.trim()) {
        alert('Lütfen JSON metni girin.');
        return;
    }
    
    const formData = new FormData();
    formData.append('text', text);
    formData.append('type', type);
    
    fetch('/text/format/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('JSON Hatası: ' + data.error);
        } else {
            document.getElementById('json-result').value = data.result;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('JSON formatlama sırasında hata oluştu.');
    });
}

function copyResult(elementId) {
    const element = document.getElementById(elementId);
    element.select();
    document.execCommand('copy');
    
    // Show feedback
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-check"></i> Kopyalandı!';
    button.classList.add('btn-success');
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.classList.remove('btn-success');
    }, 2000);
}

// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}