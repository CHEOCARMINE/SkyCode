from models import Materia, Calificacion, Alumno
from database import db

def generate_evaluation_report():
    """
    Genera un reporte agrupado por materia, mostrando alumnos y sus calificaciones.
    """
    materias = Materia.query.all()
    resultado = []

    for materia in materias:
        calificaciones = db.session.query(
            Alumno.primer_nombre,
            Alumno.primer_apellido,
            Calificacion.calificacion
        ).join(Calificacion).filter(
            Calificacion.materia_id == materia.id
        ).all()

        alumnos_data = []
        for nombre, apellido, calif in calificaciones:
            alumnos_data.append({
                "alumno": f"{nombre} {apellido}",
                "calificacion": float(calif)
            })

        resultado.append({
            "materia": materia.nombre,
            "alumnos": alumnos_data
        })

    return resultado
