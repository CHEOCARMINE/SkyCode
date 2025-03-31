from database import db
from models import Materia, Calificacion, Alumno

def generate_course_report(materia_id):
    """
    Genera un reporte para una materia específica usando datos reales de la BD.
    """
    materia = Materia.query.get(materia_id)
    if not materia:
        return None

    calificaciones = db.session.query(
        Alumno.nombre,
        Alumno.primer_apellido,
        Calificacion.calificacion
    ).join(Calificacion).filter(
        Calificacion.materia_id == materia_id
    ).all()

    datos = {
        "materia": materia.nombre,
        "calificaciones": []
    }

    for nombre, apellido, calif in calificaciones:
        datos["calificaciones"].append({
            "alumno": f"{nombre} {apellido}",
            "calificacion": float(calif)
        })

    return datos