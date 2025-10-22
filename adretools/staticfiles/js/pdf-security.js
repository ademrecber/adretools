// PDF Security Operations
let selectedSecurityFile = null;

// Step 1: PDF File Selection
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

// Display selected PDF file
function displaySelectedSecurityFile(file) {
    const display = document.getElementById('selectedSecurityFile');
    const fileSize = (file.size / 1024 / 1024).toFixed(2);
    
    display.innerHTML = `
        <div class="alert alert-success">
            <i class="fas fa-file-pdf text-danger"></i>
            <strong>${file.name}</strong> (${fileSize} MB)
            <br><small>PDF file successfully selected</small>
        </div>
    `;
}

// Step 2: Show security options
function showSecurityOptions() {
    document.getElementById('step1-select-pdf').style.display = 'none';
    document.getElementById('step2-security-options').style.display = 'block';
}

// Show encryption form
function showEncryptionForm() {
    document.getElementById('step2-security-options').style.display = 'none';
    document.getElementById('step3-encryption').style.display = 'block';
}

// Show watermark form
function showWatermarkForm() {
    document.getElementById('step2-security-options').style.display = 'none';
    document.getElementById('step3-watermark').style.display = 'block';
}

// Back to security options
function backToSecurityOptions() {
    document.getElementById('step3-encryption').style.display = 'none';
    document.getElementById('step3-watermark').style.display = 'none';
    document.getElementById('step2-security-options').style.display = 'block';
}

// PDF Encryption
function encryptPDF() {
    if (!selectedSecurityFile) {
        showSecurityAlert('Please select a PDF file first!', 'warning');
        return;
    }

    const password = document.getElementById('pdfPassword').value;
    const confirmPassword = document.getElementById('pdfPasswordConfirm').value;

    if (!password) {
        showSecurityAlert('Please enter a password!', 'warning');
        return;
    }

    if (password !== confirmPassword) {
        showSecurityAlert('Passwords do not match!', 'warning');
        return;
    }

    const formData = new FormData();
    formData.append('pdf', selectedSecurityFile);
    formData.append('password', password);

    showSecurityLoading('Encrypting PDF...');

    fetch('/pdf/encrypt/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        return response.json().then(data => {
            throw new Error(data.error || 'Encryption error');
        });
    })
    .then(blob => {
        hideSecurityLoading();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = selectedSecurityFile.name.replace('.pdf', '_encrypted.pdf');
        a.click();
        window.URL.revokeObjectURL(url);
        
        showSecurityAlert('PDF successfully encrypted!', 'success');
        resetSecurityModal();
    })
    .catch(error => {
        hideSecurityLoading();
        showSecurityAlert('Error: ' + error.message, 'danger');
    });
}

// Add Watermark
function addWatermark() {
    if (!selectedSecurityFile) {
        showSecurityAlert('Please select a PDF file first!', 'warning');
        return;
    }

    const watermarkText = document.getElementById('watermarkText').value;
    const position = document.getElementById('watermarkPosition').value;
    const opacity = document.getElementById('watermarkOpacity').value;
    const size = document.getElementById('watermarkSize').value;

    if (!watermarkText.trim()) {
        showSecurityAlert('Please enter watermark text!', 'warning');
        return;
    }

    const formData = new FormData();
    formData.append('pdf', selectedSecurityFile);
    formData.append('watermark_text', watermarkText);
    formData.append('position', position);
    formData.append('opacity', opacity);
    formData.append('size', size);

    showSecurityLoading('Adding watermark...');

    fetch('/pdf/add-watermark/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        return response.json().then(data => {
            throw new Error(data.error || 'Watermark addition error');
        });
    })
    .then(blob => {
        hideSecurityLoading();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = selectedSecurityFile.name.replace('.pdf', '_watermarked.pdf');
        a.click();
        window.URL.revokeObjectURL(url);
        
        showSecurityAlert('Watermark successfully added!', 'success');
        resetSecurityModal();
    })
    .catch(error => {
        hideSecurityLoading();
        showSecurityAlert('Error: ' + error.message, 'danger');
    });
}

// Reset modal
function resetSecurityModal() {
    selectedSecurityFile = null;
    document.getElementById('step1-select-pdf').style.display = 'block';
    document.getElementById('step2-security-options').style.display = 'none';
    document.getElementById('step3-encryption').style.display = 'none';
    document.getElementById('step3-watermark').style.display = 'none';
    
    // Clear form fields
    document.getElementById('selectedSecurityFile').innerHTML = '';
    document.getElementById('pdfPassword').value = '';
    document.getElementById('pdfPasswordConfirm').value = '';
    document.getElementById('watermarkText').value = '';
    document.getElementById('watermarkPosition').value = 'center';
    document.getElementById('watermarkOpacity').value = '0.5';
    document.getElementById('watermarkSize').value = '36';
}

// Reset when modal closes
document.addEventListener('DOMContentLoaded', function() {
    const securityModal = document.getElementById('securityModal');
    if (securityModal) {
        securityModal.addEventListener('hidden.bs.modal', function() {
            resetSecurityModal();
        });
    }
});

// Helper functions
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