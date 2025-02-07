function validateInput(input, errorElement) {
    const value = input.value;
    if (value.length > 10 || value.includes(".")) {
        errorElement.style.display = "block";
        input.classList.add("is-invalid");
    } else {
        errorElement.style.display = "none";
        input.classList.remove("is-invalid");
    }
}

function validateForm() {
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const usernameError = document.getElementById("username-error");
    const passwordError = document.getElementById("password-error");

    validateInput(username, usernameError);
    validateInput(password, passwordError);

    if (username.classList.contains("is-invalid") || password.classList.contains("is-invalid")) {
        return;
    }

    alert("Inicio de sesión exitoso");
}

// Detectar cambios en los inputs y validar en tiempo real
document.getElementById("username").addEventListener("input", function () {
    validateInput(this, document.getElementById("username-error"));
});

document.getElementById("password").addEventListener("input", function () {
    validateInput(this, document.getElementById("password-error"));
});
