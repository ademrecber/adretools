// QR Tools JavaScript

function showTool(toolId) {
    // Hide all tool sections
    document.querySelectorAll('.tool-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show selected tool section
    const targetSection = document.getElementById(toolId + '-section');
    if (targetSection) {
        targetSection.style.display = 'block';
        targetSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// QR Generation
document.addEventListener('DOMContentLoaded', function() {
    const qrForm = document.getElementById('qr-form');
    if (qrForm) {
        qrForm.addEventListener('submit', function(e) {
            e.preventDefault();
            generateQR();
        });
    }
});

function generateQR() {
    const formData = new FormData(document.getElementById('qr-form'));
    
    fetch('/qr/generate/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const preview = document.getElementById('qr-preview');
        preview.innerHTML = `<img src="${url}" class="img-fluid" alt="QR Code">`;
        document.getElementById('qr-actions').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while generating the QR code.');
    });
}

function downloadQR(format) {
    const formData = new FormData(document.getElementById('qr-form'));
    formData.append('format', format);
    
    fetch('/qr/download/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `qr_code.${format}`;
        a.click();
    });
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