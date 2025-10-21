// PDF Conversion Module
(function() {
    window.convertPDFToWord = async function() {
        console.log('convertPDFToWord function called');
        
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'application/pdf';
        input.click();
        
        console.log('File picker opened');

        input.onchange = async () => {
            console.log('File selected, input.files:', input.files);
            
            const file = input.files[0];
            if (!file) {
                console.log('No file selected, exiting');
                return;
            }
            
            console.log('Selected file:', file.name, 'Size:', file.size);

            try {
                console.log('Creating FormData...');
                const formData = new FormData();
                formData.append('pdf', file);
                
                console.log('Sending fetch request: /pdf/convert-to-word/');
                const response = await fetch('/pdf/convert-to-word/', {
                    method: 'POST',
                    body: formData
                });
                
                console.log('Response received:', response.status, response.statusText);
                
                if (response.ok) {
                    console.log('Response successful, retrieving blob...');
                    const blob = await response.blob();
                    console.log('Blob retrieved, size:', blob.size);
                    
                    const link = document.createElement('a');
                    link.href = URL.createObjectURL(blob);
                    link.download = file.name.replace('.pdf', '.docx');
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    console.log('File downloaded');
                    alert('PDF successfully converted to Word!');
                } else {
                    console.log('Response failed, retrieving error...');
                    try {
                        const error = await response.json();
                        console.log('Error message:', error);
                        console.log('Error message details:', JSON.stringify(error));
                        alert(error.error);
                    } catch (jsonError) {
                        console.log('JSON parse error:', jsonError);
                        alert('Conversion error occurred (JSON parse error)');
                    }
                }
            } catch (error) {
                console.log('Catch block - General error:', error);
                alert('Error: ' + error.message);
            }
        };
    };

    window.convertPDFToExcel = async function() {
        console.log('convertPDFToExcel called');
        
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
                    
                    alert('PDF successfully converted to Excel!');
                } else {
                    const error = await response.json();
                    alert(error.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        };
    };

    window.convertWordToPDF = async function() {
        console.log('convertWordToPDF function called');
        
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.doc,.docx';
        input.click();
        
        console.log('Word file picker opened');

        input.onchange = async () => {
            console.log('Word file selected, input.files:', input.files);
            
            const file = input.files[0];
            if (!file) {
                console.log('No Word file selected, exiting');
                return;
            }
            
            console.log('Selected Word file:', file.name, 'Size:', file.size);

            try {
                console.log('Creating Word FormData...');
                const formData = new FormData();
                formData.append('word', file);
                
                console.log('Sending Word fetch request: /pdf/convert-to-pdf/');
                const response = await fetch('/pdf/convert-to-pdf/', {
                    method: 'POST',
                    body: formData
                });
                
                console.log('Word Response received:', response.status, response.statusText);
                
                if (response.ok) {
                    console.log('Word Response successful, retrieving blob...');
                    const blob = await response.blob();
                    console.log('Word Blob retrieved, size:', blob.size);
                    
                    const link = document.createElement('a');
                    link.href = URL.createObjectURL(blob);
                    link.download = file.name.replace('.docx', '.pdf').replace('.doc', '.pdf');
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    console.log('Word PDF file downloaded');
                    alert('Word successfully converted to PDF!');
                } else {
                    console.log('Word Response failed, retrieving error...');
                    try {
                        const error = await response.json();
                        console.log('Word Error message:', error);
                        alert(error.error);
                    } catch (jsonError) {
                        console.log('Word JSON parse error:', jsonError);
                        alert('Word conversion error occurred (JSON parse error)');
                    }
                }
            } catch (error) {
                console.log('Word Catch block - General error:', error);
                alert('Error: ' + error.message);
            }
        };
    };
})();