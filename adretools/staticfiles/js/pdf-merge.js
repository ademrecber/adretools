// PDF Birleştirme Modülü
let selectedFiles = [];

function addPDF() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/pdf';
    input.click();

    input.onchange = () => {
        const file = input.files[0];
        if (!file) return;

        selectedFiles.push(file);
        updateFileList();
    };
}

function updateFileList() {
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';
    selectedFiles.forEach((file, index) => {
        const div = document.createElement('div');
        div.className = 'list-group-item d-flex justify-content-between align-items-center';
        div.innerHTML = `
            ${file.name}
            <button class="btn btn-sm btn-danger" onclick="removeFile(${index})">Kaldır</button>
        `;
        fileList.appendChild(div);
    });
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    updateFileList();
}

async function mergeSelectedPDFs() {
    if (selectedFiles.length === 0) {
        alert("Birleştirilecek PDF seçilmedi.");
        return;
    }

    const mergedPdf = await PDFLib.PDFDocument.create();

    for (const file of selectedFiles) {
        const arrayBuffer = await file.arrayBuffer();
        const pdf = await PDFLib.PDFDocument.load(arrayBuffer);
        const copiedPages = await mergedPdf.copyPages(pdf, pdf.getPageIndices());
        copiedPages.forEach(page => mergedPdf.addPage(page));
    }

    const pdfBytes = await mergedPdf.save();
    const blob = new Blob([pdfBytes], { type: 'application/pdf' });

    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'birlestirilmis.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    selectedFiles = [];
    updateFileList();
    alert("PDF birleştirme tamamlandı.");
}