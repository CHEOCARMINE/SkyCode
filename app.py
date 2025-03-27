from flask import Flask, redirect, render_template, request, url_for, flash
from config import config_by_name
from database import init_db
from services import init_mail
from reports import reports_bp
from routes import academic_bp, alumno_progress_bp 
from functions.auth.login import auth_bp as login_bp
from flask_login import LoginManager, current_user
from models import Materia, Usuario, Alumno
from config import Config
import mysql.connector

# Accediendo a la configuración de la base de datos
db_config = {
    'host': Config.DB_HOST,
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'database': Config.DB_NAME,
    'port': Config.DB_PORT
}

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    init_db(app)
    init_mail(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    @app.route('/perfil') 
    def perfil():
        usuario = Usuario.query.get(current_user.id)
        alumno = Alumno.query.get(usuario.alumno_id) if usuario and usuario.alumno_id else None
        return render_template('perfil.html', alumno=alumno)

    @app.route('/inscripcion_materias', methods=['GET', 'POST'])
    def inscripcion_materias():
        materias_seleccionadas = []
        if request.method == 'POST':
            crn = request.form.get('crn')
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Materias WHERE crn = %s", (crn,))
            materia = cursor.fetchone()
            cursor.close()
            conn.close()
            if materia:
                materias_seleccionadas.append(materia)
            else:
                flash('CRN no encontrado. Por favor, intenta nuevamente.', 'danger')
        return render_template('inscripcion_materias.html', materias=materias_seleccionadas)

    @app.route('/confirmar_inscripcion', methods=['POST'])
    def confirmar_inscripcion():
        materias_seleccionadas = request.form.getlist('materias')
        id_alumno = current_user.id

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        for crn in materias_seleccionadas:
            query = "INSERT INTO materias_cargadas (id_alumno, id_materia) VALUES (%s, %s)"
            cursor.execute(query, (id_alumno, crn))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Inscripción confirmada exitosamente', 'success')
        return redirect(url_for('historial_materias'))

    @app.route('/historial_materias')
    def historial_materias():
        id_alumno = current_user.id

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT m.nombre, m.codigo 
        FROM Materias m 
        JOIN materias_cargadas mc ON m.id = mc.id_materia 
        WHERE mc.id_alumno = %s
        """
        cursor.execute(query, (id_alumno,))
        materias = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('historial_materias.html', materias=materias)

    app.register_blueprint(academic_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(alumno_progress_bp)
    app.register_blueprint(reports_bp)

    @app.errorhandler(413)
    def request_entity_too_large(error):
        flash("El archivo subido es demasiado grande.", "registe-danger")
        return redirect(url_for('academic_bp.registrar_alumno'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config.get("DEBUG", False))