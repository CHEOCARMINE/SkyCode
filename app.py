from flask import Flask, render_template
from database import init_db, db
from models import Alumno  # Asegúrate de importar el modelo Alumno
from functions.user_management.manage_students import manage_students

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://umlpoc1b4jtwtv1q:jXI3lPvWdYg5WowmTFBS@bgvv1kdmcr0twofqncy5-mysql.services.clever-cloud.com:3306/bgvv1kdmcr0twofqncy5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sKqSKYZJRHSz3AF'  # O usa os.getenv('SECRET_KEY') si está en tu archivo .env

# Inicializar base de datos
init_db(app)

# Registrar las rutas del CRUD de alumnos
app.register_blueprint(manage_students)

@app.route('/')
def index():
    alumnos = Alumno.query.all()
    return render_template('index.html', alumnos=alumnos)

@app.route('/agregar_alumno')
def agregar_alumno():
    return render_template('add_student.html')

if __name__ == '__main__':
    app.run(debug=True)