from flask import request, redirect, url_for, flash, render_template
import secrets
from functions.pdf.generar_pdf_bienvenida import generar_pdf_bienvenida
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
from models import Carrera  # ✅ Importar aquí

def registrar_alumno():
    if request.method == "POST":
        nombre = request.form.get('nombre')
        primer_apellido = request.form.get('primer_apellido')
        segundo_apellido = request.form.get('segundo_apellido')
        curp = request.form.get('curp')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo_electronico')
        carrera_id = request.form.get('carrera_id')

        estado = request.form.get('estado')
        municipio = request.form.get('municipio')
        colonia = request.form.get('colonia')
        cp = request.form.get('cp')
        calle = request.form.get('calle')
        numero_casa = request.form.get('numero_casa')

        if not validate_curp(curp):
            flash("El CURP no cumple con el formato requerido.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        if not validate_telefono(telefono):
            flash("El teléfono debe contener exactamente 10 dígitos.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        if not validate_correo(correo):
            flash("El correo no es válido.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))

        if not validate_letters(nombre):
            flash("El nombre debe contener solo letras.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        if not validate_letters(primer_apellido):
            flash("El primer apellido debe contener solo letras.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        if not validate_letters(segundo_apellido):
            flash("El segundo apellido debe contener solo letras.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        if not validate_letters(estado) or not validate_letters(municipio) or not validate_letters(colonia):
            flash("Los campos de domicilio deben contener solo letras.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        if not validate_postal_code(cp):
            flash("El código postal debe contener exactamente 5 dígitos.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))
        if not validate_alphanumeric(numero_casa):
            flash("El número de casa debe ser alfanumérico.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))

        if existe_alumno_por_curp(curp):
            flash("El CURP ya está registrado.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))

        certificado_file = request.files.get('certificado_preparatoria')
        comprobante_file = request.files.get('comprobante_pago')

        certificado_data = certificado_file.read() if certificado_file and validate_file(certificado_file)[0] else None
        comprobante_data = comprobante_file.read() if comprobante_file and validate_file(comprobante_file)[0] else None

        matricula = generar_matricula()

        nuevo_domicilio = insertar_domicilio(
            estado=estado,
            municipio=municipio,
            colonia=colonia,
            cp=cp,
            calle=calle,
            numero_casa=numero_casa,
            pais="México"
        )

        nuevo_alumno = insertar_alumno(
            matricula,
            nombre,
            primer_apellido,
            segundo_apellido,
            curp,
            nuevo_domicilio.id,
            telefono,
            correo,
            certificado_data,
            comprobante_data,
            estado_id=1,
            carrera_id=carrera_id
        )

        temp_password = secrets.token_urlsafe(8)
        hashed_password = bcrypt.generate_password_hash(temp_password).decode('utf-8')

        try:
            crear_usuario_para_alumno(nuevo_alumno.id, hashed_password, rol_id=1)
        except Exception as e:
            flash("Error al crear el usuario del alumno.", "register-danger")
            return redirect(url_for('academic_bp.registrar_alumno'))

        # ✅ Obtener nombre de la carrera
        carrera = Carrera.query.get(carrera_id)
        carrera_nombre = carrera.nombre if carrera else "Sin definir"

        # 📄 Generar PDF de bienvenida
        pdf_path = generar_pdf_bienvenida(nombre, primer_apellido, matricula, carrera_nombre)

        # 📧 Preparar correo
        subject = "Bienvenido a SkyCode - Credenciales de Acceso"
        recipients = [correo]
        body = (
            f"Hola {nombre} {primer_apellido},\n\n"
            f"Tu usuario es tu matrícula: {matricula}\n"
            f"Tu contraseña temporal es: {temp_password}\n\n"
            "Revisa el PDF adjunto con más detalles.\n"
            "Por favor, cambia tu contraseña después del primer inicio de sesión.\n\n"
            "Saludos,\nEquipo SkyCode"
        )

        # 📎 Enviar con adjunto
        send_email(subject, recipients, body, attachments=[pdf_path])

        flash("Alumno registrado exitosamente. Se envió un correo con la contraseña y PDF de bienvenida.", "register-success")
        return redirect(url_for('academic_bp.registrar_alumno'))

    else:
        carreras = Carrera.query.all()
        return render_template('register.html', carreras=carreras)
