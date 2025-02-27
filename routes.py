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
