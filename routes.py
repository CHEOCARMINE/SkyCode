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