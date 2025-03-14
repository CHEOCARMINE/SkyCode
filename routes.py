from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from functions.auth.register import registrar_alumno as process_registration
from models import db, Materia
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
@academic_bp.route('/materias', methods=['GET'])
@login_required
def listar_materias():
    """
    Muestra todas las materias en una tabla.
    """
    materias = Materia.query.all()
    return render_template('vista_de_materias.html', materias=materias)

@academic_bp.route('/materias/agregar', methods=['GET', 'POST'])
@login_required
def agregar_materia():
    """
    Permite agregar una nueva materia.
    """
    if request.method == 'POST':
        # Recoger datos del formulario
        nombre = request.form.get('nombre')
        crn = request.form.get('crn')
        codigo = request.form.get('codigo')
        creditos = int(request.form.get('creditos'))
        correlativa_id = request.form.get('correlativa_id')  # Puede ser NULL

        # Crear nueva instancia de Materia
        nueva_materia = Materia(
            nombre=nombre,
            crn=crn,
            codigo=codigo,
            creditos=creditos,
            correlativa_id=correlativa_id if correlativa_id else None
        )
        db.session.add(nueva_materia)
        db.session.commit()
        flash('Materia agregada exitosamente.', 'success')
        return redirect(url_for('academic_bp.listar_materias'))

    # Para el formulario, listar materias existentes para seleccionar correlativas
    materias = Materia.query.all()
    return render_template('agregar_materia.html', materias=materias)

@academic_bp.route('/materias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_materia(id):
    """
    Permite editar una materia existente.
    """
    materia = Materia.query.get_or_404(id)

    if request.method == 'POST':
        # Actualizar los datos de la materia
        materia.nombre = request.form.get('nombre')
        materia.crn = request.form.get('crn')
        materia.codigo = request.form.get('codigo')
        materia.creditos = int(request.form.get('creditos'))
        materia.correlativa_id = request.form.get('correlativa_id') if request.form.get('correlativa_id') else None
        db.session.commit()
        flash('Materia actualizada exitosamente.', 'success')
        return redirect(url_for('academic_bp.listar_materias'))

    # Para el formulario, listar materias existentes para seleccionar correlativas
    materias = Materia.query.all()
    return render_template('editar_materia.html', materia=materia, materias=materias)

@academic_bp.route('/materias/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_materia(id):
    """
    Permite eliminar una materia.
    """
    materia = Materia.query.get_or_404(id)
    db.session.delete(materia)
    db.session.commit()
    flash('Materia eliminada exitosamente.', 'success')
    return redirect(url_for('academic_bp.listar_materias'))