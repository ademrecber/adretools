// URL Araçları JavaScript

// URL kısalt
async function shortenUrl() {
    const url = document.getElementById('originalUrl').value.trim();
    
    if (!url) {
        alert('⚠️ Content Required: Please enter a URL!');
        return;
    }
    
    const formData = new FormData();
    formData.append('url', url);
    
    try {
        const response = await fetch('/url/shorten/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            showResult(data);
        } else {
            const error = await response.json();
            alert('❌ Error: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Connection Issue: The Django server might not be running. Please start the server.');
        } else {
            alert('⚠️ Unexpected Error: ' + error.message);
        }
    }
}

// Sonucu göster
function showResult(data) {
    document.getElementById('shortUrl').value = data.short_url;
    document.getElementById('qrCode').src = data.qr_code;
    document.getElementById('clickCount').textContent = data.click_count;
    document.getElementById('displayOriginalUrl').textContent = data.original_url;
    document.getElementById('resultCard').style.display = 'block';
}

// URL kopyala
function copyUrl() {
    const shortUrl = document.getElementById('shortUrl');
    shortUrl.select();
    document.execCommand('copy');
    alert('✅ URL copied!');
}

// QR kod indir
function downloadQR() {
    const qrImg = document.getElementById('qrCode');
    const link = document.createElement('a');
    link.href = qrImg.src;
    link.download = 'qr-code.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// URL paylaş
function shareUrl() {
    const shortUrl = document.getElementById('shortUrl').value;
    
    if (navigator.share) {
        navigator.share({
            title: 'Shortened URL',
            url: shortUrl
        });
    } else {
        copyUrl();
    }
}

// İstatistik getir
async function getStats() {
    const code = document.getElementById('statsCode').value.trim();
    
    if (!code) {
        alert('⚠️ Content Required: Please enter a short code!');
        return;
    }
    
    const formData = new FormData();
    formData.append('code', code);
    
    try {
        const response = await fetch('/url/stats/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            showStats(data);
        } else {
            const error = await response.json();
            alert('❌ Error: ' + error.error);
            document.getElementById('statsResult').style.display = 'none';
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Connection Issue: The Django server might not be running. Please start the server.');
        } else {
            alert('⚠️ Unexpected Error: ' + error.message);
        }
    }
}

// İstatistikleri göster
function showStats(data) {
    document.getElementById('statsOriginalUrl').textContent = data.original_url;
    document.getElementById('statsClickCount').textContent = data.click_count;
    document.getElementById('statsCreatedAt').textContent = data.created_at;
    document.getElementById('statsResult').style.display = 'block';
}