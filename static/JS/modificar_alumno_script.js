function enableField(fieldId) {
    var field = document.getElementById(fieldId);
    if (field) {
        if (field.disabled) {
            field.disabled = false;
        } else {
            field.readOnly = false;
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('.custom-upload input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const labelSpan = this.parentNode.querySelector('.file-label-text span');
            if (!file) {
                labelSpan.textContent = "Subir archivo";
                labelSpan.style.color = "";
                return;
            }
            const fileName = file.name;
            const maxSize = 2 * 1024 * 1024; // 2MB en bytes
            if (file.size > maxSize) {
                labelSpan.textContent = fileName + " (Excede 2MB)";
                labelSpan.style.color = "#E74C3C"; // Rojo
            } else {
                labelSpan.textContent = fileName;
                labelSpan.style.color = "#27AE60"; // Verde
            }
        });
    });

    // Al enviar el formulario, quitar el atributo disabled de los selects para que sus valores se envíen
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            var estadoSelect = document.getElementById('estado_alumno');
            if (estadoSelect) {
                estadoSelect.disabled = false;
            }
            var carreraSelect = document.getElementById('carrera_alumno');
            if (carreraSelect) {
                carreraSelect.disabled = false;
            }
        });
    }
});
