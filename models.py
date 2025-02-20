from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Alumno(db.Model):
    __tablename__ = 'alumnos'

    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    direccion = db.Column(db.String(200), nullable=True)
    telefono = db.Column(db.String(15), nullable=True)
    documento_certificado = db.Column(db.String(255), nullable=True)  # Ruta del archivo
    documento_pago = db.Column(db.String(255), nullable=True)         # Ruta del archivo
    curp = db.Column(db.String(18), nullable=False)  # Nuevo campo para CURP

    def __init__(self, matricula, nombre, correo, fecha_nacimiento, direccion, telefono, documento_certificado, documento_pago, curp):
        self.matricula = matricula
        self.nombre = nombre
        self.correo = correo
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.telefono = telefono
        self.documento_certificado = documento_certificado
        self.documento_pago = documento_pago
        self.curp = curp  # Guardamos el CURP





class Materia(db.Model):
    __tablename__ = 'Materias'
    id = db.Column(db.Integer, primary_key=True)
    crn = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

