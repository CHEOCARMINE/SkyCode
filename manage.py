#Ejemplo de login con roles al momento de iniciar sesion
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from config import get_db_connection
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'clave_secreta'
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s AND activo = 1", (usuario,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user['contraseña'], contraseña):
            session['usuario'] = user['nombre_usuario']
            session['rol'] = user['rol']

            if user['rol'] == 'directivo':
                return redirect(url_for('dashboard', rol='directivo'))
            elif user['rol'] == 'coordinador':
                return redirect(url_for('dashboard', rol='coordinador'))
            elif user['rol'] == 'alumno':
                return redirect(url_for('dashboard', rol='alumno'))
        else:
            flash("Usuario o contraseña incorrectos, o cuenta inactiva.", "danger")

    return render_template('login.html')

@app.route('/dashboard/<rol>')
def dashboard(rol):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', rol=rol)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


#Ver materias pendientes
from flask import Flask, jsonify
from models import Alumno, Materia, Calificacion, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ulzjbyhniqbdiwgh:6dJiPKrE1AXfiS1jsfOV@bef4yknw2tlo8ei20zko-mysql.services.clever-cloud.com:3306/bef4yknw2tlo8ei20zko'
db.init_app(app)

@app.route('/materias_pendientes')
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ulzjbyhniqbdiwgh:6dJiPKrE1AXfiS1jsfOV@bef4yknw2tlo8ei20zko-mysql.services.clever-cloud.com:3306/bef4yknw2tlo8ei20zko'  # Actualizar esto con la URI de la base de datos
db.init_app(app)

@app.route('/validar_carga', methods=['POST'])
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

#dfg
from flask import Flask
from config import get_db_connection
from routes import routes

app = Flask(__name__)
db = get_db_connection(app)

app.register_blueprint(routes, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
