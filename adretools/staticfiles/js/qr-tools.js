// QR & Barkod Araçları JavaScript

// Araç gösterme/gizleme
function showTool(toolId) {
    // Tüm araçları gizle
    document.querySelectorAll('.tool-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Seçilen aracı göster
    const toolElement = document.getElementById(toolId);
    toolElement.style.display = 'block';
    
    // Sayfa aşağı kaydır
    setTimeout(() => {
        window.scrollTo({
            top: toolElement.offsetTop - 50,
            behavior: 'smooth'
        });
    }, 50);
}

// QR türü değiştiğinde içerik alanını güncelle
function changeQRType() {
    const qrType = document.getElementById('qrType').value;
    
    // Tüm içerik alanlarını gizle
    document.querySelectorAll('.content-type').forEach(area => {
        area.style.display = 'none';
    });
    
    // Seçilen türe göre alanı göster
    switch(qrType) {
        case 'text':
        case 'url':
            document.getElementById('textContent').style.display = 'block';
            break;
        case 'wifi':
            document.getElementById('wifiContent').style.display = 'block';
            break;
        case 'sms':
            document.getElementById('smsContent').style.display = 'block';
            break;
        case 'email':
            document.getElementById('emailContent').style.display = 'block';
            break;
        case 'phone':
            document.getElementById('phoneContent').style.display = 'block';
            break;
        case 'vcard':
            document.getElementById('vcardContent').style.display = 'block';
            break;
    }
}

// QR içeriğini hazırla
function prepareQRContent() {
    const qrType = document.getElementById('qrType').value;
    let content = '';
    
    switch(qrType) {
        case 'text':
        case 'url':
            content = document.getElementById('qrText').value;
            break;
        case 'wifi':
            const ssid = document.getElementById('wifiSSID').value;
            const password = document.getElementById('wifiPassword').value;
            const security = document.getElementById('wifiSecurity').value;
            content = `WIFI:T:${security};S:${ssid};P:${password};;`;
            break;
        case 'sms':
            const smsPhone = document.getElementById('smsPhone').value;
            const smsMessage = document.getElementById('smsMessage').value;
            content = `sms:${smsPhone}?body=${encodeURIComponent(smsMessage)}`;
            break;
        case 'email':
            const email = document.getElementById('emailAddress').value;
            const subject = document.getElementById('emailSubject').value;
            const body = document.getElementById('emailBody').value;
            content = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
            break;
        case 'phone':
            const phone = document.getElementById('phoneNumber').value;
            content = `tel:${phone}`;
            break;
        case 'vcard':
            const firstName = document.getElementById('vcardFirstName').value;
            const lastName = document.getElementById('vcardLastName').value;
            const vcardPhone = document.getElementById('vcardPhone').value;
            const vcardEmail = document.getElementById('vcardEmail').value;
            const org = document.getElementById('vcardOrg').value;
            content = `BEGIN:VCARD\nVERSION:3.0\nFN:${firstName} ${lastName}\nTEL:${vcardPhone}\nEMAIL:${vcardEmail}\nORG:${org}\nEND:VCARD`;
            break;
    }
    
    return content;
}

// QR kod oluştur
async function generateQR() {
    const content = prepareQRContent();
    if (!content.trim()) {
        alert('⚠️ İçerik Gerekli\n\nLütfen QR kod içeriğini girin!');
        return;
    }
    
    const size = document.getElementById('qrSize').value;
    const errorCorrection = document.getElementById('qrErrorCorrection').value;
    const foreground = document.getElementById('qrForeground').value;
    const background = document.getElementById('qrBackground').value;
    const style = document.getElementById('qrStyle').value;
    
    try {
        const formData = new FormData();
        formData.append('content', content);
        formData.append('size', size);
        formData.append('error_correction', errorCorrection);
        formData.append('foreground', foreground);
        formData.append('background', background);
        formData.append('style', style);
        
        // Logo varsa ekle
        const logoFile = document.getElementById('qrLogo').files[0];
        if (logoFile) {
            formData.append('logo', logoFile);
        }
        
        const response = await fetch('/qr/generate/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const img = document.createElement('img');
            img.src = URL.createObjectURL(blob);
            img.style.maxWidth = '100%';
            
            document.getElementById('qrCanvas').innerHTML = '';
            document.getElementById('qrCanvas').appendChild(img);
            document.getElementById('qrPreview').style.display = 'block';
            
            // Global olarak sakla
            window.currentQRBlob = blob;
        } else {
            try {
                const error = await response.json();
                alert('❌ Sunucu Hatası\n\n' + error.error);
            } catch {
                alert('🔌 Bağlantı Sorunu\n\nSunucu çalışmıyor gibi görünüyor.\nLütfen sayfayı yenileyin.');
            }
        }
    } catch (error) {
        if (error.message.includes('Failed to fetch') || error.name === 'TypeError') {
            alert('🔌 Bağlantı Sorunu\n\nSunucu çalışmıyor gibi görünüyor.\nLütfen sayfayı yenileyin veya daha sonra tekrar deneyin.');
        } else {
            alert('❌ Bir sorun oluştu\n\n' + error.message);
        }
    }
}

// QR kod indir
async function downloadQR(format) {
    if (!window.currentQRBlob) {
        alert('⚠️ QR Kod Gerekli\n\nÖnce QR kod oluşturun!');
        return;
    }
    
    const content = prepareQRContent();
    const size = document.getElementById('qrSize').value;
    const errorCorrection = document.getElementById('qrErrorCorrection').value;
    const foreground = document.getElementById('qrForeground').value;
    const background = document.getElementById('qrBackground').value;
    const style = document.getElementById('qrStyle').value;
    
    try {
        const formData = new FormData();
        formData.append('content', content);
        formData.append('size', size);
        formData.append('error_correction', errorCorrection);
        formData.append('foreground', foreground);
        formData.append('background', background);
        formData.append('style', style);
        formData.append('format', format);
        
        // Logo varsa ekle
        const logoFile = document.getElementById('qrLogo').files[0];
        if (logoFile) {
            formData.append('logo', logoFile);
        }
        
        const response = await fetch('/qr/download/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `qr_code.${format}`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            const error = await response.json();
            alert('❌ İndirme Hatası\n\n' + error.error);
        }
    } catch (error) {
        if (error.message.includes('Failed to fetch')) {
            alert('🔌 Bağlantı Sorunu\n\nSunucu ile bağlantı kurulamıyor.');
        } else {
            alert('❌ İndirme hatası\n\n' + error.message);
        }
    }
}

// QR kod oku
async function readQR() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.click();
    
    input.onchange = async () => {
        const file = input.files[0];
        if (!file) return;
        
        try {
            const formData = new FormData();
            formData.append('image', file);
            
            const response = await fetch('/qr/read/', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                document.getElementById('qrResult').innerHTML = `
                    <div class="alert alert-success">
                        <h6>✅ QR Kod Başarıyla Okundu!</h6>
                        <p><strong>İçerik:</strong> ${result.content}</p>
                    </div>
                `;
            } else {
                const error = await response.json();
                document.getElementById('qrResult').innerHTML = `
                    <div class="alert alert-warning">
                        <h6>⚠️ QR Kod Okunamadı</h6>
                        <p>${error.error}</p>
                        <small>Daha net bir resim deneyin.</small>
                    </div>
                `;
            }
        } catch (error) {
            document.getElementById('qrResult').innerHTML = `
                <div class="alert alert-danger">
                    <h6>❌ Okuma Hatası</h6>
                    <p>Resim işlenirken bir sorun oluştu.</p>
                </div>
            `;
        }
    };
}

// Barkod oluştur
async function generateBarcode() {
    const type = document.getElementById('barcodeType').value;
    const data = document.getElementById('barcodeData').value;
    
    if (!data.trim()) {
        alert('⚠️ Veri Gerekli\n\nLütfen barkod verisini girin!');
        return;
    }
    
    try {
        const formData = new FormData();
        formData.append('type', type);
        formData.append('data', data);
        
        const response = await fetch('/qr/barcode/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const img = document.createElement('img');
            img.src = URL.createObjectURL(blob);
            img.style.maxWidth = '100%';
            
            document.getElementById('barcodeCanvas').innerHTML = '';
            document.getElementById('barcodeCanvas').appendChild(img);
            document.getElementById('barcodePreview').style.display = 'block';
            
            // Global olarak sakla
            window.currentBarcodeBlob = blob;
        } else {
            const error = await response.json();
            alert('❌ Barkod Hatası\n\n' + error.error);
        }
    } catch (error) {
        if (error.message.includes('Failed to fetch')) {
            alert('🔌 Bağlantı Sorunu\n\nSunucu ile bağlantı kurulamıyor.');
        } else {
            alert('❌ Barkod oluşturma hatası\n\n' + error.message);
        }
    }
}

// Barkod indir
async function downloadBarcode(format) {
    if (!window.currentBarcodeBlob) {
        alert('⚠️ Barkod Gerekli\n\nÖnce barkod oluşturun!');
        return;
    }
    
    const type = document.getElementById('barcodeType').value;
    const data = document.getElementById('barcodeData').value;
    
    try {
        const formData = new FormData();
        formData.append('type', type);
        formData.append('data', data);
        formData.append('format', format);
        
        const response = await fetch('/qr/barcode-download/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `barcode.${format}`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            const error = await response.json();
            alert('❌ İndirme Hatası\n\n' + error.error);
        }
    } catch (error) {
        if (error.message.includes('Failed to fetch')) {
            alert('🔌 Bağlantı Sorunu\n\nSunucu ile bağlantı kurulamıyor.');
        } else {
            alert('❌ İndirme hatası\n\n' + error.message);
        }
    }
}