from models import db, Alumno, Materia, CargaAcademica, PlanEstudios

def obtener_materias_pendientes(alumno_id):
    """
    Obtiene las materias pendientes (no cursadas o reprobadas) y sugiere materias para el siguiente cuatrimestre.
    """
    # Verificar si el alumno existe
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return {"error": f"Alumno con ID {alumno_id} no encontrado."}

    # Obtener las materias cursadas y su estado
    materias_aprobadas = db.session.query(Materia.id).join(CargaAcademica).filter(
        CargaAcademica.alumno_id == alumno_id,
        CargaAcademica.calificacion >= 7  # Materias aprobadas
    ).subquery()

    # Materias pendientes (no cursadas o reprobadas)
    materias_pendientes = db.session.query(Materia).join(PlanEstudios).filter(
        PlanEstudios.carrera_id == alumno.carrera_id,
        ~Materia.id.in_(materias_aprobadas)  # Excluir materias aprobadas
    ).all()

    # Sugerencias de materias para el siguiente cuatrimestre
    cuatrimestre_actual = db.session.query(db.func.max(PlanEstudios.cuatrimestre)).join(
        CargaAcademica, Materia
    ).filter(
        CargaAcademica.alumno_id == alumno_id
    ).scalar() or 1  # Si no hay materias cursadas, empezar en el cuatrimestre 1

    materias_sugeridas = db.session.query(Materia).join(PlanEstudios).filter(
        PlanEstudios.carrera_id == alumno.carrera_id,
        PlanEstudios.cuatrimestre == (cuatrimestre_actual + 1)  # Siguiente cuatrimestre
    ).all()

    # Formatear resultados
    pendientes = [{"nombre": m.nombre, "codigo": m.codigo} for m in materias_pendientes]
    sugerencias = [{"nombre": m.nombre, "codigo": m.codigo} for m in materias_sugeridas]

    return {
        "pendientes": pendientes,
        "sugerencias": sugerencias
    }
