from flask import Flask, redirect, url_for, flash
from config import config_by_name
from database import init_db
from services import init_mail
from routes import academic_bp, alumno_progress_bp, docentes_bp 
from functions.auth.login import auth_bp as login_bp
from flask_login import LoginManager
from models import Usuario
from routes import alumno_progress_bp 
from routes import reports_bp



def create_app(config_name="development"):
    """
    Crea y configura la aplicación Flask.
    
    - Carga la configuración correspondiente al entorno.
    - Inicializa la conexión a la base de datos.
    - Inicializa Flask-Mail.
    - Inicializa Flask-Login.
    - Registra los blueprints (rutas) de la aplicación.
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
    
    # Registra los blueprints
    app.register_blueprint(academic_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(alumno_progress_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(docentes_bp)  # Aquí registramos el Blueprint de docentes

    # Manejo del error 413 (Request Entity Too Large)
    @app.errorhandler(413)
    def request_entity_too_large(error):
        flash("El archivo subido es demasiado grande.", "registe-danger")
        return redirect(url_for('academic_bp.registrar_alumno'))
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config.get("DEBUG", False))
