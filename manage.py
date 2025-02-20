from flask import Flask, jsonify
from models import Alumno, Materia, Calificacion, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  # Actualizar esto con la URI de la base de datos
db.init_app(app)

@app.route('/alumno/<int:alumno_id>/materias-pendientes')
def ver_materias_pendientes(alumno_id):
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    # Obtener materias reprobadas (calificación menor a 5)
    materias_reprobadas = [cal.materia for cal in Calificacion.query.filter_by(alumno_id=alumno_id).filter(Calificacion.calificacion < 5).all()]
    
    # Obtener materias que faltan por cursar (no presentes en Calificaciones)
    materias_faltantes = [materia for materia in Materia.query.all() if materia.id not in [cal.materia_id for cal in Calificacion.query.filter_by(alumno_id=alumno_id).all()]]
    
    # Sugerir materias para el próximo cuatrimestre 
    materias_sugeridas = obtener_materias_sugeridas(alumno)

    return jsonify({
        "pendientes": [materia.to_dict() for materia in materias_reprobadas],
        "faltantes": [materia.to_dict() for materia in materias_faltantes],
        "sugeridas": [materia.to_dict() for materia in materias_sugeridas]
    })

def obtener_materias_sugeridas(alumno):
    #Aqui se puede implementar la logica para sugerir materias según el plan de estudios
    #Debido a que aun no se implementa de manera correcta, aquí solo se devuelven todas las materias del próximo cuatrimestre
    return Materia.query.join(PlanEstudios).filter(PlanEstudios.cuatrimestre == alumno.carrera.creditos // 24 + 1).all()

if __name__ == '__main__':
    app.run(debug=True)



#Validar carga de materias
from flask import Flask, jsonify, request
from models import Alumno, Materia, CargaAcademica, PlanEstudios, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  # Actualizar esto con la URI de la base de datos
db.init_app(app)

@app.route('/alumno/<int:alumno_id>/validar-carga', methods=['POST'])
def validar_carga(alumno_id):
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    data = request.get_json()
    materias_ids = data.get("materias_ids", [])

    # Numero máximo de materias permitidas por cuatrimestre
    max_materias = 10

    # Obtener las materias seleccionadas
    materias = Materia.query.filter(Materia.id.in_(materias_ids)).all()
    total_creditos = sum(materia.creditos for materia in materias)
    total_materias = len(materias)

    if total_materias > max_materias:
        return jsonify({"error": "La carga académica excede el número máximo de materias permitidas por cuatrimestre"}), 400

    # Verificar correlativas pendientes
    alertas = []
    for materia in materias:
        correlativa = materia.correlativa
        if correlativa and correlativa.id not in [cal.materia_id for cal in alumno.calificaciones if cal.calificacion >= 6]:
            alertas.append(f"La materia {materia.nombre} tiene correlativas pendientes")

    if alertas:
        return jsonify({"alertas": alertas}), 400

    return jsonify({"message": "La carga académica es válida"}), 200

if __name__ == '__main__':
    app.run(debug=True)
