function clearFilters() {
    // Resetea el formulario
    document.getElementById("filterForm").reset();
    // Redirige a la ruta de alumnos sin filtros
    window.location.href = alumnosUrl;
}
