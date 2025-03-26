from flask import flash
from models import Alumno, EstadoAlumno, Carrera, db
from functions.auth.validations import (
    validate_letters,
    validate_curp,
    validate_telefono,
    validate_correo,
    validate_postal_code,
    validate_alphanumeric,
    validate_file
)
from database import bcrypt  # Para encriptar la contraseña

def actualizar_alumno_y_usuario(
    matricula,
    nombre, primer_apellido, segundo_apellido,
    curp, telefono, correo_electronico,
    pais, estado_domicilio, municipio, colonia, cp, calle, numero_casa,
    nuevo_estado, nueva_carrera,
    nueva_contrasena=None, nuevo_certificado=None, nuevo_comprobante=None
):
    """
    Actualiza los datos del alumno identificado por 'matricula' y, de acuerdo al nuevo estado,
    actualiza el campo 'activo' del usuario asociado.

    Además, actualiza opcionalmente la contraseña (si se proporciona nueva_contrasena),
    el certificado de preparatoria (si se proporciona nuevo_certificado) y el comprobante de pago
    (si se proporciona nuevo_comprobante).

    Se aplican las validaciones utilizando las funciones definidas en functions/auth/validations.py.
    Si alguna validación falla, se hace flash del error con la categoría "modify-danger" y se retorna None.
    """

    # Validaciones de datos personales
    if not validate_letters(nombre):
        flash("El nombre contiene caracteres no válidos.", "modify-danger")
        return None
    if not validate_letters(primer_apellido):
        flash("El apellido paterno contiene caracteres no válidos.", "modify-danger")
        return None
    if segundo_apellido and not validate_letters(segundo_apellido, required=False):
        flash("El apellido materno contiene caracteres no válidos.", "modify-danger")
        return None
    if not validate_curp(curp):
        flash("El CURP es inválido.", "modify-danger")
        return None
    if not validate_telefono(telefono):
        flash("El teléfono debe contener 10 dígitos.", "modify-danger")
        return None
    if not validate_correo(correo_electronico):
        flash("El correo electrónico es inválido o el dominio no está permitido.", "modify-danger")
        return None

    # Validaciones de datos del domicilio
    if not validate_letters(pais):
        flash("El país contiene caracteres no válidos.", "modify-danger")
        return None
    if not validate_letters(estado_domicilio):
        flash("El estado del domicilio contiene caracteres no válidos.", "modify-danger")
        return None
    if not validate_letters(municipio):
        flash("El municipio contiene caracteres no válidos.", "modify-danger")
        return None
    if not validate_letters(colonia):
        flash("La colonia contiene caracteres no válidos.", "modify-danger")
        return None
    if not validate_postal_code(cp):
        flash("El código postal debe contener exactamente 5 dígitos.", "modify-danger")
        return None
    if not validate_alphanumeric(calle):
        flash("La calle contiene caracteres no válidos.", "modify-danger")
        return None
    if not validate_alphanumeric(numero_casa):
        flash("El número de casa contiene caracteres no válidos.", "modify-danger")
        return None

    # Buscar al alumno por matrícula
    alumno = Alumno.query.filter_by(matricula=matricula).first()
    if not alumno:
        flash("Alumno no encontrado.", "modify-danger")
        return None

    # Actualizar datos personales del alumno
    alumno.nombre = nombre  # Cambio: antes era alumno.primer_nombre
    alumno.primer_apellido = primer_apellido
    alumno.segundo_apellido = segundo_apellido
    alumno.curp = curp
    alumno.telefono = telefono
    alumno.correo_electronico = correo_electronico

    # Actualizar datos del domicilio, si existe
    if alumno.domicilio:
        alumno.domicilio.pais = pais
        alumno.domicilio.estado = estado_domicilio
        alumno.domicilio.municipio = municipio
        alumno.domicilio.colonia = colonia
        alumno.domicilio.cp = cp
        alumno.domicilio.calle = calle
        alumno.domicilio.numero_casa = numero_casa
    else:
        flash("El alumno no tiene domicilio asociado.", "modify-danger")
        return None

    # Actualizar estado del alumno (relación con EstadoAlumno)
    estado_obj = EstadoAlumno.query.filter_by(nombre_estado=nuevo_estado).first()
    if estado_obj:
        alumno.estado_id = estado_obj.id
    else:
        flash("El estado especificado no existe.", "modify-danger")
        return None

    # Actualizar la carrera (relación con Carrera)
    carrera_obj = Carrera.query.filter_by(nombre=nueva_carrera).first()
    if carrera_obj:
        alumno.carrera_id = carrera_obj.id
    else:
        flash("La carrera especificada no existe.", "modify-danger")
        return None

    # Actualizar el usuario asociado (activación/desactivación)
    usuario = alumno.usuario  
    if usuario:
        usuario.activo = True if nuevo_estado.lower() == "activo" else False

    # Actualizar la contraseña si se proporciona una nueva
    if nueva_contrasena:
        hashed = bcrypt.generate_password_hash(nueva_contrasena).decode('utf-8')
        usuario.contraseña = hashed

    # Validar y actualizar el certificado de preparatoria si se proporciona un nuevo archivo
    if nuevo_certificado:
        valid, mensaje = validate_file(nuevo_certificado)
        if not valid:
            flash("Certificado: " + mensaje, "modify-danger")
            return None
        alumno.certificado_preparatoria = nuevo_certificado.read()

    # Validar y actualizar el comprobante de pago si se proporciona un nuevo archivo
    if nuevo_comprobante:
        valid, mensaje = validate_file(nuevo_comprobante)
        if not valid:
            flash("Comprobante: " + mensaje, "modify-danger")
            return None
        alumno.comprobante_pago = nuevo_comprobante.read()

    # Realizar el commit de los cambios
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash("Error al guardar los cambios en la base de datos.", "modify-danger")
        return None

    return alumno
