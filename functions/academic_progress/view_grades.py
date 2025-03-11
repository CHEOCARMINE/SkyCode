# functions/view_grades.py
from models import db, Calificacion, Materia

def get_grades(alumno_id):
    """
    Retorna una lista de diccionarios, cada uno con el nombre de la materia y la calificación obtenida.
    """
    # Realiza un join entre Calificacion y Materia
    records = db.session.query(Calificacion, Materia).join(Materia, Calificacion.materia_id == Materia.id)\
              .filter(Calificacion.alumno_id == alumno_id).all()
    grades = []
    for cal, materia in records:
        grades.append({
            "materia": materia.nombre,
            "calificacion": float(cal.calificacion) if cal.calificacion is not None else None
        })
    return grades