from flask import Blueprint, jsonify, request, render_template
from models import Alumno, Materia, Calificacion, db

routes = Blueprint('routes', __name__)

@routes.route('/materias_pendientes')
def materias_pendientes():
    return render_template('materias_pendientes.html', materias_reprobadas=materias_reprobadas, materias_faltantes=materias_faltantes, materias_sugeridas=materias_sugeridas)

@routes.route('/validar_carga', methods=['GET', 'POST'])
def validar_carga():
    return render_template('validar_carga.html')
