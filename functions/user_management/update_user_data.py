from flask import flash
from models import Coordinadores_Directivos, Usuario, db
from functions.auth.validations import (
    validate_letters,
    validate_correo
)
from database import bcrypt

def actualizar_coordinador_directivo(
    user_id,
    primer_nombre,
    primer_apellido,
    correo_electronico,
    nuevo_estado
):
    """
    Actualiza los datos del Coordinador/Directivo identificado por 'user_id' y,
    de acuerdo al nuevo estado, actualiza el campo 'activo' del usuario asociado.
    
    Se actualizan los siguientes campos editables:
      - Nombre (primer_nombre)
      - Apellido (primer_apellido)
      - Correo electrónico (correo_electronico)
      - Estado de la cuenta (activo: 1, inactivo: 0)
    
    Si alguna validación falla, se hace flash del error con la categoría "modify-danger"
    y se retorna None.
    """

    # Validaciones básicas de datos personales
    if not validate_letters(primer_nombre):
        flash("El primer nombre contiene caracteres no válidos.", "modify-danger")
        return None
    if not validate_letters(primer_apellido):
        flash("El primer apellido contiene caracteres no válidos.", "modify-danger")
        return None
    if not validate_correo(correo_electronico):
        flash("El correo electrónico es inválido o el dominio no está permitido.", "modify-danger")
        return None

    # Buscar al Coordinador/Directivo por su ID
    registro = Coordinadores_Directivos.query.get(user_id)
    if not registro:
        flash("Coordinador/Directivo no encontrado.", "modify-danger")
        return None

    # Actualizar datos editables
    registro.primer_nombre = primer_nombre
    registro.primer_apellido = primer_apellido
    registro.correo_electronico = correo_electronico

    # Actualizar el estado del usuario asociado (si existe)
    usuario = registro.usuario  
    if usuario:
        # Se utiliza 1 para activo y 0 para inactivo
        usuario.activo = 1 if nuevo_estado.lower() == "activo" else 0

    # Realizar el commit de los cambios
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash("Error al guardar los cambios en la base de datos.", "modify-danger")
        return None

    return registro
