from models import db, Horario, Alumno, Materia
from fpdf import FPDF

def obtener_horarios_por_matricula(matricula):
    alumno = Alumno.query.filter_by(matricula=matricula).first()
    if not alumno:
        return {"error": "Alumno no encontrado."}
    return Horario.query.filter_by(alumno_id=alumno.id).all()

def crear_horario(data):
    # Validar restricciones
    if Horario.query.filter_by(dia_semana=data['dia_semana'], hora_inicio=data['hora_inicio'], alumno_id=data['alumno_id']).first():
        return {"error": "Horario en conflicto."}
    nuevo_horario = Horario(**data)
    db.session.add(nuevo_horario)
    db.session.commit()
    return {"success": "Horario creado exitosamente."}

def generar_horario_pdf(horarios):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for horario in horarios:
        pdf.cell(200, 10, txt=f"{horario.materia.nombre} - {horario.dia_semana} - {horario.hora_inicio}-{horario.hora_fin}", ln=True)
    return pdf.output(dest="S").encode("latin1")
