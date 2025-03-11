from .calculate_progress import calculate_progress
from .show_pending_courses import get_pending_courses
from .view_grades import get_grades

def get_academic_progress(alumno_id):
    avance = calculate_progress(alumno_id)
    pending_courses = get_pending_courses(alumno_id)
    grades = get_grades(alumno_id)
    # Si tienes historial por cuatrimestre, inclúyelo; de lo contrario, usa lista vacía
    historial = []
    return {
        "avance": avance,
        "pending_courses": pending_courses,
        "grades": grades,
        "historial": historial
    }