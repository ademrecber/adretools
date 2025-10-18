// Metin Araçları JavaScript

let analyzeTimeout;

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', function() {
    const inputText = document.getElementById('inputText');
    
    // Metin değiştiğinde otomatik analiz
    inputText.addEventListener('input', function() {
        clearTimeout(analyzeTimeout);
        analyzeTimeout = setTimeout(analyzeText, 300);
    });
    
    // İlk analiz
    analyzeText();
});

// Metin analizi
async function analyzeText() {
    const text = document.getElementById('inputText').value;
    
    if (!text.trim()) {
        resetStats();
        return;
    }
    
    const formData = new FormData();
    formData.append('text', text);
    
    try {
        const response = await fetch('/text/analyze/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            updateStats(data);
        } else {
            console.error('Analiz hatası');
        }
    } catch (error) {
        console.error('Bağlantı hatası:', error);
    }
}

// İstatistikleri güncelle
function updateStats(data) {
    document.getElementById('charCount').textContent = data.char_count;
    document.getElementById('charNoSpaces').textContent = data.char_no_spaces;
    document.getElementById('wordCount').textContent = data.word_count;
    document.getElementById('lineCount').textContent = data.line_count;
    document.getElementById('paragraphCount').textContent = data.paragraph_count;
    document.getElementById('digitCount').textContent = data.digit_count;
    document.getElementById('letterCount').textContent = data.letter_count;
    document.getElementById('longestWord').textContent = data.longest_word || '-';
    document.getElementById('avgWordLength').textContent = data.avg_word_length;
}

// İstatistikleri sıfırla
function resetStats() {
    document.getElementById('charCount').textContent = '0';
    document.getElementById('charNoSpaces').textContent = '0';
    document.getElementById('wordCount').textContent = '0';
    document.getElementById('lineCount').textContent = '0';
    document.getElementById('paragraphCount').textContent = '0';
    document.getElementById('digitCount').textContent = '0';
    document.getElementById('letterCount').textContent = '0';
    document.getElementById('longestWord').textContent = '-';
    document.getElementById('avgWordLength').textContent = '0';
}

// Metin dönüştürme
async function transformText(type) {
    const text = document.getElementById('inputText').value;
    
    if (!text.trim()) {
        alert('⚠️ İçerik Gerekli: Önce metin girin!');
        return;
    }
    
    const formData = new FormData();
    formData.append('text', text);
    formData.append('type', type);
    
    try {
        const response = await fetch('/text/transform/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            document.getElementById('inputText').value = data.result;
            analyzeText();
        } else {
            const error = await response.json();
            alert('❌ Dönüştürme Hatası: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Bağlantı Sorunu: Django sunucusu çalışmıyor olabilir. Lütfen sunucuyu başlatın.');
        } else {
            alert('⚠️ Beklenmeyen Hata: ' + error.message);
        }
    }
}

// Metin kodlama
async function encodeText(type) {
    const text = document.getElementById('inputText').value;
    
    if (!text.trim()) {
        alert('⚠️ İçerik Gerekli: Önce metin girin!');
        return;
    }
    
    const formData = new FormData();
    formData.append('text', text);
    formData.append('type', type);
    
    try {
        const response = await fetch('/text/encode/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            document.getElementById('inputText').value = data.result;
            analyzeText();
        } else {
            const error = await response.json();
            alert('❌ Kodlama Hatası: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Bağlantı Sorunu: Django sunucusu çalışmıyor olabilir. Lütfen sunucuyu başlatın.');
        } else {
            alert('⚠️ Beklenmeyen Hata: ' + error.message);
        }
    }
}

// Metin formatlama
async function formatText(type) {
    const text = document.getElementById('inputText').value;
    
    if (!text.trim()) {
        alert('⚠️ İçerik Gerekli: Önce metin girin!');
        return;
    }
    
    const formData = new FormData();
    formData.append('text', text);
    formData.append('type', type);
    
    try {
        const response = await fetch('/text/format/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            document.getElementById('inputText').value = data.result;
            analyzeText();
        } else {
            const error = await response.json();
            alert('❌ Format Hatası: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Bağlantı Sorunu: Django sunucusu çalışmıyor olabilir. Lütfen sunucuyu başlatın.');
        } else {
            alert('⚠️ Beklenmeyen Hata: ' + error.message);
        }
    }
}