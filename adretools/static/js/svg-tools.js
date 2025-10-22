// Convert Raster to SVG (enhanced version)
async function convertRasterToSVG() {
    if (!currentRasterFile) {
        alert('⚠️ Content Required: Please select an image file first!');
        return;
    }

    const formData = new FormData();
    formData.append('image_file', currentRasterFile);

    // New: Conversion mode selector (embed or vector)
    const modeSelect = document.getElementById('convertMode');
    const mode = modeSelect ? modeSelect.value : 'embed';
    formData.append('mode', mode);

    try {
        const response = await fetch('/svg/raster-to-svg/', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            downloadBlob(blob, `${currentRasterFile.name.split('.')[0]}.svg`);
        } else {
            const error = await response.json();
            alert('❌ Server Error: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Connection Issue: The Django server may not be running. Please start the server.');
        } else {
            alert('⚠️ Unexpected Error: ' + error.message);
        }
    }
}