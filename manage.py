from flask import Flask, jsonify
from models import Alumno, Materia, Calificacion, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  # Actualiza esto con la URI de tu base de datos
db.init_app(app)

@app.route('/alumno/<int:alumno_id>/materias-pendientes')
def ver_materias_pendientes(alumno_id):
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    # Obtener materias reprobadas (calificación menor a 6)
    materias_reprobadas = [cal.materia for cal in Calificacion.query.filter_by(alumno_id=alumno_id).filter(Calificacion.calificacion < 6).all()]
    
    # Obtener materias que faltan por cursar (no presentes en Calificaciones)
    materias_faltantes = [materia for materia in Materia.query.all() if materia.id not in [cal.materia_id for cal in Calificacion.query.filter_by(alumno_id=alumno_id).all()]]
    
    # Sugerir materias para el próximo cuatrimestre (esto puede ser ajustado según tus reglas de negocio)
    materias_sugeridas = obtener_materias_sugeridas(alumno)

    return jsonify({
        "pendientes": [materia.to_dict() for materia in materias_reprobadas],
        "faltantes": [materia.to_dict() for materia in materias_faltantes],
        "sugeridas": [materia.to_dict() for materia in materias_sugeridas]
    })

def obtener_materias_sugeridas(alumno):
    # Aquí puedes implementar la lógica para sugerir materias según el plan de estudios y las reglas específicas
    # Por simplicidad, aquí solo estamos devolviendo todas las materias del próximo cuatrimestre
    return Materia.query.join(PlanEstudios).filter(PlanEstudios.cuatrimestre == alumno.carrera.creditos // 24 + 1).all()

if __name__ == '__main__':
    app.run(debug=True)
