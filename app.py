from flask import Flask, redirect, render_template, request, url_for, flash
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate
from database import db, init_db  # Importar db e init_db desde database.py
from models import Usuario, Alumno, Materia, Horario  # Importar modelos necesarios
from routes import academic_bp, alumno_progress_bp, docentes_bp, reports_bp  # Importar los blueprints
from services import init_mail  # Inicializar el servicio de correo
from functions.auth.login import auth_bp as login_bp  # Blueprint de autenticación
from config import config_by_name  # Configuración de la app

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Inicializa la base de datos
    init_db(app)

    # Inicializa Flask-Mail
    init_mail(app)

    # Inicializa Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirige al login si el usuario no está autenticado

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registra los blueprints
    app.register_blueprint(academic_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(alumno_progress_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(docentes_bp)

    # Configura Flask-Migrate
    migrate = Migrate(app, db)

    # Manejo del error 413 (Request Entity Too Large)
    @app.errorhandler(413)
    def request_entity_too_large(error):
        flash("El archivo subido es demasiado grande.", "danger")
        return redirect(url_for('academic_bp.registrar_alumno'))

    # Ruta de inicio (Login)
    @app.route("/")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("seleccion_materia"))  # Si ya está autenticado, va a selección
        return render_template("login.html")  # Si no, muestra el login

    # Ruta para la selección de materias (solo si está autenticado)
    @app.route("/seleccion")
    @login_required
    def seleccion_materia():
        materias = Materia.query.all()  # Obtener todas las materias
        return render_template("seleccion.html", materias=materias)

    # Ruta para inscribir materias
    @app.route("/inscribir", methods=["POST"])
    @login_required
    def inscribir():
        seleccionadas = request.form.getlist("materias")  # IDs de materias seleccionadas
        materias_seleccionadas = Materia.query.filter(Materia.id.in_(seleccionadas)).all()
        return render_template("resumen.html", seleccionadas=materias_seleccionadas)

    # Ruta para asignar horarios
    @app.route('/asignar_horario', methods=['GET', 'POST'])
    def asignar_horario():
        if request.method == 'POST':
            # Obtener datos del formulario
            crn = request.form['crn']
            hora_inicio = request.form['hora_inicio']
            hora_fin = request.form['hora_fin']
            salon = request.form.get('salon')
            lunes = 'lunes' in request.form
            martes = 'martes' in request.form
            miercoles = 'miercoles' in request.form
            jueves = 'jueves' in request.form
            viernes = 'viernes' in request.form

            # Buscar la materia por CRN
            materia = Materia.query.filter_by(crn=crn).first()
            if not materia:
                flash('Materia no encontrada con el CRN proporcionado.', 'danger')
                return render_template('asignar_horario.html')

            # Crear el objeto Horario
            nuevo_horario = Horario(
                crn=crn,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                salon=salon,
                lunes=lunes,
                martes=martes,
                miercoles=miercoles,
                jueves=jueves,
                viernes=viernes,
                materia=materia
            )

            try:
                db.session.add(nuevo_horario)
                db.session.commit()  # Guardar en la base de datos
                flash(f'Horarios asignados correctamente a la materia {materia.nombre}.', 'success')
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error al asignar horario: {e.__class__.__name__} - {str(e)}")
                flash(f'Error al asignar horarios: {str(e)}', 'danger')

        # Esto siempre debe ocurrir al final, independientemente de si es POST o GET
        return render_template('asignar_horario.html')

    @app.route('/horario')
    def horario():
       return render_template('visualizar_horario.html')




    # Ruta para ver el perfil del usuario
    @app.route('/perfil')
    @login_required
    def perfil():
        usuario = Usuario.query.get(current_user.id)  # Obtener usuario actual
        alumno = Alumno.query.get(usuario.alumno_id) if usuario and usuario.alumno_id else None
        return render_template('perfil.html', usuario=usuario, alumno=alumno)

    return app  # Retorna la app Flask configurada


# Ejecutar la aplicación
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
