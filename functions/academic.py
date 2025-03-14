from flask import render_template, make_response
from weasyprint import HTML
from database import db
from models import Alumno, CargaAcademica

def generar_horario_pdf(alumno_id):
    """
    Consulta los datos necesarios usando SQLAlchemy y genera un PDF.
    """
    try:
        # Consulta: Obtener al alumno
        alumno = Alumno.query.get(alumno_id)
        if not alumno:
            return f"Alumno con ID {alumno_id} no encontrado.", 404

        # Consulta: Cargas académicas del alumno
        cargas_academicas = CargaAcademica.query.filter_by(alumno_id=alumno_id).all()

        # Construir datos para la plantilla HTML
        clases = []
        for carga in cargas_academicas:
            materia = carga.materia
            clases.append({
                "nombre_materia": materia.nombre,
                "horario": f"{materia.codigo} (CRN: {materia.crn})",
                "salon": "Por Definir",  # Personaliza si se requieren datos adicionales
                "nombre_docente": "Por Definir"  # Ajusta si hay relación directa con docentes
            })

    except Exception as e:
        return f"Error al obtener datos: {e}", 500

    # Generar el PDF a partir del HTML
    html = render_template('horario.html', clases=clases, alumno_id=alumno_id)
    pdf = HTML(string=html).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=horario.pdf'
    return response
