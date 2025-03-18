from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, abort
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from math import ceil
from functions.auth.register import registrar_alumno as process_registration
from models import db, Materia
from functions.user_management.view_students import get_students
from models import Carrera, EstadoAlumno, Alumno
from functions.academic_progress import get_academic_progress
from services import send_email 
from functions.user_management.update_students_data import actualizar_alumno_y_usuario
from functions.reports.generate_statistical_report import generate_statistical_report
from functions.reports.export_report import generar_pdf_reporte

academic_bp = Blueprint('academic_bp', __name__)
alumno_progress_bp = Blueprint('alumno_progress', __name__)

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

    if request.method == "POST":
        # Recoger datos del formulario
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
        
        # Estado y Carrera
        nuevo_estado = request.form.get('estado_alumno')
        nueva_carrera = request.form.get('carrera_alumno')
        
        # Contraseña y Docuemntos
        nueva_contrasena = request.form.get('contraseña')
        nuevo_certificado = request.files.get('certificado_preparatoria')
        nuevo_comprobante = request.files.get('comprobante_pago')
        
        try:
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
        
        # Construir el mensaje de correo con todos los datos modificados.
        subject = "Actualización de tus datos en SkyCode"
        body = f"Hola {alumno_actualizado.primer_nombre},\n\n"
        body += "Se han actualizado los siguientes datos en tu cuenta:\n\n"
        # Datos personales
        body += "Datos Personales:\n"
        body += f"  Nombre: {alumno_actualizado.primer_nombre} {alumno_actualizado.segundo_nombre or ''}\n"
        body += f"  Apellidos: {alumno_actualizado.primer_apellido} {alumno_actualizado.segundo_apellido}\n"
        body += f"  CURP: {alumno_actualizado.curp}\n"
        body += f"  Teléfono: {alumno_actualizado.telefono}\n"
        body += f"  Correo Electrónico: {alumno_actualizado.correo_electronico}\n\n"
        
        # Datos de domicilio
        if alumno_actualizado.domicilio:
            body += "Datos de Domicilio:\n"
            body += f"  País: {alumno_actualizado.domicilio.pais}\n"
            body += f"  Estado: {alumno_actualizado.domicilio.estado}\n"
            body += f"  Municipio: {alumno_actualizado.domicilio.municipio}\n"
            body += f"  Colonia: {alumno_actualizado.domicilio.colonia}\n"
            body += f"  Código Postal: {alumno_actualizado.domicilio.cp}\n"
            body += f"  Calle: {alumno_actualizado.domicilio.calle}\n"
            body += f"  Número de Casa: {alumno_actualizado.domicilio.numero_casa}\n\n"
        else:
            body += "No se actualizaron datos de domicilio.\n\n"
        
        # Estado y Carrera
        body += f"Estado del Alumno: {alumno_actualizado.estado.nombre_estado if alumno_actualizado.estado else 'N/A'}\n"
        body += f"Carrera: {alumno_actualizado.carrera.nombre if alumno_actualizado.carrera else 'N/A'}\n\n"
        
        # Incluir la nueva contraseña si se proporcionó
        if nueva_contrasena:
            body += f"Tu nueva contraseña es: {nueva_contrasena}\n\n"
        
        body += "Si tienes alguna duda o necesitas asistencia, por favor contáctanos.\n\n"
        body += "Saludos,\nEquipo SkyCode"

        # Enviar correo al alumno
        send_email(subject, [alumno_actualizado.correo_electronico], body)
        
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

@alumno_progress_bp.route('/progress')
@login_required
def mostrar_historial_academico():
    if current_user.rol_id != 1:  # Solo los alumnos pueden ver su progreso
        flash("No tienes permisos para ver esta sección.", "danger")
        return redirect(url_for('academic_bp.index'))

    progress_data = get_academic_progress(current_user.alumno_id)

    return render_template(
        'progress.html',
        avance=progress_data["avance"],
        historial=progress_data["historial"],
        pending_courses=progress_data["pending_courses"]
    )

reports_bp = Blueprint('reports_bp', __name__)

@reports_bp.route('/reports')
@login_required
def mostrar_reportes():
    if current_user.rol_id != 3:  # Solo los directivos pueden acceder
        flash("No tienes permisos para acceder a esta sección.", "danger")
        return redirect(url_for('academic_bp.index'))

    report_data = generate_statistical_report()  # Obtener datos reales del reporte

    return render_template('reports.html', report_data=report_data)


@reports_bp.route('/reports/download_pdf')
@login_required
def download_report_pdf():
    try:
        datos_reporte = generate_statistical_report()  # Obtiene los datos

        if not datos_reporte:
            flash("No hay datos para generar el reporte.", "danger")
            return redirect(url_for('reports_bp.mostrar_reportes'))

        pdf_path = generar_pdf_reporte(datos_reporte)  # <-- Ahora sí pasamos los datos

        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        flash(f"Error al generar el PDF: {str(e)}", "danger")
        return redirect(url_for('reports_bp.mostrar_reportes'))