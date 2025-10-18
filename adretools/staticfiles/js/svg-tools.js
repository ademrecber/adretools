// Raster'ı SVG'ye dönüştür (geliştirilmiş sürüm)
async function convertRasterToSVG() {
    if (!currentRasterFile) {
        alert('⚠️ İçerik Gerekli: Önce resim dosyası seçin!');
        return;
    }

    const formData = new FormData();
    formData.append('image_file', currentRasterFile);

    // Yeni: Dönüştürme modu seçicisi (embed veya vector)
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
            alert('❌ Sunucu Hatası: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Bağlantı Sorunu: Django sunucusu çalışmıyor olabilir. Lütfen sunucuyu başlatın.');
        } else {
            alert('⚠️ Beklenmeyen Hata: ' + error.message);
        }
    }
}
