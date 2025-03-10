function enableField(fieldId) {
    var field = document.getElementById(fieldId);
    if (field) {
        if (field.hasAttribute("disabled")) {
            field.removeAttribute("disabled");
        } else {
            field.removeAttribute("readonly");
        }
    }
}
document.addEventListener('DOMContentLoaded', function() {
    // Selecciona todos los inputs de tipo file dentro de .custom-upload
    const fileInputs = document.querySelectorAll('.custom-upload input[type="file"]');

    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            // Busca el <span> que muestra el texto dentro del label
            const labelSpan = this.parentNode.querySelector('.file-label-text span');

            if (!file) {
                // Si el usuario cancela la selección
                labelSpan.textContent = "Subir archivo";
                labelSpan.style.color = "";
                return;
            }

            const fileName = file.name;
            const maxSize = 2 * 1024 * 1024; // 2MB

            if (file.size > maxSize) {
                // Archivo excede el tamaño permitido
                labelSpan.textContent = fileName + " (Excede 2MB)";
                labelSpan.style.color = "#E74C3C"; // Rojo
            } else {
                // Archivo válido
                labelSpan.textContent = fileName;
                labelSpan.style.color = "#27AE60"; // Verde
            }
        });
    });
});
