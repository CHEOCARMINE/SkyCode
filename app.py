from flask import Flask, redirect, render_template, url_for, flash
from config import config_by_name
from database import init_db
from services import init_mail
from routes import academic_bp
from functions.auth.login import auth_bp as login_bp
from flask_login import LoginManager, current_user
from models import Usuario, Alumno
from routes import alumno_progress_bp 

def create_app(config_name="development"):
    """
    Crea y configura la aplicación Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Inicializa la base de datos
    init_db(app)
    
    # Inicializa Flask-Mail
    init_mail(app)
    
    # Inicializa Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Rutas
    @app.route('/perfil') 
    def perfil():
        usuario = Usuario.query.get(current_user.id)  # Asegúrate de estar autenticado
        alumno = Alumno.query.get(usuario.alumno_id) if usuario and usuario.alumno_id else None
        return render_template('perfil.html', alumno=alumno)

    @app.route('/evaluacion_docente')
    def evaluacion_docente():
        return render_template('evaluacion_docente.html')

    # Registra los blueprints
    app.register_blueprint(academic_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(alumno_progress_bp)

    # Manejo del error 413 (Request Entity Too Large)
    @app.errorhandler(413)
    def request_entity_too_large(error):
        flash("El archivo subido es demasiado grande.", "registe-danger")
        return redirect(url_for('academic_bp.registrar_alumno'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config.get("DEBUG", False))
