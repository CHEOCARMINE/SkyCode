import logging
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import (
    db,
    Role,
    EstadoAlumno,
    Cuatrimestre,
    Carrera,
    Alumno,
    Usuario,
    Grupo,
    GrupoAlumno,
    Materia,
    PlanEstudios,
    TipoCargaAcademica,
    CargaAcademica,
    Calificacion,
    EvaluacionDocente,
    Notificacion,
    Reporte,
    Domicilio,
    Coordinadores_Directivos
)

bcrypt = Bcrypt()

def init_db(app):
    """
    Inicializa la conexión a la base de datos.
    Se llama desde app.py en el contexto de la aplicación.
    """
    db.init_app(app)

# ------------------------------------------------------------
# Funciones para el registro de nuevos domicilios y alumnos
# ------------------------------------------------------------

def insertar_domicilio(estado, municipio, colonia, cp, calle, numero_casa, pais="México"):
    """
    Inserta un nuevo registro en la tabla Domicilios y lo guarda en la base de datos.
    
    :param estado: Estado (string)
    :param municipio: Municipio (string)
    :param colonia: Colonia (string)
    :param cp: Código Postal (string)
    :param calle: Calle (string)
    :param numero_calle: Número de calle (string)
    :param pais: País (por defecto "México")
    :return: Objeto Domicilio insertado.
    """
    nuevo_domicilio = Domicilio(
        pais=pais,
        estado=estado,
        municipio=municipio,
        colonia=colonia,
        cp=cp,
        calle=calle,
        numero_casa=numero_casa
    )
    db.session.add(nuevo_domicilio)
    db.session.commit()  # Commit para asignar un ID al domicilio
    return nuevo_domicilio

def insertar_alumno(matricula, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, 
                    curp, domicilio_id, telefono, correo_electronico, certificado_preparatoria, 
                    comprobante_pago, estado_id, carrera_id):
    """
    Inserta un nuevo registro en la tabla Alumnos usando el ID del domicilio insertado.
    Retorna el objeto Alumno insertado.
    """
    nuevo_alumno = Alumno(
        matricula=matricula,
        primer_nombre=primer_nombre,
        segundo_nombre=segundo_nombre,
        primer_apellido=primer_apellido,
        segundo_apellido=segundo_apellido,
        curp=curp,
        domicilio_id=domicilio_id,
        telefono=telefono,
        correo_electronico=correo_electronico,
        certificado_preparatoria=certificado_preparatoria,
        comprobante_pago=comprobante_pago,
        estado_id=estado_id,
        carrera_id=carrera_id
    )
    db.session.add(nuevo_alumno)
    db.session.commit()
    return nuevo_alumno

def crear_usuario_para_alumno(alumno_id, hashed_password, rol_id=1):
    """
    Crea el usuario asociado al alumno usando su ID, encripta la contraseña y lo guarda.
    Retorna el objeto Usuario creado.
    """
    nuevo_usuario = Usuario(
        contraseña=hashed_password,
        rol_id=rol_id,
        alumno_id=alumno_id
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario

def existe_alumno_por_curp(curp):
    """
    Retorna el objeto Alumno si existe un registro con el CURP proporcionado,
    o None en caso contrario.
    """
    from models import Alumno 
    return Alumno.query.filter_by(curp=curp).first()

# -------------------------------------------------
# Nota:
# Este archivo unificado (database.py) centraliza tanto las funciones de acceso a datos
# como algunas integraciones con servicios externos. Se planea trasladar la lógica de
# integración a un módulo independiente (services.py) en el futuro para separar responsabilidades.
# -------------------------------------------------
