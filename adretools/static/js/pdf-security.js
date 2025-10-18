// PDF Güvenlik İşlemleri
let selectedSecurityFile = null;

// Adım 1: PDF Dosyası Seçimi
function selectSecurityPDF() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf';
    input.onchange = function(e) {
        const file = e.target.files[0];
        if (file) {
            selectedSecurityFile = file;
            displaySelectedSecurityFile(file);
            showSecurityOptions();
        }
    };
    input.click();
}

// Seçilen PDF dosyasını göster
function displaySelectedSecurityFile(file) {
    const display = document.getElementById('selectedSecurityFile');
    const fileSize = (file.size / 1024 / 1024).toFixed(2);
    
    display.innerHTML = `
        <div class="alert alert-success">
            <i class="fas fa-file-pdf text-danger"></i>
            <strong>${file.name}</strong> (${fileSize} MB)
            <br><small>PDF dosyası başarıyla seçildi</small>
        </div>
    `;
}

// Adım 2: Güvenlik seçeneklerini göster
function showSecurityOptions() {
    document.getElementById('step1-select-pdf').style.display = 'none';
    document.getElementById('step2-security-options').style.display = 'block';
}

// Şifreleme formunu göster
function showEncryptionForm() {
    document.getElementById('step2-security-options').style.display = 'none';
    document.getElementById('step3-encryption').style.display = 'block';
}

// Filigran formunu göster
function showWatermarkForm() {
    document.getElementById('step2-security-options').style.display = 'none';
    document.getElementById('step3-watermark').style.display = 'block';
}

// Güvenlik seçeneklerine geri dön
function backToSecurityOptions() {
    document.getElementById('step3-encryption').style.display = 'none';
    document.getElementById('step3-watermark').style.display = 'none';
    document.getElementById('step2-security-options').style.display = 'block';
}

// PDF Şifreleme
function encryptPDF() {
    if (!selectedSecurityFile) {
        showSecurityAlert('Lütfen önce bir PDF dosyası seçin!', 'warning');
        return;
    }

    const password = document.getElementById('pdfPassword').value;
    const confirmPassword = document.getElementById('pdfPasswordConfirm').value;

    if (!password) {
        showSecurityAlert('Lütfen bir şifre girin!', 'warning');
        return;
    }



    if (password !== confirmPassword) {
        showSecurityAlert('Şifreler eşleşmiyor!', 'warning');
        return;
    }

    const formData = new FormData();
    formData.append('pdf', selectedSecurityFile);
    formData.append('password', password);

    showSecurityLoading('PDF şifreleniyor...');

    fetch('/pdf/encrypt/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        return response.json().then(data => {
            throw new Error(data.error || 'Şifreleme hatası');
        });
    })
    .then(blob => {
        hideSecurityLoading();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = selectedSecurityFile.name.replace('.pdf', '_sifreli.pdf');
        a.click();
        window.URL.revokeObjectURL(url);
        
        showSecurityAlert('PDF başarıyla şifrelendi!', 'success');
        resetSecurityModal();
    })
    .catch(error => {
        hideSecurityLoading();
        showSecurityAlert('Hata: ' + error.message, 'danger');
    });
}

// Filigran Ekleme
function addWatermark() {
    if (!selectedSecurityFile) {
        showSecurityAlert('Lütfen önce bir PDF dosyası seçin!', 'warning');
        return;
    }

    const watermarkText = document.getElementById('watermarkText').value;
    const position = document.getElementById('watermarkPosition').value;
    const opacity = document.getElementById('watermarkOpacity').value;
    const size = document.getElementById('watermarkSize').value;

    if (!watermarkText.trim()) {
        showSecurityAlert('Lütfen filigran metni girin!', 'warning');
        return;
    }

    const formData = new FormData();
    formData.append('pdf', selectedSecurityFile);
    formData.append('watermark_text', watermarkText);
    formData.append('position', position);
    formData.append('opacity', opacity);
    formData.append('size', size);

    showSecurityLoading('Filigran ekleniyor...');

    fetch('/pdf/add-watermark/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        return response.json().then(data => {
            throw new Error(data.error || 'Filigran ekleme hatası');
        });
    })
    .then(blob => {
        hideSecurityLoading();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = selectedSecurityFile.name.replace('.pdf', '_filigranli.pdf');
        a.click();
        window.URL.revokeObjectURL(url);
        
        showSecurityAlert('Filigran başarıyla eklendi!', 'success');
        resetSecurityModal();
    })
    .catch(error => {
        hideSecurityLoading();
        showSecurityAlert('Hata: ' + error.message, 'danger');
    });
}

// Modal'ı sıfırla
function resetSecurityModal() {
    selectedSecurityFile = null;
    document.getElementById('step1-select-pdf').style.display = 'block';
    document.getElementById('step2-security-options').style.display = 'none';
    document.getElementById('step3-encryption').style.display = 'none';
    document.getElementById('step3-watermark').style.display = 'none';
    
    // Form alanlarını temizle
    document.getElementById('selectedSecurityFile').innerHTML = '';
    document.getElementById('pdfPassword').value = '';
    document.getElementById('pdfPasswordConfirm').value = '';
    document.getElementById('watermarkText').value = '';
    document.getElementById('watermarkPosition').value = 'center';
    document.getElementById('watermarkOpacity').value = '0.5';
    document.getElementById('watermarkSize').value = '36';
}

// Modal kapandığında sıfırla
document.addEventListener('DOMContentLoaded', function() {
    const securityModal = document.getElementById('securityModal');
    if (securityModal) {
        securityModal.addEventListener('hidden.bs.modal', function() {
            resetSecurityModal();
        });
    }
});

// Yardımcı fonksiyonlar
function showSecurityAlert(message, type) {
    if (window.showAlert) {
        window.showAlert(message, type);
    } else {
        alert(message);
    }
}

function showSecurityLoading(message) {
    if (window.showLoading) {
        window.showLoading(message);
    }
}

function hideSecurityLoading() {
    if (window.hideLoading) {
        window.hideLoading();
    }
}