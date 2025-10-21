// Image Tools JavaScript

let currentImageFile = null;

// Show/hide tools
function showTool(toolId) {
    // Hide all tools
    document.querySelectorAll('.tool-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show selected tool
    document.getElementById(toolId).style.display = 'block';
}

// Select image for resizing
function selectImageForResize() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.click();
    
    input.onchange = () => {
        const file = input.files[0];
        if (file) {
            currentImageFile = file;
            document.getElementById('resizeImageDisplay').innerHTML = `
                <div class="alert alert-info">
                    Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)
                </div>
            `;
        }
    };
}

// Apply preset size
function applyPresetSize() {
    const preset = document.getElementById('resizePreset').value;
    if (preset) {
        const [width, height] = preset.split('x');
        document.getElementById('resizeWidth').value = width;
        document.getElementById('resizeHeight').value = height;
    }
}

// Resize image
async function resizeImage() {
    if (!currentImageFile) {
        alert('⚠️ Content Required: Please select an image first!');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', currentImageFile);
    
    const width = document.getElementById('resizeWidth').value;
    const height = document.getElementById('resizeHeight').value;
    const percent = document.getElementById('resizePercent').value;
    const keepRatio = document.getElementById('keepAspectRatio').checked;
    
    if (percent) {
        formData.append('percent', percent);
    } else if (width && height) {
        formData.append('width', width);
        formData.append('height', height);
    } else {
        alert('⚠️ Missing Parameters: Please enter size parameters!');
        return;
    }
    
    formData.append('keep_ratio', keepRatio);
    
    try {
        const response = await fetch('/image/resize/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            downloadBlob(blob, `resized_${currentImageFile.name}`);
        } else {
            const error = await response.json();
            alert('❌ Server Error: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Connection Issue: Django server might not be running. Please start the server.');
        } else {
            alert('⚠️ Unexpected Error: ' + error.message);
        }
    }
}

// Select image for cropping
function selectImageForCrop() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.click();
    
    input.onchange = () => {
        const file = input.files[0];
        if (file) {
            currentImageFile = file;
            document.getElementById('cropImageDisplay').innerHTML = `
                <div class="alert alert-info">
                    Selected: ${file.name}
                </div>
            `;
        }
    };
}

// Crop image
async function cropImage() {
    if (!currentImageFile) {
        alert('⚠️ Content Required: Please select an image first!');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', currentImageFile);
    formData.append('x', document.getElementById('cropX').value || 0);
    formData.append('y', document.getElementById('cropY').value || 0);
    formData.append('width', document.getElementById('cropWidth').value);
    formData.append('height', document.getElementById('cropHeight').value);
    
    try {
        const response = await fetch('/image/crop/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            downloadBlob(blob, `cropped_${currentImageFile.name}`);
        } else {
            const error = await response.json();
            alert('❌ Server Error: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Connection Issue: Django server might not be running. Please start the server.');
        } else {
            alert('⚠️ Unexpected Error: ' + error.message);
        }
    }
}

// Select image for rotation
function selectImageForRotate() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.click();
    
    input.onchange = () => {
        const file = input.files[0];
        if (file) {
            currentImageFile = file;
            document.getElementById('rotateImageDisplay').innerHTML = `
                <div class="alert alert-info">
                    Selected: ${file.name}
                </div>
            `;
        }
    };
}

// Flip horizontally
function flipHorizontal() {
    if (!currentImageFile) {
        alert('⚠️ Content Required: Please select an image first!');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', currentImageFile);
    formData.append('flip_h', 'true');
    
    processRotation(formData, 'flipped_h_');
}

// Flip vertically
function flipVertical() {
    if (!currentImageFile) {
        alert('⚠️ Content Required: Please select an image first!');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', currentImageFile);
    formData.append('flip_v', 'true');
    
    processRotation(formData, 'flipped_v_');
}

// Rotate image
async function rotateImage() {
    if (!currentImageFile) {
        alert('⚠️ Content Required: Please select an image first!');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', currentImageFile);
    
    const angleSelect = document.getElementById('rotateAngle').value;
    let angle = 0;
    
    if (angleSelect === 'custom') {
        angle = document.getElementById('customAngle').value || 0;
    } else {
        angle = angleSelect;
    }
    
    formData.append('angle', angle);
    
    processRotation(formData, 'rotated_');
}

// Perform rotation
async function processRotation(formData, prefix) {
    try {
        const response = await fetch('/image/rotate/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            downloadBlob(blob, `${prefix}${currentImageFile.name}`);
        } else {
            const error = await response.json();
            alert('❌ Server Error: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Connection Issue: Django server might not be running. Please start the server.');
        } else {
            alert('⚠️ Unexpected Error: ' + error.message);
        }
    }
}

// Select image for format conversion
function selectImageForConvert() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.click();
    
    input.onchange = () => {
        const file = input.files[0];
        if (file) {
            currentImageFile = file;
            document.getElementById('convertImageDisplay').innerHTML = `
                <div class="alert alert-info">
                    Selected: ${file.name}
                </div>
            `;
        }
    };
}

// Update quality value
document.addEventListener('DOMContentLoaded', function() {
    const qualitySlider = document.getElementById('imageQuality');
    const qualityValue = document.getElementById('qualityValue');
    
    if (qualitySlider && qualityValue) {
        qualitySlider.addEventListener('input', function() {
            qualityValue.textContent = this.value;
        });
    }
});

// Convert format
async function convertFormat() {
    if (!currentImageFile) {
        alert('⚠️ Content Required: Please select an image first!');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', currentImageFile);
    formData.append('format', document.getElementById('targetFormat').value);
    formData.append('quality', document.getElementById('imageQuality').value);
    formData.append('transparency', document.getElementById('keepTransparency').checked);
    
    try {
        const response = await fetch('/image/convert/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const format = document.getElementById('targetFormat').value;
            downloadBlob(blob, `converted.${format}`);
        } else {
            const error = await response.json();
            alert('❌ Server Error: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Connection Issue: Django server might not be running. Please start the server.');
        } else {
            alert('⚠️ Unexpected Error: ' + error.message);
        }
    }
}

// Select image for compression
function selectImageForCompress() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.click();
    
    input.onchange = () => {
        const file = input.files[0];
        if (file) {
            currentImageFile = file;
            document.getElementById('compressImageDisplay').innerHTML = `
                <div class="alert alert-info">
                    Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)
                </div>
            `;
        }
    };
}

// Update custom quality value
document.addEventListener('DOMContentLoaded', function() {
    const customQualitySlider = document.getElementById('customQuality');
    const customQualityValue = document.getElementById('customQualityValue');
    
    if (customQualitySlider && customQualityValue) {
        customQualitySlider.addEventListener('input', function() {
            customQualityValue.textContent = this.value;
        });
    }
});

// Compress image
async function compressImage() {
    if (!currentImageFile) {
        alert('⚠️ Content Required: Please select an image first!');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', currentImageFile);
    
    const compressionLevel = document.getElementById('compressionLevel').value;
    let quality = 70;
    
    switch(compressionLevel) {
        case 'light':
            quality = 90;
            break;
        case 'medium':
            quality = 70;
            break;
        case 'heavy':
            quality = 50;
            break;
        case 'custom':
            quality = document.getElementById('customQuality').value;
            break;
    }
    
    formData.append('quality', quality);
    
    const targetSize = document.getElementById('targetSize').value;
    if (targetSize && targetSize > 0) {
        formData.append('target_size', targetSize);
    }
    
    try {
        const response = await fetch('/image/compress/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            downloadBlob(blob, `compressed_${currentImageFile.name.split('.')[0]}.jpg`);
        } else {
            const error = await response.json();
            alert('❌ Server Error: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Connection Issue: Django server might not be running. Please start the server.');
        } else {
            alert('⚠️ Unexpected Error: ' + error.message);
        }
    }
}

// Select file for ICO
function selectFileForIco() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*,.pdf,.svg';
    input.click();
    
    input.onchange = () => {
        const file = input.files[0];
        if (file) {
            currentImageFile = file;
            const fileType = file.name.split('.').pop().toUpperCase();
            document.getElementById('icoFileDisplay').innerHTML = `
                <div class="alert alert-success">
                    <i class="fas fa-check"></i> Selected: ${file.name} (${fileType})
                </div>
            `;
        }
    };
}

// Create ICO
async function createIco() {
    if (!currentImageFile) {
        alert('⚠️ Content Required: Please select a file first!');
        return;
    }
    
    document.getElementById('icoProgress').style.display = 'block';
    
    const formData = new FormData();
    formData.append('image', currentImageFile);
    
    try {
        const response = await fetch('/image/ico/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            downloadBlob(blob, `${currentImageFile.name.split('.')[0]}.ico`);
        } else {
            const error = await response.json();
            alert('❌ Server Error: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Connection Issue: Django server might not be running. Please start the server.');
        } else {
            alert('⚠️ Unexpected Error: ' + error.message);
        }
    } finally {
        document.getElementById('icoProgress').style.display = 'none';
    }
}

// Download blob file
function downloadBlob(blob, filename) {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}