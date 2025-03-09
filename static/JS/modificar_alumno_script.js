// Función para habilitar un campo removiendo el atributo 'readonly'
function enableField(fieldId) {
    var field = document.getElementById(fieldId);
    if (field) {
        field.removeAttribute('readonly');
    }
}
