document.addEventListener('DOMContentLoaded', function() {
    // Selecciona todos los inputs de tipo file dentro de .custom-upload
    const fileInputs = document.querySelectorAll('.custom-upload input[type="file"]');
  
    fileInputs.forEach(function(input) {
      input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        // Busca el <span> que muestra el texto en el label
        const labelText = this.parentNode.querySelector('.file-label-text');
  
        if (!file) {
          // Si el usuario cancela la selección
          labelText.textContent = "Subir archivo";
          labelText.style.color = ""; // Restablece el color por defecto
          return;
        }
  
        const fileName = file.name;
        const maxSize = 2 * 1024 * 1024; // 2MB en bytes
  
        if (file.size > maxSize) {
          // Archivo excede el tamaño permitido
          labelText.textContent = fileName + " (Excede 2MB)";
          labelText.style.color = "#E74C3C"; // Rojo
        } else {
          // Archivo válido
          labelText.textContent = fileName;
          labelText.style.color = "#27AE60"; // Verde
        }
      });
    });
  });
  