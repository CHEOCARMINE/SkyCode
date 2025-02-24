from flask import Flask, redirect, url_for, flash
from config import config_by_name
from database import init_db
from services import init_mail
from routes import academic_bp

def create_app(config_name="development"):
    """
    Crea y configura la aplicación Flask.
    
    - Carga la configuración correspondiente al entorno.
    - Inicializa la conexión a la base de datos.
    - Inicializa Flask-Mail.
    - Registra los blueprints (rutas) de la aplicación.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Inicializa la base de datos
    init_db(app)
    
    # Inicializa Flask-Mail
    init_mail(app)
    
    # Registra el blueprint principal
    app.register_blueprint(academic_bp)

    # Manejo del error 413 (Request Entity Too Large)
    @app.errorhandler(413)
    def request_entity_too_large(error):
        flash("El archivo subido es demasiado grande.", "danger")
        return redirect(url_for('academic_bp.registrar_alumno'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config.get("DEBUG", False))
