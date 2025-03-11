from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from functions.auth.register import registrar_alumno as process_registration
from functions.academic_progress import get_academic_progress


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

alumno_progress_bp: Blueprint = Blueprint('alumno_progress', __name__)

@alumno_progress_bp.route('/academic_progress')
@login_required
def academic_progress_view():
    if current_user.rol_id != 1:
        abort(403)
    
    progress_data = get_academic_progress(current_user.id)
    return render_template('progress.html',
                           avance=progress_data.get("avance", 0),
                           historial=progress_data.get("historial", []),
                           grades=progress_data.get("grades", []),
                           pending_courses=progress_data.get("pending_courses", []))