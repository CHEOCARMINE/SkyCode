from database import obtener_avance_carrera, obtener_historial_academico, obtener_materias_pendientes

def get_academic_progress(alumno_id):
    return {
        "avance": obtener_avance_carrera(alumno_id),
        "historial": obtener_historial_academico(alumno_id),
        "pending_courses": obtener_materias_pendientes(alumno_id),
    }
