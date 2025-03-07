from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from functions.auth.register import registrar_alumno as process_registration
from functions.user_management.view_students import get_students

academic_bp = Blueprint('academic_bp', __name__)

# Ruta para el index del sitio web. Debe estar protegida con login_required para que solo los usuarios autenticados puedan acceder.
@academic_bp.route('/', endpoint='index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('index.html')

# Ruta para el formulario de registro de alumnos. Debe estar protegida con login_required para que solo los usuarios autenticados puedan acceder y los coordinadores.
@academic_bp.route('/register', methods=['GET', 'POST'])
@login_required
def registrar_alumno():
    if current_user.rol_id != 2:
        flash("No tienes permisos para registrar alumnos", "danger")
        return redirect(url_for('academic_bp.index'))
    return process_registration()

# Ruta para la lista de alumnos. Debe estar protegida con login_required para que solo los usuarios autenticados puedan acceder y los coordinadores.
@academic_bp.route('/alumnos', methods=['GET'])
@login_required
def alumnos():
    if current_user.rol_id != 2:
        flash("No tienes permisos para acceder a esta sección.", "danger")
        return redirect(url_for('academic_bp.index'))

    nombre = request.args.get('nombre')
    apellido = request.args.get('apellido')
    segundo_apellido = request.args.get('segundo_apellido')
    matricula = request.args.get('matricula')

    students = get_students(nombre, apellido, segundo_apellido, matricula)
    return render_template('alumnos.html', students=students)