from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from math import ceil
from functions.auth.register import registrar_alumno as process_registration
from functions.user_management.view_students import get_students
from models import Carrera, EstadoAlumno

academic_bp = Blueprint('academic_bp', __name__)

@academic_bp.route('/', endpoint='index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('index.html')

@academic_bp.route('/register', methods=['GET', 'POST'])
@login_required
def registrar_alumno():
    if current_user.rol_id != 2:
        flash("No tienes permisos para registrar alumnos", "danger")
        return redirect(url_for('academic_bp.index'))
    return process_registration()

@academic_bp.route('/alumnos', methods=['GET'])
@login_required
def alumnos():
    if current_user.rol_id != 2:
        flash("No tienes permisos para acceder a esta sección.", "danger")
        return redirect(url_for('academic_bp.index'))

    # Parámetros de paginación
    page = request.args.get('page', 1, type=int)
    page_size = 10

    # Filtros
    nombre = request.args.get('nombre')
    apellido_paterno = request.args.get('apellido_paterno')
    apellido_materno = request.args.get('apellido_materno')
    matricula = request.args.get('matricula')
    carrera_filtro = request.args.get('carrera')
    estado_filtro = request.args.get('estado')

    # Se obtiene la Query en lugar de resultados
    query = get_students(
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        matricula=matricula,
        carrera=carrera_filtro,
        estado=estado_filtro,
        as_query=True
    )

    # Contamos el total de registros filtrados
    total = query.count()
    # Calculamos cuántas páginas habrá en total
    total_pages = ceil(total / page_size)

    # Calculamos cuántos registros saltar (offset)
    skip = (page - 1) * page_size

    # Obtenemos solo los registros de la página actual (objetos Alumno)
    students_page = query.offset(skip).limit(page_size).all()

    # Convertimos cada objeto alumno a un diccionario, forzando la conversión a string
    students_dict = []
    for alumno in students_page:
        student_data = {
            "matricula": alumno.matricula,
            "primer_nombre": alumno.primer_nombre,
            "primer_apellido": alumno.primer_apellido,
            "segundo_apellido": alumno.segundo_apellido,
            "carrera": str(alumno.carrera.nombre) if alumno.carrera else "",
            "estado": str(alumno.estado.nombre_estado) if alumno.estado else ""
        }
        students_dict.append(student_data)

    # Se obtienen las opciones para los select de Carrera y EstadoAlumno
    carreras = Carrera.query.all()
    estados = EstadoAlumno.query.all()

    return render_template(
        'alumnos.html',
        students=students_dict,
        carreras=carreras,
        estados=estados,
        page=page,
        total_pages=total_pages,
        # Reenviamos los filtros para que no se pierdan
        matricula=matricula,
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        carrera_filtro=carrera_filtro,
        estado_filtro=estado_filtro
    )