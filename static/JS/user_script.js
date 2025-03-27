// Función para borrar filtros: resetea el formulario y redirige a la URL base de coordinadores/directivos
function clearFilters() {
    document.getElementById("filterForm").reset();
    window.location.href = coordinadoresUrl;
}

// Configuración para el auto-envío (debounce)
let typingTimer;
const doneTypingInterval = 500; // Tiempo en milisegundos

// Selecciona todos los campos que tienen la clase "auto-submit"
const autoSubmitFields = document.querySelectorAll('.auto-submit');
const filterForm = document.getElementById('filterForm');

// Agrega los eventos a cada campo
autoSubmitFields.forEach(field => {
    // Para inputs: escucha el evento keyup
    field.addEventListener('keyup', () => {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(() => {
            filterForm.submit();
        }, doneTypingInterval);
    });
    // Para selects (u otros) o cambios inmediatos: envía el formulario al cambiar la opción
    field.addEventListener('change', () => {
        filterForm.submit();
    });
});
