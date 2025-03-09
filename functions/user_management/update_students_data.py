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
    Si alguna validación falla, se lanza un ValueError.
    """
    
    # Validaciones de datos personales
    if not validate_letters(primer_nombre):
        raise ValueError("El primer nombre contiene caracteres no válidos.")
    if segundo_nombre and not validate_letters(segundo_nombre, required=False):
        raise ValueError("El segundo nombre contiene caracteres no válidos.")
    if not validate_letters(primer_apellido):
        raise ValueError("El primer apellido contiene caracteres no válidos.")
    if segundo_apellido and not validate_letters(segundo_apellido, required=False):
        raise ValueError("El segundo apellido contiene caracteres no válidos.")
    if not validate_curp(curp):
        raise ValueError("El CURP es inválido.")
    if not validate_telefono(telefono):
        raise ValueError("El teléfono debe contener 10 dígitos.")
    if not validate_correo(correo_electronico):
        raise ValueError("El correo electrónico es inválido o el dominio no está permitido.")
    
    # Validaciones de datos del domicilio
    if not validate_letters(pais):
        raise ValueError("El país contiene caracteres no válidos.")
    if not validate_letters(estado_domicilio):
        raise ValueError("El estado del domicilio contiene caracteres no válidos.")
    if not validate_letters(municipio):
        raise ValueError("El municipio contiene caracteres no válidos.")
    if not validate_letters(colonia):
        raise ValueError("La colonia contiene caracteres no válidos.")
    if not validate_postal_code(cp):
        raise ValueError("El código postal debe contener exactamente 5 dígitos.")
    if not validate_alphanumeric(calle):
        raise ValueError("La calle contiene caracteres no válidos.")
    if not validate_alphanumeric(numero_casa):
        raise ValueError("El número de casa contiene caracteres no válidos.")
    
    alumno = Alumno.query.filter_by(matricula=matricula).first()
    if not alumno:
        raise ValueError("Alumno no encontrado.")
    
    alumno.primer_nombre = primer_nombre
    alumno.segundo_nombre = segundo_nombre
    alumno.primer_apellido = primer_apellido
    alumno.segundo_apellido = segundo_apellido
    alumno.curp = curp
    alumno.telefono = telefono
    alumno.correo_electronico = correo_electronico
    
    if alumno.domicilio:
        alumno.domicilio.pais = pais
        alumno.domicilio.estado = estado_domicilio
        alumno.domicilio.municipio = municipio
        alumno.domicilio.colonia = colonia
        alumno.domicilio.cp = cp
        alumno.domicilio.calle = calle
        alumno.domicilio.numero_casa = numero_casa
    
    estado_obj = EstadoAlumno.query.filter_by(nombre_estado=nuevo_estado).first()
    if estado_obj:
        alumno.estado_id = estado_obj.id
    else:
        raise ValueError("El estado especificado no existe.")
    
    carrera_obj = Carrera.query.filter_by(nombre=nueva_carrera).first()
    if carrera_obj:
        alumno.carrera_id = carrera_obj.id
    else:
        raise ValueError("La carrera especificada no existe.")
    
    usuario = alumno.usuario  
    if usuario:
        usuario.activo = True if nuevo_estado.lower() == "activo" else False
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    
    return alumno
