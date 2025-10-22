// Color Finder JavaScript

let canvas, ctx, imageData;
let colorHistory = [];

// When page loads
document.addEventListener('DOMContentLoaded', function() {
    canvas = document.getElementById('colorCanvas');
    ctx = canvas.getContext('2d');
    
    // Drag & Drop
    const uploadArea = document.getElementById('uploadArea');
    
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            loadImage(files[0]);
        }
    });
    
    // Canvas click
    canvas.addEventListener('click', function(e) {
        if (imageData) {
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            
            const x = Math.floor((e.clientX - rect.left) * scaleX);
            const y = Math.floor((e.clientY - rect.top) * scaleY);
            
            getColorAtPosition(x, y);
        }
    });
    
    // File input
    document.getElementById('imageInput').addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            loadImage(e.target.files[0]);
        }
    });
});

// Select image
function selectImage() {
    document.getElementById('imageInput').click();
}

// Load image
function loadImage(file) {
    if (!file.type.startsWith('image/')) {
        alert('⚠️ Invalid File: Please select an image file!');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            // Set canvas size
            const maxWidth = 600;
            const maxHeight = 400;
            
            let { width, height } = img;
            
            if (width > maxWidth) {
                height = (height * maxWidth) / width;
                width = maxWidth;
            }
            
            if (height > maxHeight) {
                width = (width * maxHeight) / height;
                height = maxHeight;
            }
            
            canvas.width = width;
            canvas.height = height;
            
            // Draw image
            ctx.drawImage(img, 0, 0, width, height);
            imageData = ctx.getImageData(0, 0, width, height);
            
            // Update UI
            document.getElementById('uploadArea').style.display = 'none';
            document.getElementById('imageContainer').style.display = 'block';
        };
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
}

// Get color at specified position
function getColorAtPosition(x, y) {
    if (!imageData) return;
    
    const index = (y * imageData.width + x) * 4;
    const r = imageData.data[index];
    const g = imageData.data[index + 1];
    const b = imageData.data[index + 2];
    
    updateColorInfo(x, y, r, g, b);
    addToHistory(r, g, b);
}

// Update color information
function updateColorInfo(x, y, r, g, b) {
    // Coordinates
    document.getElementById('coordinates').textContent = `X: ${x}, Y: ${y}`;
    
    // HEX
    const hex = rgbToHex(r, g, b);
    document.getElementById('hexValue').value = hex;
    
    // RGB
    const rgb = `rgb(${r}, ${g}, ${b})`;
    document.getElementById('rgbValue').value = rgb;
    
    // HSL
    const hsl = rgbToHsl(r, g, b);
    document.getElementById('hslValue').value = `hsl(${hsl.h}, ${hsl.s}%, ${hsl.l}%)`;
    
    // CMYK
    const cmyk = rgbToCmyk(r, g, b);
    document.getElementById('cmykValue').value = `cmyk(${cmyk.c}%, ${cmyk.m}%, ${cmyk.y}%, ${cmyk.k}%)`;
    
    // Color preview
    document.getElementById('colorPreview').style.backgroundColor = rgb;
}

// Convert RGB to HEX
function rgbToHex(r, g, b) {
    return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

// Convert RGB to HSL
function rgbToHsl(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;
    
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;
    
    if (max === min) {
        h = s = 0;
    } else {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        
        switch (max) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }
    
    return {
        h: Math.round(h * 360),
        s: Math.round(s * 100),
        l: Math.round(l * 100)
    };
}

// Convert RGB to CMYK
function rgbToCmyk(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;
    
    const k = 1 - Math.max(r, Math.max(g, b));
    const c = (1 - r - k) / (1 - k) || 0;
    const m = (1 - g - k) / (1 - k) || 0;
    const y = (1 - b - k) / (1 - k) || 0;
    
    return {
        c: Math.round(c * 100),
        m: Math.round(m * 100),
        y: Math.round(y * 100),
        k: Math.round(k * 100)
    };
}

// Add to color history
function addToHistory(r, g, b) {
    const color = { r, g, b };
    const colorStr = `rgb(${r}, ${g}, ${b})`;
    
    // Remove duplicate color
    colorHistory = colorHistory.filter(c => !(c.r === r && c.g === g && c.b === b));
    
    // Add to beginning
    colorHistory.unshift(color);
    
    // Keep maximum 10 colors
    if (colorHistory.length > 10) {
        colorHistory = colorHistory.slice(0, 10);
    }
    
    updateHistoryDisplay();
}

// Update history display
function updateHistoryDisplay() {
    const historyDiv = document.getElementById('colorHistory');
    
    if (colorHistory.length === 0) {
        historyDiv.innerHTML = '<small class="text-muted">No colors selected yet</small>';
        return;
    }
    
    historyDiv.innerHTML = colorHistory.map(color => {
        const colorStr = `rgb(${color.r}, ${color.g}, ${color.b})`;
        const hex = rgbToHex(color.r, color.g, color.b);
        return `<div class="color-history-item" style="width: 30px; height: 30px; background-color: ${colorStr}; border: 1px solid #ddd; margin: 2px; cursor: pointer; border-radius: 3px;" title="${hex}" onclick="selectHistoryColor(${color.r}, ${color.g}, ${color.b})"></div>`;
    }).join('');
}

// Select color from history
function selectHistoryColor(r, g, b) {
    updateColorInfo(0, 0, r, g, b);
}

// Copy all color codes
function copyAllColors() {
    const hex = document.getElementById('hexValue').value;
    const rgb = document.getElementById('rgbValue').value;
    const hsl = document.getElementById('hslValue').value;
    const cmyk = document.getElementById('cmykValue').value;
    
    const text = `HEX: ${hex}\nRGB: ${rgb}\nHSL: ${hsl}\nCMYK: ${cmyk}`;
    
    navigator.clipboard.writeText(text).then(() => {
        alert('✅ Color codes copied!');
    }).catch(() => {
        alert('❌ Copy failed!');
    });
}

// Clear history
function clearHistory() {
    colorHistory = [];
    updateHistoryDisplay();
}

// Reset image
function resetImage() {
    document.getElementById('uploadArea').style.display = 'block';
    document.getElementById('imageContainer').style.display = 'none';
    document.getElementById('imageInput').value = '';
    
    imageData = null;
    
    // Reset color information
    document.getElementById('coordinates').textContent = 'X: -, Y: -';
    document.getElementById('hexValue').value = '#ffffff';
    document.getElementById('rgbValue').value = 'rgb(255, 255, 255)';
    document.getElementById('hslValue').value = 'hsl(0, 0%, 100%)';
    document.getElementById('cmykValue').value = 'cmyk(0%, 0%, 0%, 0%)';
    document.getElementById('colorPreview').style.backgroundColor = '#ffffff';
}