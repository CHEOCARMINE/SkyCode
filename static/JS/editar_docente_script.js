// Función para habilitar el campo seleccionado al presionar el lápiz
function enableField(fieldId) {
    var field = document.getElementById(fieldId);
    if (field) {
        field.readOnly = false; // Elimina la propiedad de solo lectura
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Al enviar el formulario, asegurarse de que todos los valores se envíen
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            const fields = document.querySelectorAll('.form-control');
            fields.forEach(function(field) {
                field.readOnly = false; // Asegura que todos los valores se envíen correctamente
            });
        });
    }
});
