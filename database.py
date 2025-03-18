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

def actualizar_alumno_y_usuario(matricula, 
                                primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                                curp, telefono, correo_electronico,
                                pais, estado_domicilio, municipio, colonia, cp, calle, numero_casa,
                                nuevo_estado, nueva_carrera):
    # Recuperar el alumno por matrícula
    alumno = Alumno.query.filter_by(matricula=matricula).first()
    if not alumno:
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

    # Actualizar el estado del alumno
    estado_obj = EstadoAlumno.query.filter_by(nombre_estado=nuevo_estado).first()
    if estado_obj:
        alumno.estado_id = estado_obj.id

    # Actualizar la carrera
    carrera_obj = Carrera.query.filter_by(nombre=nueva_carrera).first()
    if carrera_obj:
        alumno.carrera_id = carrera_obj.id

    # Actualizar el estado del usuario asociado
    usuario = alumno.usuario  
    if usuario:
        # Si el nuevo estado es "Activo", asigna 1; de lo contrario, 0.
        usuario.activo = 1 if nuevo_estado.lower() == "activo" else 0

    # Realizar el commit de los cambios
    db.session.commit()

    return alumno

# ------------------------------------------------------------
# 🔥 Aquí van las funciones NUEVAS para obtener datos académicos 🔥
# ------------------------------------------------------------

def obtener_avance_carrera(alumno_id):
    """
    Calcula el avance de la carrera en porcentaje basado en materias aprobadas.
    """
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return 0

    carrera = Carrera.query.get(alumno.carrera_id)
    if not carrera:
        return 0

    creditos_aprobados = db.session.query(db.func.sum(Materia.creditos)).join(Calificacion).filter(
        Calificacion.alumno_id == alumno_id,
        Calificacion.calificacion >= 7  
    ).scalar() or 0

    porcentaje_avance = (creditos_aprobados / carrera.creditos) * 100
    return round(porcentaje_avance, 2)


def obtener_historial_academico(alumno_id):
    """
    Obtiene las materias aprobadas, reprobadas y en curso por cuatrimestre.
    """
    historial = []
    
    for cuatrimestre in range(1, 10):  
        materias = db.session.query(
            Materia.nombre.label("materia"),
            Calificacion.calificacion.label("calificacion"),
        ).join(Calificacion).filter(
            Calificacion.alumno_id == alumno_id,
            Materia.id == Calificacion.materia_id,
            PlanEstudios.cuatrimestre == cuatrimestre,
            PlanEstudios.materia_id == Materia.id
        ).all()

        aprobadas = sum(1 for mat in materias if mat.calificacion >= 7)
        reprobadas = sum(1 for mat in materias if mat.calificacion < 7)
        en_curso = sum(1 for mat in materias if mat.calificacion is None)

        historial.append({
            "cuatrimestre": cuatrimestre,
            "aprobadas": aprobadas,
            "reprobadas": reprobadas,
            "en_curso": en_curso,
            "calificaciones": [mat.calificacion for mat in materias if mat.calificacion]
        })
    
    return historial


def obtener_materias_pendientes(alumno_id):
    """
    Obtiene las materias pendientes (no cursadas o no aprobadas).
    """
    materias_pendientes = db.session.query(
        Materia.nombre
    ).join(PlanEstudios).filter(
        PlanEstudios.carrera_id == Alumno.carrera_id,
        PlanEstudios.materia_id == Materia.id,
        ~db.exists().where(
            (Calificacion.alumno_id == alumno_id) &
            (Calificacion.materia_id == Materia.id) &
            (Calificacion.calificacion >= 7)  
        )
    ).all()

    return [materia.nombre for materia in materias_pendientes]

def obtener_numero_alumnos_inscritos():
    """
    Retorna el número total de alumnos inscritos.
    """
    return db.session.query(Alumno).count()

def obtener_numero_alumnos_egresados():
    """
    Retorna el número total de alumnos egresados.
    """
    return db.session.query(Alumno).filter(Alumno.estado_id == 3).count()


def obtener_promedios_por_carrera():
    """
    Retorna un diccionario con el promedio general de calificaciones por carrera.
    Si no hay datos, retorna 0 en lugar de "N/A".
    """
    carreras = db.session.query(Carrera).all()
    promedios = {}

    for carrera in carreras:
        promedio = db.session.query(db.func.avg(Calificacion.calificacion)).join(Alumno).filter(
            Alumno.carrera_id == carrera.id,
            Calificacion.calificacion != None
        ).scalar() or 0  # Si no hay datos, devuelve 0 en lugar de None o "N/A"
        
        promedios[carrera.nombre] = round(promedio, 2)  # Redondeo seguro

    return promedios


def obtener_estadisticas_generales():
    try:
        total_alumnos = Alumno.query.count()
        total_egresados = Alumno.query.filter(Alumno.estado_id == 3).count()
        promedio_global = db.session.query(db.func.avg(Calificacion.calificacion)).scalar() or 0
    except Exception as e:
        db.session.rollback()
        raise e  # Sigue mostrando el error, pero no cierra la sesión manualmente.

    return {
        "total_alumnos": total_alumnos,
        "total_egresados": total_egresados,
        "promedio_global": round(promedio_global, 2)
    }


# -------------------------------------------------
# Nota:
# Este archivo unificado (database.py) centraliza tanto las funciones de acceso a datos
# como algunas integraciones con servicios externos. Se planea trasladar la lógica de
# integración a un módulo independiente (services.py) en el futuro para separar responsabilidades.
# -------------------------------------------------