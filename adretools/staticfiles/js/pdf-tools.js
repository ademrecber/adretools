// PDF Tools JavaScript - Modüler yapı
let selectedFiles = [];
let selectedPDF = null;

function showTool(toolId) {
    // Tüm araçları gizle
    document.querySelectorAll('.tool-section').forEach(section => {
        section.style.display = 'none';
    });
    // Seçilen aracı göster
    const toolElement = document.getElementById(toolId);
    toolElement.style.display = 'block';
    
    // Smooth scroll ile araca git
    setTimeout(() => {
        toolElement.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }, 100);
}

// PDF Bölme
async function splitPDF() {
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
            link.download = `page${i + 1}.pdf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            await new Promise(resolve => setTimeout(resolve, 300));
        }
        alert("PDF splitting completed.");
    };
}

// PDF Birleştirme
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
            <button class="btn btn-sm btn-danger" onclick="removeFile(${index})">Remove</button>
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
        alert("No PDFs selected for merging.");
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
    link.download = 'merged.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    selectedFiles = [];
    updateFileList();
    alert("PDF merging completed.");
}

// Çoklu Bölme
function selectPDF() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/pdf';
    input.click();

    input.onchange = () => {
        selectedPDF = input.files[0];
        const display = document.getElementById('selectedFileDisplay');
        display.innerHTML = `
            <div class="alert alert-info">
                <strong>${selectedPDF.name}</strong> selected
                <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeSelectedPDF()">Remove</button>
            </div>
        `;
    };
}

function removeSelectedPDF() {
    selectedPDF = null;
    document.getElementById('selectedFileDisplay').innerHTML = '';
}

function addRange() {
    const container = document.getElementById('rangeContainer');
    const div = document.createElement('div');
    div.className = 'input-group mb-2';
    div.innerHTML = `
        <input type="text" class="form-control" placeholder="e.g: 5-10 or 99">
        <button class="btn btn-outline-danger" onclick="this.parentElement.remove()">Remove</button>
    `;
    container.appendChild(div);
}

async function splitMultipleRanges() {
    if (!selectedPDF) {
        alert("Please select a PDF first.");
        return;
    }

    const arrayBuffer = await selectedPDF.arrayBuffer();
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
                alert(`Invalid range: ${value}`);
                return;
            }
            start = parseInt(match[1], 10) - 1;
            end = parseInt(match[2], 10) - 1;
        } else {
            const pageNum = parseInt(value, 10);
            if (isNaN(pageNum)) {
                alert(`Invalid page: ${value}`);
                return;
            }
            start = end = pageNum - 1;
        }

        if (start < 0 || end >= totalPages || start > end) {
            alert(`Invalid range: ${value}`);
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
        link.download = `page_${range.label}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        await new Promise(resolve => setTimeout(resolve, 300));
    }

    alert("Multi-page split completed.");
}

// Klasör Birleştirme
let selectedFolders = [];

function addFolder() {
    const input = document.createElement('input');
    input.type = 'file';
    input.webkitdirectory = true;
    input.multiple = true;
    input.click();

    input.onchange = () => {
        const files = Array.from(input.files).filter(f => f.name.toLowerCase().endsWith('.pdf'));
        if (files.length === 0) {
            alert("No PDF files found in the selected folder.");
            return;
        }

        const folderPath = files[0].webkitRelativePath.split('/')[0];
        selectedFolders.push({ files, path: folderPath });
        updateFolderList();
    };
}

function updateFolderList() {
    const folderList = document.getElementById('folderList');
    folderList.innerHTML = '';
    selectedFolders.forEach((folder, index) => {
        const div = document.createElement('div');
        div.className = 'list-group-item d-flex justify-content-between align-items-center';
        div.innerHTML = `
            ${folder.path} (${folder.files.length} PDFs)
            <button class="btn btn-sm btn-danger" onclick="removeFolder(${index})">Remove</button>
        `;
        folderList.appendChild(div);
    });
}

function removeFolder(index) {
    selectedFolders.splice(index, 1);
    updateFolderList();
}

async function mergeFolderPDFs() {
    if (selectedFolders.length < 2) {
        alert("At least two folders must be selected.");
        return;
    }

    const fileMaps = selectedFolders.map(folder => 
        new Map(folder.files.map(f => [f.name, f]))
    );
    
    const commonNames = [...fileMaps[0].keys()].filter(name => 
        fileMaps.every(map => map.has(name))
    );

    if (commonNames.length === 0) {
        alert("No PDFs with common names found.");
        return;
    }

    for (const name of commonNames) {
        const mergedPdf = await PDFLib.PDFDocument.create();

        for (const folder of selectedFolders) {
            const file = folder.files.find(f => f.name === name);
            const arrayBuffer = await file.arrayBuffer();
            const pdf = await PDFLib.PDFDocument.load(arrayBuffer);
            const copiedPages = await mergedPdf.copyPages(pdf, pdf.getPageIndices());
            copiedPages.forEach(page => mergedPdf.addPage(page));
        }

        const pdfBytes = await mergedPdf.save();
        const blob = new Blob([pdfBytes], { type: 'application/pdf' });

        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `${name.replace(/\.pdf$/i, '')}_merged.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        await new Promise(resolve => setTimeout(resolve, 300));
    }

    selectedFolders = [];
    updateFolderList();
    alert(`${commonNames.length} PDFs merged.`);
}

// Aralıklı Bölme
let intervalPDF = null;

function selectIntervalPDF() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/pdf';
    input.click();

    input.onchange = () => {
        intervalPDF = input.files[0];
        const display = document.getElementById('intervalFileDisplay');
        display.innerHTML = `
            <div class="alert alert-info">
                <strong>${intervalPDF.name}</strong> selected
                <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeIntervalPDF()">Remove</button>
            </div>
        `;
    };
}

function removeIntervalPDF() {
    intervalPDF = null;
    document.getElementById('intervalFileDisplay').innerHTML = '';
}

async function splitByInterval() {
    if (!intervalPDF) {
        alert("Please select a PDF first.");
        return;
    }

    const intervalSize = parseInt(document.getElementById('intervalSize').value);
    const startPage = parseInt(document.getElementById('startPage').value);

    if (intervalSize < 1 || startPage < 1) {
        alert("Invalid values. Please enter positive numbers.");
        return;
    }

    const arrayBuffer = await intervalPDF.arrayBuffer();
    const pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer);
    const totalPages = pdfDoc.getPageCount();

    if (startPage > totalPages) {
        alert(`Start page (${startPage}) cannot be greater than total pages (${totalPages}).`);
        return;
    }

    let currentPage = startPage - 1; // 0-based index
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
        link.download = `part_${partNumber}_page_${currentPage + 1}-${endPage + 1}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        currentPage += intervalSize;
        partNumber++;
        
        await new Promise(resolve => setTimeout(resolve, 300));
    }

    alert(`PDF split into ${partNumber - 1} parts.`);
}