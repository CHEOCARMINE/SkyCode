from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user
from models import db, Usuario, Alumno, Coordinadores_Directivos

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        password = request.form.get('password')

        # Verificar si la matrícula pertenece a un alumno o a un coordinador/directivo
        if matricula.startswith('ALU'):
            alumno = Alumno.query.filter_by(matricula=matricula).first()
            if not alumno:
                flash('Matrícula no registrada como alumno', 'login-danger')
                return redirect(url_for('auth.login'))
            user = Usuario.query.filter_by(alumno_id=alumno.id).first()
        elif matricula.startswith('COO') or matricula.startswith('DIR'):
            cd = Coordinadores_Directivos.query.filter_by(matricula=matricula).first()
            if not cd:
                flash('Matrícula no registrada como coordinador/directivo', 'login-danger')
                return redirect(url_for('auth.login'))
            user = Usuario.query.filter_by(coordinador_directivo_id=cd.id).first()
        else:
            flash('Usuario no existe: formato de matrícula no reconocido', 'login-danger')
            return redirect(url_for('auth.login'))

        if not user:
            flash('Usuario no existe', 'login-danger')
            return redirect(url_for('auth.login'))

        # Verificar la contraseña
        if bcrypt.check_password_hash(user.contraseña, password):
            login_user(user)
            flash('Inicio de sesión exitoso', 'login-success')
            # Redirigir a la página principal (index) que es común para todos los roles
            return redirect(url_for('academic_bp.index'))
        else:
            flash('Contraseña incorrecta', 'login-danger')
            return redirect(url_for('auth.login'))

    # Método GET: se muestra el formulario de login
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión', 'login-success')
    return redirect(url_for('auth.login'))
