// Çoklu PDF Bölme Modülü
(function() {
    let selectedPDFMulti = null;

    window.selectPDF = function() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'application/pdf';
        input.click();

        input.onchange = () => {
            selectedPDFMulti = input.files[0];
            const display = document.getElementById('selectedFileDisplay');
            display.innerHTML = `
                <div class="alert alert-info">
                    <strong>${selectedPDFMulti.name}</strong> seçildi
                    <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeSelectedPDF()">Kaldır</button>
                </div>
            `;
        };
    };

    window.removeSelectedPDF = function() {
        selectedPDFMulti = null;
        document.getElementById('selectedFileDisplay').innerHTML = '';
    };

    window.addRange = function() {
        const container = document.getElementById('rangeContainer');
        const div = document.createElement('div');
        div.className = 'input-group mb-2';
        div.innerHTML = `
            <input type="text" class="form-control" placeholder="örn: 5-10 veya 99">
            <button class="btn btn-outline-danger" onclick="this.parentElement.remove()">Kaldır</button>
        `;
        container.appendChild(div);
    };

    window.splitMultipleRanges = async function() {
        if (!selectedPDFMulti) {
            alert("Lütfen önce bir PDF seçin.");
            return;
        }

        const arrayBuffer = await selectedPDFMulti.arrayBuffer();
        const pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer);
        const totalPages = pdfDoc.getPageCount();

        const rangeInputs = document.querySelectorAll('#rangeContainer input');
        const ranges = [];

        for (const input of rangeInputs) {
            const value = input.value.trim();
            if (!value) continue;

            let start, end;
            if (value.includes('-')) {
                const match = value.match(/^(\d+)-(\d+)$/);
                if (!match) {
                    alert(`Geçersiz aralık: ${value}`);
                    return;
                }
                start = parseInt(match[1], 10) - 1;
                end = parseInt(match[2], 10) - 1;
            } else {
                const pageNum = parseInt(value, 10);
                if (isNaN(pageNum)) {
                    alert(`Geçersiz sayfa: ${value}`);
                    return;
                }
                start = end = pageNum - 1;
            }

            if (start < 0 || end >= totalPages || start > end) {
                alert(`Geçersiz aralık: ${value}`);
                return;
            }

            ranges.push({ start, end, label: value });
        }

        for (const range of ranges) {
            const newPdf = await PDFLib.PDFDocument.create();
            const pages = await newPdf.copyPages(pdfDoc, 
                Array.from({ length: range.end - range.start + 1 }, (_, i) => i + range.start)
            );
            pages.forEach(page => newPdf.addPage(page));

            const pdfBytes = await newPdf.save();
            const blob = new Blob([pdfBytes], { type: 'application/pdf' });

            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `sayfa_${range.label}.pdf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            await new Promise(resolve => setTimeout(resolve, 300));
        }

        alert("Çoklu bölme tamamlandı.");
    };
})();