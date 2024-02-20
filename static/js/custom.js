document.addEventListener('DOMContentLoaded', function () {
    
    var submit = document.getElementById('submit');
    var telechargement = document.querySelector('.telechargement');
    var btnDownload = document.querySelector('.btn-download');
    var btnDownload2 = document.querySelector('.btn-download-2');
    var captureButton = document.getElementById('captureButton');
    

    if(captureButton){
        captureButton.addEventListener('click',function(){
            captureView();
        });
    }
    function captureView() {
        setTimeout(function () {
            html2canvas(document.getElementById('map')).then(function (canvas) {
                // Convert the canvas to a data URL in JPEG format with specified quality
                var jpegDataUrl = canvas.toDataURL('image/jpeg', 0.9); // 0.9 is the quality value (0.0 to 1.0)
    
                // Create an anchor element to download the captured view as an image
                var link = document.createElement('a');
                link.href = jpegDataUrl;
                link.download = 'captured_view.jpg';
                link.click();
            });
        }, 1000);
    
        // Add any logic you need after capturing the view
    }
    

    if(submit){
        submit.addEventListener('click',function(){
            var file = document.querySelector('.file');
            file.style.display = 'none';
            telechargement.style.display = 'block';
        });
    }
    
    var element = document.getElementById('print-content');
    var element2 = document.getElementById('print-content-2');
    
    if(btnDownload){
        btnDownload.addEventListener('click',function(e){
            e.preventDefault();

            var options = {
                margin: 10, // Marge en pixels
                filename: 'Rapport_IRD.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 4 }, // Échelle pour améliorer la qualité sur les écrans haute résolution
                jsPDF: {
                    unit: 'mm',
                    format: [300, 300], // [largeur, hauteur]
                    orientation: 'portrait', // ou 'landscape' pour paysage
                    putOnlyUsedFonts: true,
                },
            };
            
            html2pdf(element, options);
        });
    }

    if(btnDownload2){
        btnDownload2.addEventListener('click',function(e){
            e.preventDefault();

            var options = {
                margin: 10, // Marge en pixels
                filename: 'Rapport_IRD.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 4 }, // Échelle pour améliorer la qualité sur les écrans haute résolution
                jsPDF: {
                    unit: 'mm',
                    format: [300, 400], // [largeur, hauteur]
                    orientation: 'portrait', // ou 'landscape' pour paysage
                    putOnlyUsedFonts: true,
                },
            };
            

            html2pdf(element2, options);
        });
    }
    
    
    const fileInput = document.getElementById('file-input');
    const fileDropArea = document.getElementById('file-drop-area');
    const fileLabel = document.getElementById('file-label');

    const fileInput1 = document.getElementById('file-input-1');
    const fileInput2 = document.getElementById('file-input-2');
    const fileDropArea1 = document.getElementById('file-drop-area-1');
    const fileDropArea2 = document.getElementById('file-drop-area-2');
    const fileLabel1 = document.getElementById('file-label-1');
    const fileLabel2 = document.getElementById('file-label-2');

    if(fileInput){
        fileInput.addEventListener('change', () => {
            const files = fileInput.files;
            if (files.length > 0) {
                if(files[0].name.length > 8){
                    fileLabel.innerHTML = files[0].name.substring(0,8)+"...";
                }
                else{
                    fileLabel.innerHTML = files[0].name;
                }
                fileLabel.style.fontSize = '50px';
            }
        });
    }


    if (fileDropArea) {
        fileDropArea.addEventListener('dragover', (event) => {
            event.preventDefault();
            fileDropArea.classList.add('highlight');
            updateFileLabel(event.clientX, event.clientY);
        });
    
        fileDropArea.addEventListener('dragenter', () => {
            // Afficher le message "Relâcher"
            fileLabel.innerHTML = 'Relâcher';
            fileLabel.style.fontSize = '50px';
        });
    
        fileDropArea.addEventListener('dragleave', (event) => {
            fileDropArea.classList.remove('highlight');
            updateFileLabel(event.clientX, event.clientY);
        });
    
        fileDropArea.addEventListener('drag', (event) => {
            updateFileLabel(event.clientX, event.clientY);
        });
    
        fileDropArea.addEventListener('drop', (event) => {
            event.preventDefault();
            fileDropArea.classList.remove('highlight');
            fileLabel.style.display = 'block';
    
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                if (files[0].name.length > 8) {
                    fileLabel.innerHTML = files[0].name.substring(0, 8) + "...";
                } else {
                    fileLabel.innerHTML = files[0].name;
                }
            }
        });
    
        fileDropArea.addEventListener('dragend', () => {
            // Revenir à l'état initial lorsque le glissement est terminé
            fileLabel.innerHTML = '<i class="bx bxs-down-arrow-circle" ></i>';
            fileLabel.style.display = 'block';
        });

        function updateFileLabel(x, y) {
            // Mettre à jour le label en fonction de la position du curseur
            const rect = fileDropArea.getBoundingClientRect();
            if (x > rect.left && x < rect.right && y > rect.top && y < rect.bottom) {
                fileLabel.innerHTML = 'Relâcher';
                fileLabel.style.fontSize = '50px';
            } else {
                fileLabel.innerHTML = '<i class="bx bxs-down-arrow-circle" ></i>';
                fileLabel.style.display = 'block';
            }
        }
    
    }
    

    if(fileInput1){
        fileInput1.addEventListener('change', () => {
            const files = fileInput1.files;
            if (files.length > 0) {
                if(files[0].name.length > 8){
                    fileLabel1.innerHTML = files[0].name.substring(0,8)+"...";
                }
                else{
                    fileLabel1.innerHTML = files[0].name;
                }
                fileLabel1.style.fontSize = '50px';
            }
        });
    }

    if (fileDropArea1) {
        fileDropArea1.addEventListener('dragover', (event) => {
            event.preventDefault();
            fileDropArea1.classList.add('highlight');
            updateFileLabel(event.clientX, event.clientY);
        });
    
        fileDropArea1.addEventListener('dragenter', () => {
            // Afficher le message "Relâcher"
            fileLabel1.innerHTML = 'Relâcher';
            fileLabel1.style.fontSize = '50px';
        });
    
        fileDropArea1.addEventListener('dragleave', (event) => {
            fileDropArea1.classList.remove('highlight');
            updateFileLabel(event.clientX, event.clientY);
        });
    
        fileDropArea1.addEventListener('drag', (event) => {
            updateFileLabel(event.clientX, event.clientY);
        });
    
        fileDropArea1.addEventListener('drop', (event) => {
            event.preventDefault();
            fileDropArea1.classList.remove('highlight');
            fileLabel1.style.display = 'block';
    
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                fileInput1.files = files;
                if (files[0].name.length > 8) {
                    fileLabel1.innerHTML = files[0].name.substring(0, 8) + "...";
                } else {
                    fileLabel1.innerHTML = files[0].name;
                }
            }
        });
    
        fileDropArea1.addEventListener('dragend', () => {
            // Revenir à l'état initial lorsque le glissement est terminé
            fileLabel1.innerHTML = '<i class="bx bxs-download"></i>';
            fileLabel1.style.display = 'block';
        });

        function updateFileLabel(x, y) {
            // Mettre à jour le label en fonction de la position du curseur
            const rect = fileDropArea1.getBoundingClientRect();
            if (x > rect.left && x < rect.right && y > rect.top && y < rect.bottom) {
                fileLabel1.innerHTML = 'Relâcher';
                fileLabel1.style.fontSize = '50px';
            } else {
                fileLabel1.innerHTML = '<i class="bx bxs-download"></i>';
                fileLabel1.style.display = 'block';
            }
        }
    
    }

    if(fileInput2){
        fileInput2.addEventListener('change', () => {
            const files = fileInput2.files;
            if (files.length > 0) {
                if(files[0].name.length > 8){
                    fileLabel2.innerHTML = files[0].name.substring(0,8)+"...";
                }
                else{
                    fileLabel2.innerHTML = files[0].name;
                }
                fileLabel2.style.fontSize = '50px';
            }
        });
    }

    if (fileDropArea2) {
        fileDropArea2.addEventListener('dragover', (event) => {
            event.preventDefault();
            fileDropArea2.classList.add('highlight');
            updateFileLabel(event.clientX, event.clientY);
        });
    
        fileDropArea2.addEventListener('dragenter', () => {
            // Afficher le message "Relâcher"
            fileLabel2.innerHTML = 'Relâcher';
            fileLabel2.style.fontSize = '50px';
        });
    
        fileDropArea2.addEventListener('dragleave', (event) => {
            fileDropArea2.classList.remove('highlight');
            updateFileLabel(event.clientX, event.clientY);
        });
    
        fileDropArea2.addEventListener('drag', (event) => {
            updateFileLabel(event.clientX, event.clientY);
        });
    
        fileDropArea2.addEventListener('drop', (event) => {
            event.preventDefault();
            fileDropArea2.classList.remove('highlight');
            fileLabel2.style.display = 'block';
    
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                fileInput2.files = files;
                if (files[0].name.length > 8) {
                    fileLabel2.innerHTML = files[0].name.substring(0, 8) + "...";
                } else {
                    fileLabel2.innerHTML = files[0].name;
                }
            }
        });
    
        fileDropArea2.addEventListener('dragend', () => {
            // Revenir à l'état initial lorsque le glissement est terminé
            fileLabel2.innerHTML = '<i class="bx bxs-download"></i>';
            fileLabel2.style.display = 'block';
        });

        function updateFileLabel(x, y) {
            // Mettre à jour le label en fonction de la position du curseur
            const rect = fileDropArea2.getBoundingClientRect();
            if (x > rect.left && x < rect.right && y > rect.top && y < rect.bottom) {
                fileLabel2.innerHTML = 'Relâcher';
                fileLabel2.style.fontSize = '50px';
            } else {
                fileLabel2.innerHTML = '<i class="bx bxs-download"></i>';
                fileLabel2.style.display = 'block';
            }
        }
    
    }

});