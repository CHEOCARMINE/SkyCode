from models import Carrera, Alumno, Calificacion
from database import db

def generate_career_report():
    carreras = Carrera.query.all()
    datos = []

    for carrera in carreras:
        alumnos = Alumno.query.filter_by(carrera_id=carrera.id).all()
        total = len(alumnos)

        # Calificaciones válidas (descarta None)
        calificaciones = db.session.query(Calificacion.calificacion).join(Alumno).filter(
            Alumno.carrera_id == carrera.id
        ).all()

        calif_validas = [c[0] for c in calificaciones if c[0] is not None]

        # Mostrar promedio solo si hay datos válidos
        promedio = round(sum(calif_validas) / len(calif_validas), 2) if calif_validas else ""

        datos.append({
            "carrera": carrera.nombre,
            "total_alumnos": total,
            "promedio": promedio
        })

    return datos
