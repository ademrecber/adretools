// PDF Editing Module

async function rotatePDF() {
    const angle = parseInt(document.getElementById('rotationAngle').value);
    
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/pdf';
    input.click();

    input.onchange = async () => {
        const file = input.files[0];
        if (!file) return;

        try {
            const arrayBuffer = await file.arrayBuffer();
            const pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer);
            
            const pages = pdfDoc.getPages();
            
            for (const page of pages) {
                page.setRotation(PDFLib.degrees(angle));
            }

            const pdfBytes = await pdfDoc.save();
            const blob = new Blob([pdfBytes], { type: 'application/pdf' });

            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `${file.name.replace('.pdf', '')}_rotated.pdf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            alert(`PDF rotated by ${angle}°!`);
            
        } catch (error) {
            alert('Error: ' + error.message);
        }
    };
}

async function addBlankPage() {
    const position = parseInt(document.getElementById('pagePosition').value);
    if (!position || position < 1) {
        alert("Please enter a valid page position!");
        return;
    }
    
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/pdf';
    input.click();

    input.onchange = async () => {
        const file = input.files[0];
        if (!file) return;

        try {
            const arrayBuffer = await file.arrayBuffer();
            const pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer);
            
            const totalPages = pdfDoc.getPageCount();
            
            if (position > totalPages + 1) {
                alert(`Position cannot be greater than ${totalPages + 1}!`);
                return;
            }
            
            // Add blank page
            const blankPage = pdfDoc.insertPage(position - 1);
            blankPage.setSize(595, 842); // A4 size

            const pdfBytes = await pdfDoc.save();
            const blob = new Blob([pdfBytes], { type: 'application/pdf' });

            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `${file.name.replace('.pdf', '')}_blank_page.pdf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            alert(`Blank page added at position ${position}!`);
            document.getElementById('pagePosition').value = '';
            
        } catch (error) {
            alert('Error: ' + error.message);
        }
    };
}