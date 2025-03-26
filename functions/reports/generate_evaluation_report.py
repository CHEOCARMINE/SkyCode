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
            Alumno.nombre,
            Alumno.primer_apellido,
            Alumno.segundo_apellido,
            Calificacion.calificacion
        ).join(Calificacion).filter(
            Calificacion.materia_id == materia.id
        ).all()

        alumnos_data = []
        for nombre, ap1, ap2, calif in calificaciones:
            nombre_completo = f"{nombre} {ap1} {ap2}"
            alumnos_data.append({
                "alumno": nombre_completo,
                "calificacion": float(calif)
            })

        resultado.append({
            "materia": materia.nombre,
            "alumnos": alumnos_data
        })

    return resultado
