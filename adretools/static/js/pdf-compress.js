// PDF Compression Module

async function compressPDF() {
    const compressionLevel = document.getElementById('compressionLevel').value;
    
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/pdf';
    input.click();

    input.onchange = async () => {
        const file = input.files[0];
        if (!file) return;

        try {
            const originalSize = (file.size / 1024 / 1024).toFixed(2);
            
            const arrayBuffer = await file.arrayBuffer();
            const pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer);
            
            // Simple compression - clear metadata
            pdfDoc.setTitle('');
            pdfDoc.setAuthor('');
            pdfDoc.setSubject('');
            pdfDoc.setKeywords([]);
            pdfDoc.setProducer('');
            pdfDoc.setCreator('');
            
            const pdfBytes = await pdfDoc.save({
                useObjectStreams: true,
                addDefaultPage: false
            });
            
            const newSize = (pdfBytes.length / 1024 / 1024).toFixed(2);
            const savings = ((1 - pdfBytes.length / file.size) * 100).toFixed(1);
            
            const blob = new Blob([pdfBytes], { type: 'application/pdf' });

            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `${file.name.replace('.pdf', '')}_compressed.pdf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            alert(`PDF compressed!\nOriginal: ${originalSize} MB\nNew: ${newSize} MB\nSavings: %${savings}`);
            
        } catch (error) {
            alert('Error: ' + error.message);
        }
    };
}