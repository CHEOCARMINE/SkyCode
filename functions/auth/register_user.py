from flask import request, redirect, url_for, flash, render_template
import secrets
from functions.auth.validations import (
    validate_letters,
    validate_correo,
    generar_matricula_coordinador_directivo  
)
from database import (
    bcrypt,
    insertar_coordinador_directivo, 
    crear_usuario_para_coordinador_directivo
)
from services import send_email

def registrar_coordinador_directivo():
    if request.method == "POST":
        # Recoger datos del formulario
        primer_nombre   = request.form.get('primer_nombre')
        primer_apellido = request.form.get('primer_apellido')
        correo          = request.form.get('correo_electronico')
        tipo_usuario    = request.form.get('tipo_usuario')  # "COO" o "DIR"

        # Validaciones básicas
        if not validate_letters(primer_nombre):
            flash("El primer nombre debe contener solo letras y espacios.", "register_COO_DIR-danger")
            return redirect(url_for('academic_bp.register_user_route'))
        if not validate_letters(primer_apellido):
            flash("El primer apellido debe contener solo letras y espacios.", "register_COO_DIR-danger")
            return redirect(url_for('academic_bp.register_user_route'))
        if not validate_correo(correo):
            flash("El correo no es válido o no pertenece a un dominio permitido.", "register_COO_DIR-danger")
            return redirect(url_for('academic_bp.register_user_route'))
        if tipo_usuario not in ['COO', 'DIR']:
            flash("El tipo de usuario no es válido.", "register_COO_DIR-danger")
            return redirect(url_for('academic_bp.register_user_route'))

        # Generar la matrícula para Coordinador/Directivo
        matricula = generar_matricula_coordinador_directivo(tipo_usuario)

        # Insertar el registro en la tabla Coordinadores_Directivos
        nuevo_registro = insertar_coordinador_directivo(
            matricula,
            primer_nombre,
            primer_apellido,
            correo
        )

        # Crear el usuario asociado con una contraseña temporal
        temp_password   = secrets.token_urlsafe(8)
        hashed_password = bcrypt.generate_password_hash(temp_password).decode('utf-8')

        # Asignar rol según el tipo de usuario (por ejemplo, rol_id 2 para coordinadores y 3 para directivos)
        rol_id = 2 if tipo_usuario == 'COO' else 3

        try:
            crear_usuario_para_coordinador_directivo(nuevo_registro.id, hashed_password, rol_id)
        except Exception as e:
            flash("Hubo un problema al crear el usuario asociado. Por favor, inténtalo nuevamente.", "register_COO_DIR-danger")
            return redirect(url_for('academic_bp.register_user_route'))

        # Preparar y enviar el correo con las credenciales temporales
        subject    = "Bienvenido a SkyCode - Contraseña Temporal"
        recipients = [correo]
        body = (
            f"Hola {primer_nombre} {primer_apellido},\n\n"
            f"Tu usuario es tu matrícula: {matricula}\n"
            f"Tu contraseña temporal es: {temp_password}\n\n"
            "Por favor, cambia tu contraseña al ingresar al sistema.\n\n"
            "Saludos,\nEquipo SkyCode"
        )
        send_email(subject, recipients, body)

        flash("Coordinador/Directivo registrado exitosamente. Se ha enviado un correo con la contraseña temporal.", "register_COO_DIR-success")
        return redirect(url_for('academic_bp.register_user_route'))
    else:
        return render_template('register_user.html')
