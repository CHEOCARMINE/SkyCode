# routes.py
from flask import Blueprint, render_template, redirect, url_for

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return redirect(url_for('routes.login'))  # Redirige a la página de login

@routes.route('/login')
def login():
    return render_template('login.html')  # Renderiza el archivo login.html

@routes.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Ajusta si el nombre del HTML es diferente

@routes.route('/base')
def base():
    return render_template('base.html')  # Ajusta si el nombre del HTML es diferente

@routes.route('/inscripcion_materias')
def seleccion_materias():
    return render_template('inscripcion_materias.html')  # Asegúrate de que este archivo exista en /templates



@routes.route('/perfil')
def perfil():
    return render_template('perfil.html')  # Renderiza el archivo perfil.html
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from functions.auth.register import registrar_alumno as process_registration

academic_bp = Blueprint('academic_bp', __name__)

@academic_bp.route('/', endpoint='index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('index.html')

@academic_bp.route('/register', methods=['GET', 'POST'])
@login_required
def registrar_alumno():
    # Suponiendo que en tu base de datos:
    # 1 = Alumno, 2 = Coordinador, 3 = Directivo
    if current_user.rol_id != 2:
        flash("No tienes permisos para registrar alumnos", "danger")
        return redirect(url_for('academic_bp.index'))
    return process_registration()