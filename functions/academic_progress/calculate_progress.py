# functions/calculate_progress.py
from models import db, Calificacion, PlanEstudios, Alumno

def calculate_progress(alumno_id):
    """
    Calcula el porcentaje de avance de la carrera para el alumno.
    Se basa en la cantidad de materias aprobadas (por ejemplo, calificación >= 6)
    versus el total de materias del plan de estudios de la carrera.
    """
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return 0.0

    total_materias = PlanEstudios.query.filter_by(carrera_id=alumno.carrera_id).count()
    materias_aprobadas = Calificacion.query.filter_by(alumno_id=alumno_id).filter(Calificacion.calificacion >= 6).count()

    if total_materias == 0:
        return 0.0

    avance = (materias_aprobadas / total_materias) * 100
    return avance