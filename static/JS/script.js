document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    const messageDiv = document.getElementById("message");

    function showMessage(message, type) {
        messageDiv.className = "message " + type;
        messageDiv.innerText = message;
        messageDiv.style.display = "block";
    }

    loginForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const userId = document.getElementById("id").value.trim();
        const password = document.getElementById("password").value.trim();

        if (userId.length === 0 || password.length === 0) {
            showMessage("Por favor, completa todos los campos.", "error");
            return;
        }

        fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: userId, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showMessage("Inicio de sesión exitoso, redirigiendo...", "success");
                setTimeout(() => {
                    window.location.href = "/dashboard";
                }, 1500);
            } else {
                showMessage(data.message, "error");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            showMessage("Error al conectar con el servidor.", "error");
        });
    });
});
