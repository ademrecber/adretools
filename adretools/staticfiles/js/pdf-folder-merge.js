// Klasör Birleştirme Modülü
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
            alert("Seçilen klasörde PDF dosyası bulunamadı.");
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
            ${folder.path} (${folder.files.length} PDF)
            <button class="btn btn-sm btn-danger" onclick="removeFolder(${index})">Kaldır</button>
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
        alert("En az iki klasör seçilmelidir.");
        return;
    }

    const fileMaps = selectedFolders.map(folder => 
        new Map(folder.files.map(f => [f.name, f]))
    );
    
    const commonNames = [...fileMaps[0].keys()].filter(name => 
        fileMaps.every(map => map.has(name))
    );

    if (commonNames.length === 0) {
        alert("Ortak isimde PDF bulunamadı.");
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
        link.download = `${name.replace(/\.pdf$/i, '')}_birlestirilmis.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        await new Promise(resolve => setTimeout(resolve, 300));
    }

    selectedFolders = [];
    updateFolderList();
    alert(`${commonNames.length} adet PDF birleştirildi.`);
}