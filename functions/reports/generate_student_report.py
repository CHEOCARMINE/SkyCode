from models import Alumno, Carrera, Calificacion, Materia

def generate_student_report(alumno_id):
    """
    Genera los datos para el reporte por alumno.
    """
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return None

    historial = []
    materias = Calificacion.query.filter_by(alumno_id=alumno.id).all()

    aprobadas = reprobadas = en_curso = 0

    for cal in materias:
        materia = Materia.query.get(cal.materia_id)
        estado = ""
        if cal.calificacion is None:
            estado = "En curso"
            en_curso += 1
        elif cal.calificacion >= 70:
            estado = "Aprobado"
            aprobadas += 1
        else:
            estado = "Reprobado"
            reprobadas += 1

        historial.append({
            "materia": materia.nombre if materia else "Desconocida",
            "calificacion": cal.calificacion if cal.calificacion is not None else "N/A",
            "estado": estado
        })

    datos = {
        "alumno": {
            "nombre_completo": f"{alumno.primer_nombre} {alumno.primer_apellido}",
            "matricula": alumno.matricula,
            "carrera": alumno.carrera.nombre if alumno.carrera else "N/A"
        },
        "historial": historial,
        "conteo_aprobadas": aprobadas,
        "conteo_reprobadas": reprobadas,
        "conteo_en_curso": en_curso
    }

    return datos
