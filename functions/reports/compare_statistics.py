from models import Carrera, Alumno, Calificacion
from database import db

def comparar_estadisticas(carrera_id_1, carrera_id_2):
    carreras = Carrera.query.filter(Carrera.id.in_([carrera_id_1, carrera_id_2])).all()
    resultado = []

    for carrera in carreras:
        alumnos = Alumno.query.filter_by(carrera_id=carrera.id).all()
        total_alumnos = len(alumnos)

        # Contar egresados (estado_id = 3)
        total_egresados = Alumno.query.filter_by(carrera_id=carrera.id, estado_id=3).count()

        # Promedio de calificaciones
        calificaciones = db.session.query(Calificacion.calificacion).join(Alumno).filter(
            Alumno.carrera_id == carrera.id,
            Calificacion.calificacion.isnot(None)
        ).all()

        promedio = round(
            sum([c[0] for c in calificaciones]) / len(calificaciones),
            2
        ) if calificaciones else ""

        resultado.append({
            "id": carrera.id,
            "nombre": carrera.nombre,
            "total_alumnos": total_alumnos,
            "total_egresados": total_egresados,
            "promedio": promedio
        })

    return resultado
