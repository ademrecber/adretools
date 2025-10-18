// PDF Dönüştürme Modülü
(function() {
    window.convertPDFToWord = async function() {
        console.log('convertPDFToWord fonksiyonu çağrıldı');
        
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'application/pdf';
        input.click();
        
        console.log('Dosya seçici açıldı');

        input.onchange = async () => {
            console.log('Dosya seçildi, input.files:', input.files);
            
            const file = input.files[0];
            if (!file) {
                console.log('Dosya seçilmedi, çıkılıyor');
                return;
            }
            
            console.log('Seçilen dosya:', file.name, 'Boyut:', file.size);

            try {
                console.log('FormData oluşturuluyor...');
                const formData = new FormData();
                formData.append('pdf', file);
                
                console.log('Fetch isteği gönderiliyor: /pdf/convert-to-word/');
                const response = await fetch('/pdf/convert-to-word/', {
                    method: 'POST',
                    body: formData
                });
                
                console.log('Response alındı:', response.status, response.statusText);
                
                if (response.ok) {
                    console.log('Response başarılı, blob alınıyor...');
                    const blob = await response.blob();
                    console.log('Blob alındı, boyut:', blob.size);
                    
                    const link = document.createElement('a');
                    link.href = URL.createObjectURL(blob);
                    link.download = file.name.replace('.pdf', '.docx');
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    console.log('Dosya indirildi');
                    alert('PDF başarıyla Word\'e dönüştürüldü!');
                } else {
                    console.log('Response başarısız, hata alınıyor...');
                    try {
                        const error = await response.json();
                        console.log('Hata mesajı:', error);
                        console.log('Hata mesajı detay:', JSON.stringify(error));
                        alert(error.error);
                    } catch (jsonError) {
                        console.log('JSON parse hatası:', jsonError);
                        alert('Dönüştürme hatası oluştu (JSON parse hatası)');
                    }
                }
            } catch (error) {
                console.log('Catch bloğu - Genel hata:', error);
                alert('Hata: ' + error.message);
            }
        };
    };

    window.convertPDFToExcel = async function() {
        console.log('convertPDFToExcel çağrıldı');
        
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'application/pdf';
        input.click();

        input.onchange = async () => {
            const file = input.files[0];
            if (!file) return;
            
            try {
                const formData = new FormData();
                formData.append('pdf', file);
                
                const response = await fetch('/pdf/convert-to-excel/', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const blob = await response.blob();
                    const link = document.createElement('a');
                    link.href = URL.createObjectURL(blob);
                    link.download = file.name.replace('.pdf', '.xlsx');
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    alert('PDF başarıyla Excel\'e dönüştürüldü!');
                } else {
                    const error = await response.json();
                    alert(error.error);
                }
            } catch (error) {
                alert('Hata: ' + error.message);
            }
        };
    };

    window.convertWordToPDF = async function() {
        console.log('convertWordToPDF fonksiyonu çağrıldı');
        
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.doc,.docx';
        input.click();
        
        console.log('Word dosya seçici açıldı');

        input.onchange = async () => {
            console.log('Word dosyası seçildi, input.files:', input.files);
            
            const file = input.files[0];
            if (!file) {
                console.log('Word dosyası seçilmedi, çıkılıyor');
                return;
            }
            
            console.log('Seçilen Word dosyası:', file.name, 'Boyut:', file.size);

            try {
                console.log('Word FormData oluşturuluyor...');
                const formData = new FormData();
                formData.append('word', file);
                
                console.log('Word Fetch isteği gönderiliyor: /pdf/convert-to-pdf/');
                const response = await fetch('/pdf/convert-to-pdf/', {
                    method: 'POST',
                    body: formData
                });
                
                console.log('Word Response alındı:', response.status, response.statusText);
                
                if (response.ok) {
                    console.log('Word Response başarılı, blob alınıyor...');
                    const blob = await response.blob();
                    console.log('Word Blob alındı, boyut:', blob.size);
                    
                    const link = document.createElement('a');
                    link.href = URL.createObjectURL(blob);
                    link.download = file.name.replace('.docx', '.pdf').replace('.doc', '.pdf');
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    console.log('Word PDF dosyası indirildi');
                    alert('Word başarıyla PDF\'e dönüştürüldü!');
                } else {
                    console.log('Word Response başarısız, hata alınıyor...');
                    try {
                        const error = await response.json();
                        console.log('Word Hata mesajı:', error);
                        alert(error.error);
                    } catch (jsonError) {
                        console.log('Word JSON parse hatası:', jsonError);
                        alert('Word dönüştürme hatası oluştu (JSON parse hatası)');
                    }
                }
            } catch (error) {
                console.log('Word Catch bloğu - Genel hata:', error);
                alert('Hata: ' + error.message);
            }
        };
    };
})();