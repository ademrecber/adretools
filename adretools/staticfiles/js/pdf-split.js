// PDF Bölme Modülü
(function() {
    let selectedPDFSplit = null;

    // Tek sayfa bölme
    window.splitPDF = async function() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'application/pdf';
        input.click();

        input.onchange = async () => {
            const file = input.files[0];
            if (!file) return;

            const arrayBuffer = await file.arrayBuffer();
            const pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer);

            for (let i = 0; i < pdfDoc.getPageCount(); i++) {
                const newPdf = await PDFLib.PDFDocument.create();
                const [copiedPage] = await newPdf.copyPages(pdfDoc, [i]);
                newPdf.addPage(copiedPage);

                const pdfBytes = await newPdf.save();
                const blob = new Blob([pdfBytes], { type: 'application/pdf' });

                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = `sayfa${i + 1}.pdf`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

                await new Promise(resolve => setTimeout(resolve, 300));
            }
            alert("PDF bölme tamamlandı.");
        };
    };

    // Aralıklı bölme
    window.selectIntervalPDF = function() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'application/pdf';
        input.click();

        input.onchange = () => {
            selectedPDFSplit = input.files[0];
            const display = document.getElementById('intervalFileDisplay');
            display.innerHTML = `
                <div class="alert alert-info">
                    <strong>${selectedPDFSplit.name}</strong> seçildi
                    <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeIntervalPDF()">Kaldır</button>
                </div>
            `;
        };
    };

    window.removeIntervalPDF = function() {
        selectedPDFSplit = null;
        document.getElementById('intervalFileDisplay').innerHTML = '';
    };

    window.splitByInterval = async function() {
        if (!selectedPDFSplit) {
            alert("Lütfen önce bir PDF seçin.");
            return;
        }

        const intervalSize = parseInt(document.getElementById('intervalSize').value);
        const startPage = parseInt(document.getElementById('startPage').value);

        if (intervalSize < 1 || startPage < 1) {
            alert("Geçersiz değerler. Lütfen pozitif sayılar girin.");
            return;
        }

        const arrayBuffer = await selectedPDFSplit.arrayBuffer();
        const pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer);
        const totalPages = pdfDoc.getPageCount();

        if (startPage > totalPages) {
            alert(`Başlangıç sayfası (${startPage}) toplam sayfa sayısından (${totalPages}) büyük olamaz.`);
            return;
        }

        let currentPage = startPage - 1;
        let partNumber = 1;

        while (currentPage < totalPages) {
            const endPage = Math.min(currentPage + intervalSize - 1, totalPages - 1);
            
            const newPdf = await PDFLib.PDFDocument.create();
            const pageIndices = [];
            
            for (let i = currentPage; i <= endPage; i++) {
                pageIndices.push(i);
            }
            
            const copiedPages = await newPdf.copyPages(pdfDoc, pageIndices);
            copiedPages.forEach(page => newPdf.addPage(page));

            const pdfBytes = await newPdf.save();
            const blob = new Blob([pdfBytes], { type: 'application/pdf' });

            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `bolum_${partNumber}_sayfa_${currentPage + 1}-${endPage + 1}.pdf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            currentPage += intervalSize;
            partNumber++;
            
            await new Promise(resolve => setTimeout(resolve, 300));
        }

        alert(`PDF ${partNumber - 1} parçaya bölündü.`);
    };
})();