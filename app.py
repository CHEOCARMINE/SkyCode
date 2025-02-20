from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import pymysql
from models import db, Alumno, Materia  # Importar modelos
from routes import routes
# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
pymysql.install_as_MySQLdb()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI').replace("mysql://", "mysql+pymysql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para evitar advertencias

# Inicializar SQLAlchemy con la aplicación Flask
db.init_app(app)

# Ruta para obtener el nombre de la materia basado en el CRN
@app.route('/getMateria', methods=['POST'])
def get_materia():
    crn = request.form.get('crn')
    if crn:
        materia = Materia.query.filter_by(crn=crn).first()
        if materia:
            return materia.nombre  # Retorna el nombre de la materia en texto plano
        else:
            return "CRN no encontrado"
    return "CRN no proporcionado"

# Registrar otras rutas y funcionalidades
@app.route('/registrar_alumno')
def base():
    return render_template('base.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        fecha_nacimiento = datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d')
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        matricula = generar_matricula()

        documento_certificado = request.files['certificado']
        documento_curp = request.files['curp']
        documento_pago = request.files['comprobante_pago']

        certificado_path = curp_path = pago_path = None

        if documento_certificado and allowed_file(documento_certificado.filename):
            certificado_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(documento_certificado.filename))
            documento_certificado.save(certificado_path)

        if documento_curp and allowed_file(documento_curp.filename):
            curp_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(documento_curp.filename))
            documento_curp.save(curp_path)

        if documento_pago and allowed_file(documento_pago.filename):
            pago_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(documento_pago.filename))
            documento_pago.save(pago_path)

        nuevo_alumno = Alumno(
            matricula=matricula,
            nombre=nombre,
            correo=correo,
            fecha_nacimiento=fecha_nacimiento,
            direccion=direccion,
            telefono=telefono,
            documento_certificado=certificado_path,
            documento_curp=curp_path,
            documento_pago=pago_path
        )

        try:
            db.session.add(nuevo_alumno)
            db.session.commit()
            return redirect(url_for('exito'))
        except:
            db.session.rollback()
            return 'Hubo un problema al guardar el alumno.'

    return render_template('registro.html')

# Registrar el blueprint de rutas
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)

