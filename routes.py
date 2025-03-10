from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import current_user, login_required
from math import ceil
from functions.auth.register import registrar_alumno as process_registration
from functions.user_management.view_students import get_students
from models import Carrera, EstadoAlumno, Alumno

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
        flash("No tienes permisos para registrar alumnos", "index-danger")
        return redirect(url_for('academic_bp.index'))
    return process_registration()

@academic_bp.route('/alumnos', methods=['GET'])
@login_required
def alumnos():
    if current_user.rol_id != 2:
        flash("No tienes permisos para acceder a esta sección.", "index-danger")
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

    query = get_students(
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        matricula=matricula,
        carrera=carrera_filtro,
        estado=estado_filtro,
        as_query=True
    )

    total = query.count()
    total_pages = ceil(total / page_size)
    skip = (page - 1) * page_size
    students_page = query.offset(skip).limit(page_size).all()

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

    carreras = Carrera.query.all()
    estados = EstadoAlumno.query.all()

    return render_template(
        'alumnos.html',
        students=students_dict,
        carreras=carreras,
        estados=estados,
        page=page,
        total_pages=total_pages,
        matricula=matricula,
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        carrera_filtro=carrera_filtro,
        estado_filtro=estado_filtro
    )

@academic_bp.route('/modificar_alumno', methods=['GET', 'POST'])
@login_required
def modificar_alumno():
    if current_user.rol_id != 2:
        flash("No tienes permisos para modificar alumnos", "index-danger")
        return redirect(url_for('academic_bp.index'))
    
    from models import EstadoAlumno, Carrera, Alumno

    if request.method == "POST":
        matricula = request.form.get('matricula')
        primer_nombre  = request.form.get('primer_nombre')
        segundo_nombre = request.form.get('segundo_nombre')
        primer_apellido = request.form.get('primer_apellido')
        segundo_apellido = request.form.get('segundo_apellido')
        curp = request.form.get('curp')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo_electronico')
        
        # Datos de domicilio
        pais = request.form.get('pais')
        estado_domicilio = request.form.get('estado_domicilio')
        municipio = request.form.get('municipio')
        colonia = request.form.get('colonia')
        cp = request.form.get('cp')
        calle = request.form.get('calle')
        numero_casa = request.form.get('numero_casa')
        
        nuevo_estado = request.form.get('estado_alumno')
        nueva_carrera = request.form.get('carrera_alumno')
        
        nueva_contrasena = request.form.get('contraseña')
        nuevo_certificado = request.files.get('certificado_preparatoria')
        nuevo_comprobante = request.files.get('comprobante_pago')
        
        try:
            from functions.user_management.update_students_data import actualizar_alumno_y_usuario
            alumno_actualizado = actualizar_alumno_y_usuario(
                matricula,
                primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                curp, telefono, correo,
                pais, estado_domicilio, municipio, colonia, cp, calle, numero_casa,
                nuevo_estado, nueva_carrera,
                nueva_contrasena, nuevo_certificado, nuevo_comprobante
            )
            if alumno_actualizado is None:
                flash("No se pudo actualizar el alumno. Revisa los datos ingresados.", "alumno-danger")
                alumno = Alumno.query.filter_by(matricula=matricula).first()
                estados = EstadoAlumno.query.all()
                carreras = Carrera.query.all()
                return render_template("modificar_alumno.html", alumno=alumno, form_data=request.form, estados=estados, carreras=carreras)
        except Exception as e:
            flash(f"Error al actualizar el alumno: {str(e)}", "alumno-danger")
            alumno = Alumno.query.filter_by(matricula=matricula).first()
            estados = EstadoAlumno.query.all()
            carreras = Carrera.query.all()
            return render_template("modificar_alumno.html", alumno=alumno, form_data=request.form, estados=estados, carreras=carreras)
        
        flash("Datos del alumno actualizados correctamente.", "alumno-success")
        return redirect(url_for('academic_bp.alumnos'))
    
    else:
        matricula = request.args.get('matricula')
        if not matricula:
            flash("No se especificó la matrícula del alumno.", "alumno-danger")
            return redirect(url_for('academic_bp.alumnos'))
        
        alumno = Alumno.query.filter_by(matricula=matricula).first()
        if not alumno:
            flash("Alumno no encontrado.", "alumno-danger")
            return redirect(url_for('academic_bp.alumnos'))
        
        estados = EstadoAlumno.query.all()
        carreras = Carrera.query.all()
        return render_template("modificar_alumno.html", alumno=alumno, estados=estados, carreras=carreras)

@academic_bp.route('/descargar_certificado/<matricula>', methods=['GET'])
@login_required
def descargar_certificado(matricula):
    alumno = Alumno.query.filter_by(matricula=matricula).first()
    if not alumno or not alumno.certificado_preparatoria:
        flash("Certificado no disponible.", "modify-danger")
        return redirect(url_for('academic_bp.modificar_alumno', matricula=matricula))
    from io import BytesIO
    return send_file(
    BytesIO(alumno.certificado_preparatoria),
    download_name="certificado.pdf",
    as_attachment=True
    )


@academic_bp.route('/descargar_comprobante/<matricula>', methods=['GET'])
@login_required
def descargar_comprobante(matricula):
    alumno = Alumno.query.filter_by(matricula=matricula).first()
    if not alumno or not alumno.comprobante_pago:
        flash("Comprobante no disponible.", "modify-danger")
        return redirect(url_for('academic_bp.modificar_alumno', matricula=matricula))
    from io import BytesIO
    return send_file(
    BytesIO(alumno.comprobante_pago),
    download_name="comprobante.pdf",
    as_attachment=True
    )