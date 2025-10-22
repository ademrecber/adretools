// Image ↔ PDF Module
let selectedImageFiles = [];

async function imagesToPDF() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.multiple = true;
    input.click();

    input.onchange = async () => {
        selectedImageFiles = Array.from(input.files);
        const display = document.getElementById('selectedImages');
        
        if (selectedImageFiles.length > 0) {
            display.innerHTML = `
                <div class="alert alert-info">
                    ${selectedImageFiles.length} images selected
                    <button class="btn btn-sm btn-success ms-2" onclick="createPDFFromImages()">Create PDF</button>
                </div>
            `;
        }
    };
}

async function createPDFFromImages() {
    if (selectedImageFiles.length === 0) {
        alert("Please select images!");
        return;
    }

    try {
        const pdfDoc = await PDFLib.PDFDocument.create();

        for (const imageFile of selectedImageFiles) {
            const imageBytes = await imageFile.arrayBuffer();
            let image;
            
            if (imageFile.type === 'image/png') {
                image = await pdfDoc.embedPng(imageBytes);
            } else {
                image = await pdfDoc.embedJpg(imageBytes);
            }

            const page = pdfDoc.addPage();
            const { width, height } = page.getSize();
            
            // Fit image to page
            const imageAspectRatio = image.width / image.height;
            const pageAspectRatio = width / height;
            
            let drawWidth, drawHeight;
            if (imageAspectRatio > pageAspectRatio) {
                drawWidth = width - 40; // 20px margin
                drawHeight = drawWidth / imageAspectRatio;
            } else {
                drawHeight = height - 40; // 20px margin
                drawWidth = drawHeight * imageAspectRatio;
            }

            page.drawImage(image, {
                x: (width - drawWidth) / 2,
                y: (height - drawHeight) / 2,
                width: drawWidth,
                height: drawHeight,
            });
        }

        const pdfBytes = await pdfDoc.save();
        const blob = new Blob([pdfBytes], { type: 'application/pdf' });

        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'images_to_pdf.pdf';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        selectedImageFiles = [];
        document.getElementById('selectedImages').innerHTML = '';
        alert("PDF successfully created!");

    } catch (error) {
        alert("Error: " + error.message);
    }
}

async function pdfToImages() {
    const format = document.getElementById('imageFormat').value;
    
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/pdf';
    input.click();

    input.onchange = async () => {
        const file = input.files[0];
        if (!file) return;

        try {
            // Load PDF.js library
            if (!window.pdfjsLib) {
                const script = document.createElement('script');
                script.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
                document.head.appendChild(script);
                
                await new Promise(resolve => {
                    script.onload = resolve;
                });
                
                window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
            }

            const arrayBuffer = await file.arrayBuffer();
            const pdf = await window.pdfjsLib.getDocument(arrayBuffer).promise;
            
            for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
                const page = await pdf.getPage(pageNum);
                const viewport = page.getViewport({ scale: 2.0 });
                
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                canvas.height = viewport.height;
                canvas.width = viewport.width;
                
                await page.render({
                    canvasContext: context,
                    viewport: viewport
                }).promise;
                
                // Create image from canvas
                canvas.toBlob((blob) => {
                    const link = document.createElement('a');
                    link.href = URL.createObjectURL(blob);
                    link.download = `page_${pageNum}.${format}`;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }, `image/${format}`, 0.9);
                
                await new Promise(resolve => setTimeout(resolve, 500));
            }
            
            alert(`PDF converted to ${pdf.numPages} images!`);
            
        } catch (error) {
            alert('Error: ' + error.message);
        }
    };
}