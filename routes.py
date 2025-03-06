from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from functions.auth.register import registrar_alumno as process_registration

academic_bp = Blueprint('academic_bp', __name__)

@academic_bp.route('/', endpoint='index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('index.html')

@academic_bp.route('/register', methods=['GET', 'POST'])
@login_required
def registrar_alumno():
    # Suponiendo que en tu base de datos:
    # 1 = Alumno, 2 = Coordinador, 3 = Directivo
    if current_user.rol_id != 2:
        flash("No tienes permisos para registrar alumnos", "danger")
        return redirect(url_for('academic_bp.index'))
    return process_registration()

    from flask import Blueprint, render_template, make_response
from weasyprint import HTML
import mysql.connector

# Blueprint para las rutas académicas
academic_bp = Blueprint('academic_bp', __name__)

@academic_bp.route('/imprimir_horario/<int:alumno_id>')
def imprimir_horario(alumno_id):
    # Conectar a la base de datos y obtener los datos del horario
    conn = mysql.connector.connect(
        host="tu_host",
        user="tu_usuario",
        password="tu_contraseña",
        database="tu_base_de_datos"
    )
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            materias.nombre AS nombre_materia, 
            horarios.horario, 
            horarios.salon, 
            docentes.nombre AS nombre_docente 
        FROM horarios 
        JOIN materias ON horarios.materia_id = materias.id 
        JOIN docentes ON horarios.docente_id = docentes.id 
        WHERE horarios.alumno_id = %s
    """
    cursor.execute(query, (alumno_id,))
    clases = cursor.fetchall()
    conn.close()

    # Renderizar la plantilla HTML con los datos
    html = render_template('horario.html', clases=clases)

    # Convertir el HTML a PDF
    pdf = HTML(string=html).write_pdf()

    # Crear la respuesta del PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=horario.pdf'
    return response

# Registro del blueprint en el archivo principal (app.py)
# app.register_blueprint(academic_bp)
