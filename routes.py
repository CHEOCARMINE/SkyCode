from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, abort
from flask_login import current_user, login_required
from math import ceil
from functions.auth.register import registrar_alumno as process_registration
from functions.user_management.view_students import get_students
from models import db, Carrera, EstadoAlumno, Alumno, Materia, Coordinadores_Directivos,Cuatrimestre
from functions.academic_progress import get_academic_progress
from services import send_email 
from functions.user_management.update_students_data import actualizar_alumno_y_usuario
from functions.auth.register_user import registrar_coordinador_directivo
from functions.user_management.view_user import get_coordinadores_directivos
from functions.user_management.update_user_data import actualizar_coordinador_directivo
from database import bcrypt, db
from functions.reports.generate_statistical_report import generate_statistical_report
from functions.reports.export_report import generar_pdf_reporte

academic_bp = Blueprint('academic_bp', __name__)
alumno_progress_bp = Blueprint('alumno_progress', __name__)
reports_bp = Blueprint('reports_bp', __name__)

# ------------------------------------------------------------
# Route del Index
# ------------------------------------------------------------

@academic_bp.route('/', endpoint='index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('index.html')

# ------------------------------------------------------------
# Route para el registro de alumnos
# ------------------------------------------------------------

@academic_bp.route('/register', methods=['GET', 'POST'])
@login_required
def registrar_alumno():
    if current_user.rol_id != 2:
        flash("No tienes permisos para registrar alumnos", "index-danger")
        return redirect(url_for('academic_bp.index'))
    return process_registration()

# ------------------------------------------------------------
# Route para Materias
# ------------------------------------------------------------

@academic_bp.route('/materias', methods=['GET'])
@login_required
def listar_materias():
    """
    Muestra todas las materias en una tabla.
    """
    materias = Materia.query.all()
    return render_template('vista_de_materias.html', materias=materias)

# ------------------------------------------------------------
# Route para agregar Materias
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# Route para editar Materia
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# Route para eliminar Materia
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# Route para ver alumnos
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# Route para modificar alumnos
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# Route para descargar Certificado
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# Route para descargar Comprobante
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# Route para ver Progreso de Alumno
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# Route para el registro de Coordinadores/Directivos
# ------------------------------------------------------------

@academic_bp.route('/register_user', methods=['GET', 'POST'])
@login_required
def register_user_route():
    if current_user.rol_id != 3:
        flash("No tienes permisos para registrar coordinadores/directivos", "index-danger")
        return redirect(url_for('auth.index'))
    return registrar_coordinador_directivo()

# ------------------------------------------------------------
# Route para Ver Coordinadores y Directivos
# ------------------------------------------------------------

@academic_bp.route('/coordinadores_directivos', methods=['GET'])
@login_required
def coordinadores_directivos():
    if current_user.rol_id != 3:
        flash("No tienes permisos para acceder a esta sección.", "index-danger")
        return redirect(url_for('academic_bp.index'))
    
    # Parámetros de paginación
    page = request.args.get('page', 1, type=int)
    page_size = 10

    # Filtros
    nombre = request.args.get('nombre')
    apellido = request.args.get('apellido')
    matricula = request.args.get('matricula')
    estado_filtro = request.args.get('estado')  # '1' o '0'
    rol_filter = request.args.get('rol', type=int)  # Valor numérico (2: Coordinador, 3: Directivo)

    # Obtiene la query filtrada
    query = get_coordinadores_directivos(
        nombre=nombre,
        apellido=apellido,
        matricula=matricula,
        rol=rol_filter,
        estado=estado_filtro,
        as_query=True
    )
    
    total = query.count()
    total_pages = ceil(total / page_size)
    skip = (page - 1) * page_size
    registros_page = query.offset(skip).limit(page_size).all()
    
    users_dict = []
    for registro in registros_page:
        data = {
            "id": registro.id,
            "matricula": registro.matricula,
            "primer_nombre": registro.primer_nombre,
            "primer_apellido": registro.primer_apellido,
            "estado": "Activo" if registro.usuario and registro.usuario.activo else "Inactivo",
            "rol": "Coordinador" if registro.usuario and registro.usuario.rol_id == 2 
                   else ("Directivo" if registro.usuario and registro.usuario.rol_id == 3 else "Sin definir")
        }
        users_dict.append(data)
    
    return render_template(
        'user.html',
        users=users_dict,
        page=page,
        total_pages=total_pages,
        matricula=matricula,
        nombre=nombre,
        apellido=apellido,
        estado_filtro=estado_filtro,
        rol_filter=rol_filter
    )

# ------------------------------------------------------------
# Route para Modificar Coordinadores y Directivos
# ------------------------------------------------------------

@academic_bp.route('/modificar_coordinador_directivo', methods=['GET', 'POST'])
@login_required
def modificar_coordinador_directivo():
    if current_user.rol_id != 3:
        flash("No tienes permisos para modificar coordinadores/directivos", "coordinador-danger")
        return redirect(url_for('academic_bp.index'))
    
    if request.method == "POST":
        # Recoger datos del formulario
        user_id = request.form.get('user_id')
        primer_nombre = request.form.get('primer_nombre')
        primer_apellido = request.form.get('primer_apellido')
        correo = request.form.get('correo_electronico')
        estado_cuenta = request.form.get('estado_cuenta')  
        nueva_contrasena = request.form.get('contraseña')   
        
        try:
            coordinador_actualizado = actualizar_coordinador_directivo(
                user_id,
                primer_nombre,
                primer_apellido,
                correo,
                "Activo" if estado_cuenta == "1" else "Inactivo"
            )
            if not coordinador_actualizado:
                flash("No se pudo actualizar el Coordinador/Directivo. Revisa los datos ingresados.", "coordinador-danger")
                return redirect(url_for('academic_bp.modificar_coordinador_directivo', user_id=user_id))
        except Exception as e:
            flash(f"Error al actualizar el Coordinador/Directivo: {str(e)}", "coordinador-danger")
            return redirect(url_for('academic_bp.modificar_coordinador_directivo', user_id=user_id))
        
        # Actualizar la contraseña si se proporciona
        if nueva_contrasena:
            usuario = coordinador_actualizado.usuario
            if usuario:
                hashed = bcrypt.generate_password_hash(nueva_contrasena).decode('utf-8')
                usuario.contraseña = hashed

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Error al guardar los cambios en la base de datos.", "coordinador-danger")
            return redirect(url_for('academic_bp.modificar_coordinador_directivo', user_id=user_id))
        
        # Construir el mensaje de correo con los datos modificados
        subject = "Actualización de tus datos en SkyCode"
        body = f"Hola {coordinador_actualizado.primer_nombre} {coordinador_actualizado.primer_apellido},\n\n"
        body += "Se han actualizado los siguientes datos en tu cuenta:\n\n"
        body += f"  Nombre: {coordinador_actualizado.primer_nombre}\n"
        body += f"  Apellido: {coordinador_actualizado.primer_apellido}\n"
        body += f"  Correo Electrónico: {coordinador_actualizado.correo_electronico}\n"
        body += f"  Estado de la Cuenta: {'Activo' if coordinador_actualizado.usuario and coordinador_actualizado.usuario.activo else 'Inactivo'}\n"
        if nueva_contrasena:
            body += f"\nTu nueva contraseña es: {nueva_contrasena}\n"
        body += "\nSi tienes alguna duda o necesitas asistencia, por favor contáctanos.\n\n"
        body += "Saludos,\nEquipo SkyCode"
        send_email(subject, [correo], body)
        
        flash("Datos del Coordinador/Directivo actualizados correctamente.", "coordinador-success")
        return redirect(url_for('academic_bp.coordinadores_directivos'))
    
    else:
        user_id = request.args.get('user_id')
        if not user_id:
            flash("No se especificó el ID del Coordinador/Directivo.", "coordinador-danger")
            return redirect(url_for('academic_bp.coordinadores_directivos'))
        
        registro = Coordinadores_Directivos.query.get(user_id)
        if not registro:
            flash("Coordinador/Directivo no encontrado.", "coordinador-danger")
            return redirect(url_for('academic_bp.coordinadores_directivos'))
        
        return render_template("modificar_user.html", registro=registro)

# ------------------------------------------------------------
# Route de Reporte Estadistico
# ------------------------------------------------------------

@reports_bp.route('/reports')
@login_required
def mostrar_reportes():
    if current_user.rol_id != 3:  # Solo los directivos pueden acceder
        flash("No tienes permisos para acceder a esta sección.", "danger")
        return redirect(url_for('academic_bp.index'))

    report_data = generate_statistical_report()  # Obtener datos reales del reporte

    return render_template('reports.html', report_data=report_data)


# ------------------------------------------------------------
# Route para descargar el reporte en PDF
# ------------------------------------------------------------

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

@academic_bp.route('/materias/pendientes/<int:alumno_id>', methods=['GET'])
@login_required
def materias_pendientes(alumno_id):
    """
    Muestra las materias pendientes por cursar y sugeridas para el siguiente cuatrimestre.
    """
    # Consultar materias pendientes
    materias_pendientes = db.session.execute("""
        SELECT m.id, m.nombre
        FROM Materias m
        LEFT JOIN Calificaciones c
            ON m.id = c.materia_id AND c.alumno_id = :alumno_id
        WHERE c.calificacion IS NULL OR c.calificacion < 70
    """, {"alumno_id": alumno_id}).fetchall()

    # Consultar materias sugeridas (siguiendo correlativas)
    materias_sugeridas = db.session.execute("""
        SELECT m.id, m.nombre
        FROM Materias m
        LEFT JOIN Calificaciones c
            ON m.id = c.materia_id AND c.alumno_id = :alumno_id
        WHERE (c.calificacion IS NULL OR c.calificacion < 70)
          AND (m.correlativa_id IS NULL 
            OR m.correlativa_id IN (
                SELECT materia_id
                FROM Calificaciones
                WHERE calificacion >= 70 AND alumno_id = :alumno_id
            ))
    """, {"alumno_id": alumno_id}).fetchall()

    return render_template(
        'materias_pendientes.html',
        pendientes=materias_pendientes,
        sugeridas=materias_sugeridas
    )
# ------------------------------------------------------------
# Route para Cuatrimestres 
# ------------------------------------------------------------
@academic_bp.route('/cuatrimestres', methods=['GET'])
@login_required
def listar_cuatrimestres():
    """
    Lista todos los cuatrimestres existentes.
    """
    cuatrimestres = Cuatrimestre.query.all()  # Consulta todos los registros en la tabla Cuatrimestres
    return render_template('listar_cuatrimestres.html', cuatrimestres=cuatrimestres)
@academic_bp.route('/cuatrimestres/agregar', methods=['GET', 'POST'])


@login_required
def agregar_cuatrimestre():
    """
    Permite agregar un nuevo cuatrimestre.
    """
    if request.method == 'POST':
        nocuatrimestre = request.form.get('nocuatrimestre')
        descripcion = request.form.get('descripcion')

        # Crear un nuevo objeto Cuatrimestre y guardarlo en la base de datos
        nuevo_cuatrimestre = Cuatrimestre(nocuatrimestre=nocuatrimestre, descripcion=descripcion)
        db.session.add(nuevo_cuatrimestre)
        db.session.commit()

        flash('Cuatrimestre agregado exitosamente.', 'success')
        return redirect(url_for('academic_bp.listar_cuatrimestres'))
    
    return render_template('agregar_cuatrimestre.html')

@academic_bp.route('/cuatrimestres/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cuatrimestre(id):
    """
    Permite editar un cuatrimestre existente.
    """
    cuatrimestre = Cuatrimestre.query.get_or_404(id)  # Obtiene el registro o lanza un error 404

    if request.method == 'POST':
        # Actualizar los campos
        cuatrimestre.nocuatrimestre = request.form.get('nocuatrimestre')
        cuatrimestre.descripcion = request.form.get('descripcion')
        db.session.commit()

        flash('Cuatrimestre actualizado exitosamente.', 'success')
        return redirect(url_for('academic_bp.listar_cuatrimestres'))
    
    return render_template('editar_cuatrimestre.html', cuatrimestre=cuatrimestre)

@academic_bp.route('/cuatrimestres/eliminar/<int:id>', methods=['POST'])

@login_required
def eliminar_cuatrimestre(id):
    """
    Permite eliminar un cuatrimestre específico.
    """
    cuatrimestre = Cuatrimestre.query.get_or_404(id)  # Obtiene el registro o lanza un error 404

    db.session.delete(cuatrimestre)  # Elimina el registro de la base de datos
    db.session.commit()

    flash('Cuatrimestre eliminado exitosamente.', 'success')
    return redirect(url_for('academic_bp.listar_cuatrimestres'))

