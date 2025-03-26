from flask import request, redirect, url_for, flash, render_template
import secrets
from functions.auth.validations import (
    generar_matricula,
    validate_curp,
    validate_telefono,
    validate_correo,
    validate_file,
    validate_letters,      
    validate_postal_code,  
    validate_alphanumeric   
)
from database import (
    bcrypt,
    insertar_alumno, 
    crear_usuario_para_alumno, 
    existe_alumno_por_curp,
    insertar_domicilio
)
from services import send_email

def registrar_alumno():
    if request.method == "POST":
        # Recoger datos personales
        nombre = request.form.get('nombre')  # Cambio: antes era primer_nombre
        primer_apellido = request.form.get('primer_apellido')
        segundo_apellido = request.form.get('segundo_apellido')
        curp = request.form.get('curp')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo_electronico')
        carrera_id = request.form.get('carrera_id')

        # Recoger datos de domicilio desde el formulario
        estado = request.form.get('estado')
        municipio = request.form.get('municipio')
        colonia = request.form.get('colonia')
        cp = request.form.get('cp')
        calle = request.form.get('calle')
        numero_casa = request.form.get('numero_casa')

        # Validaciones básicas de formato
        if not validate_curp(curp):
            flash("El CURP no cumple con el formato requerido.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        if not validate_telefono(telefono):
            flash("El teléfono debe contener exactamente 10 dígitos.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        if not validate_correo(correo):
            flash("El correo no es válido o no pertenece a un dominio permitido.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))

        # Validar que los campos de nombres y apellidos contengan solo letras
        if not validate_letters(nombre):  # Cambio: antes era primer_nombre
            flash("El nombre debe contener solo letras y espacios.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        if not validate_letters(primer_apellido):
            flash("El primer apellido debe contener solo letras y espacios.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        if not validate_letters(segundo_apellido):
            flash("El segundo apellido debe contener solo letras y espacios.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        
        # Validar campos de domicilio: estado, municipio y colonia solo deben contener letras y espacios
        if not validate_letters(estado):
            flash("El estado debe contener solo letras y espacios.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        if not validate_letters(municipio):
            flash("El municipio debe contener solo letras y espacios.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        if not validate_letters(colonia):
            flash("La colonia debe contener solo letras y espacios.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        # Validar el código postal: solo números y exactamente 5 dígitos
        if not validate_postal_code(cp):
            flash("El código postal debe contener exactamente 5 dígitos numéricos.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        # Validar el número de casa: debe ser alfanumérico (se permiten espacios y guiones)
        if not validate_alphanumeric(numero_casa):
            flash("El número de casa debe contener solo caracteres alfanuméricos, espacios y guiones.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))

        # Verificar duplicidad del CURP
        if existe_alumno_por_curp(curp):
            flash("El CURP ya está registrado en el sistema.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))

        # Validar y procesar los archivos
        certificado_file = request.files.get('certificado_preparatoria')
        comprobante_file = request.files.get('comprobante_pago')
        
        if certificado_file:
            valid, mensaje = validate_file(certificado_file)
            if not valid:
                flash(f"Certificado: {mensaje}", "register-danger")
                return redirect(url_for('academic_bp.registrar_alumno'))
            certificado_data = certificado_file.read()
        else:
            certificado_data = None

        if comprobante_file:
            valid, mensaje = validate_file(comprobante_file)
            if not valid:
                flash(f"Comprobante: {mensaje}", "register-danger")
                return redirect(url_for('academic_bp.registrar_alumno'))
            comprobante_data = comprobante_file.read()
        else:
            comprobante_data = None

        # Generar la matrícula automáticamente
        matricula = generar_matricula()

        # Insertar el domicilio en la base de datos (usa "México" como país fijo)
        nuevo_domicilio = insertar_domicilio(
            estado=estado,
            municipio=municipio,
            colonia=colonia,
            cp=cp,
            calle=calle,
            numero_casa=numero_casa,
            pais="México"
        )
        domicilio_id = nuevo_domicilio.id

        # Inserción del alumno usando el ID del domicilio
        nuevo_alumno = insertar_alumno(
            matricula,
            nombre,  # Cambio: antes era primer_nombre
            primer_apellido,
            segundo_apellido,
            curp,
            domicilio_id,  # Se pasa el ID del domicilio insertado
            telefono,
            correo,
            certificado_data,
            comprobante_data,
            estado_id=1,      # Se asume que 1 es 'Activo'
            carrera_id=carrera_id
        )

        # Crear el usuario asociado con una contraseña temporal usando Flask-Bcrypt
        temp_password = secrets.token_urlsafe(8)
        hashed_password = bcrypt.generate_password_hash(temp_password).decode('utf-8')
        try:
            crear_usuario_para_alumno(nuevo_alumno.id, hashed_password, rol_id=1)  # Se asume que 1 es 'Alumno'
        except Exception as e:
            # Si ocurre un error al crear el usuario, se registra el error y se muestra un mensaje
            flash("Hubo un problema al crear el usuario asociado. Por favor, inténtalo nuevamente.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))

        # Preparar y enviar el correo con las credenciales temporales
        subject = "Bienvenido a SkyCode - Contraseña Temporal"
        recipients = [correo]
        body = (
            f"Hola {nombre} {primer_apellido},\n\n"  # Cambio: antes era primer_nombre
            f"Tu usuario es tu matrícula: {matricula}\n"
            f"Tu contraseña temporal es: {temp_password}\n\n"
            "Por favor, cambia tu contraseña al ingresar al sistema.\n\n"
            "Saludos,\nEquipo SkyCode"
        )
        send_email(subject, recipients, body)

        flash("Alumno registrado exitosamente. Se ha enviado un correo con la contraseña temporal.", "register-success")
        return redirect(url_for('academic_bp.registrar_alumno'))
    else:
        from models import Carrera
        carreras = Carrera.query.all()
        return render_template('register.html', carreras=carreras)
