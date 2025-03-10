from flask import flash
from models import Alumno, EstadoAlumno, Carrera, db
from functions.auth.validations import (
    validate_letters,
    validate_curp,
    validate_telefono,
    validate_correo,
    validate_postal_code,
    validate_alphanumeric
)

def actualizar_alumno_y_usuario(
    matricula,
    primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
    curp, telefono, correo_electronico,
    pais, estado_domicilio, municipio, colonia, cp, calle, numero_casa,
    nuevo_estado, nueva_carrera
):
    """
    Actualiza los datos del alumno identificado por 'matricula' y, 
    de acuerdo al nuevo estado, actualiza el campo 'activo' del usuario asociado.
    
    Se aplican las validaciones utilizando las funciones definidas en functions/auth/validations.py.
    Si alguna validación falla, se hace flash del error con la categoría "modify-danger"
    y se retorna None.
    """
    
    # Validaciones de datos personales
    if not validate_letters(primer_nombre):
        flash("El primer nombre contiene caracteres no válidos.", "modify-danger")
        return None
    if segundo_nombre and not validate_letters(segundo_nombre, required=False):
        flash("El segundo nombre contiene caracteres no válidos.", "modify-danger")
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
    alumno.primer_nombre = primer_nombre
    alumno.segundo_nombre = segundo_nombre
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
    usuario = alumno.usuario  # Se asume que la relación es uno a uno entre Alumno y Usuario
    if usuario:
        usuario.activo = True if nuevo_estado.lower() == "activo" else False
    
    # Realizar el commit de los cambios
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash("Error al guardar los cambios en la base de datos.", "modify-danger")
        return None
    
    return alumno
