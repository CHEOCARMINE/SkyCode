from flask import Blueprint, render_template
from functions.auth.register import registrar_alumno as process_registration

academic_bp = Blueprint('academic_bp', __name__)

@academic_bp.route('/', endpoint='index')
def index():
    return render_template('index.html')

@academic_bp.route('/register', methods=['GET', 'POST'])
def registrar_alumno():
    return process_registration()