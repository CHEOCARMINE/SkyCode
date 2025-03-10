function enableField(fieldId) {
    var field = document.getElementById(fieldId);
    if (field) {
        // Si es un select, remueve el atributo "disabled"
        if (field.tagName.toLowerCase() === "select") {
            field.removeAttribute("disabled");
        } else {
            // Para otros inputs, remueve el atributo "readonly"
            field.removeAttribute("readonly");
        }
    }
}
