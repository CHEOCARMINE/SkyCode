# functions/show_pending_courses.py
from models import db, PlanEstudios, Calificacion, Materia, Alumno

def get_pending_courses(alumno_id):
    """
    Retorna una lista de nombres de materias pendientes para el alumno.
    Se consideran pendientes las materias que están en el plan de estudios de la carrera
    pero que no han sido aprobadas (por ejemplo, calificación < 6).
    """
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return []

    # Obtener todas las materias del plan de estudios de la carrera del alumno
    plan = PlanEstudios.query.filter_by(carrera_id=alumno.carrera_id).all()
    materia_ids_plan = [p.materia_id for p in plan]

    # Materias aprobadas
    aprobadas = Calificacion.query.filter_by(alumno_id=alumno_id).filter(Calificacion.calificacion >= 6).all()
    aprobadas_ids = [a.materia_id for a in aprobadas]

    # Materias pendientes: aquellas que están en el plan pero no se han aprobado
    pendientes_ids = [mid for mid in materia_ids_plan if mid not in aprobadas_ids]

    if pendientes_ids:
        pending_courses = Materia.query.filter(Materia.id.in_(pendientes_ids)).all()
        return [m.nombre for m in pending_courses]
    return []