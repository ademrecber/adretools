// PDF Main Module - Common functions

// Show alert function
window.showAlert = function(message, type = 'info') {
    // Create Bootstrap alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-close after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
};

// Show loading function
window.showLoading = function(message = 'Processing...') {
    // Remove existing loading
    hideLoading();
    
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'pdf-loading';
    loadingDiv.className = 'position-fixed d-flex align-items-center justify-content-center';
    loadingDiv.style.cssText = 'top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 10000;';
    
    loadingDiv.innerHTML = `
        <div class="text-center text-white">
            <div class="spinner-border text-light mb-3" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div class="h5">${message}</div>
        </div>
    `;
    
    document.body.appendChild(loadingDiv);
};

// Hide loading function
window.hideLoading = function() {
    const loadingDiv = document.getElementById('pdf-loading');
    if (loadingDiv) {
        loadingDiv.remove();
    }
};

// Format file size
window.formatFileSize = function(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// PDF file check
window.isPDFFile = function(file) {
    return file && file.type === 'application/pdf';
};

// Get file extension
window.getFileExtension = function(filename) {
    return filename.split('.').pop().toLowerCase();
};