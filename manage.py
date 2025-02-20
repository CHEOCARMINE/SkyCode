from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from database import get_db_connection  # Importa la conexión a la base de datos
from functions.reports.generate_statistical_report import obtener_estadisticas_generales
import bcrypt
import os
# ✅ Configuración de la aplicación
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave para manejar sesiones

# ==========================
# 📌 RUTA DE LOGIN
# ==========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get("id").strip() if data.get("id") else None
        password = data.get("password")

        # Verificar si el usuario quiere entrar como invitado
        if user_id == "invitado":
            session["usuario_id"] = None
            session["rol"] = "Invitado"
            return jsonify({"success": True, "message": "Inicio de sesión como invitado", "redirect": "/dashboard"})

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Buscar el usuario en la base de datos
        cursor.execute("SELECT * FROM Usuarios WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        db.close()

        if user:
            stored_password = user["contraseña"]
            stored_rol = user["rol"]

            # Comparar la contraseña ingresada con la almacenada en la BD
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                session["usuario_id"] = user["id"]
                session["rol"] = stored_rol
                return jsonify({"success": True, "message": "Inicio de sesión exitoso", "redirect": "/dashboard"})
            else:
                return jsonify({"success": False, "message": "Usuario o contraseña incorrectos"}), 401

        return jsonify({"success": False, "message": "Usuario no encontrado"}), 404

    return render_template('auth/login.html')



# ==========================
# 📌 RUTA PARA EL PROGRESO ACADÉMICO (progress.html)
# ==========================
@app.route('/progress')
def progress():
    print("Accediendo a /progress")  # <-- Depuración

    # Verificar si el usuario ha iniciado sesión
    usuario_autenticado = "usuario_id" in session

    if usuario_autenticado:
        alumno_id = session["usuario_id"]
        username = session.get("username", "Invitado")
        rol = session.get("rol", "Desconocido")
        print(f"Usuario autenticado: {alumno_id}")  # <-- Depuración

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT m.nombre AS materia, c.calificacion, c.cuatrimestre
            FROM Calificaciones c
            JOIN Materias m ON c.materia_id = m.id
            WHERE c.alumno_id = %s
            ORDER BY c.cuatrimestre ASC
        """, (alumno_id,))
        calificaciones = cursor.fetchall()

        print(f"Calificaciones obtenidas: {calificaciones}")  # <-- Depuración

        aprobadas = sum(1 for c in calificaciones if c["calificacion"] >= 7)
        reprobadas = sum(1 for c in calificaciones if c["calificacion"] < 7)
        total_materias = 50  # Ajusta este valor según tu base de datos
        avance = round((aprobadas / total_materias) * 100, 2) if total_materias > 0 else 0

        db.close()

    else:
        # Si no está autenticado, mostrar valores por defecto para un invitado
        username = "Invitado"
        rol = "Desconocido"
        calificaciones = []
        aprobadas = 0
        reprobadas = 0
        avance = 0
        print("Usuario no autenticado, mostrando datos como invitado")  # <-- Depuración

    print(f"Mostrando progress.html con avance: {avance}%")  # <-- Depuración
    return render_template("progress.html", 
                           username=username, 
                           rol=rol, 
                           calificaciones=calificaciones, 
                           aprobadas=aprobadas, 
                           reprobadas=reprobadas, 
                           avance=avance)

@app.route('/reports')
def reports():
    from functions.reports.generate_statistical_report import generate_statistical_report  # Importamos dentro de la función para evitar importaciones circulares

    # Obtener datos desde la función de reportes
    estadisticas = generate_statistical_report()

    return render_template("reports.html", 
                           total_inscritos=estadisticas.get("total_inscritos", 0),
                           total_egresados=estadisticas.get("total_egresados", 0),
                           promedio_global=estadisticas.get("promedio_global", 0.0),
                           promedios_carreras=estadisticas.get("promedios_carreras", []))



# ==========================
# 📌 RUTA PARA EL DASHBOARD
# ==========================
@app.route('/dashboard')
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", 
                           username=session.get("username", "Invitado"), 
                           rol=session.get("rol", "Desconocido"))

# ==========================
# 📌 CERRAR SESIÓN
# ==========================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ✅ Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=5030)
