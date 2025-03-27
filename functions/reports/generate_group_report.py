from models import Alumno, Carrera, EstadoAlumno, Calificacion
from database import db
from collections import defaultdict

def generate_group_report():
    """
    Genera el reporte por grupo (por carrera), agrupando alumnos y mostrando su estado académico.
    """
    carreras = Carrera.query.all()
    datos = []

    for carrera in carreras:
        alumnos = Alumno.query.filter_by(carrera_id=carrera.id).all()

        alumnos_info = []
        for alumno in alumnos:
            estado = alumno.estado.nombre_estado if alumno.estado else "Sin estado"
            nombre_completo = f"{alumno.nombre} {alumno.primer_apellido} {alumno.segundo_apellido}"
            alumnos_info.append({
                "nombre": nombre_completo,
                "estado": estado
            })

        datos.append({
            "carrera": carrera.nombre,
            "alumnos": alumnos_info,
            "cantidad": len(alumnos_info)
        })

    return datos