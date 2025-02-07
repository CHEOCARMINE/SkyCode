from database import db

class Alumno(db.Model):
    __tablename__ = 'Alumnos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)  # Deja esta línea como está para mantener la restricción de clave foránea
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    domicilio = db.Column(db.String(200))
    telefono = db.Column(db.String(15))
    correo_electronico = db.Column(db.String(100), unique=True, nullable=False)
    estatus = db.Column(db.String(20))
    carrera = db.Column(db.String(100))

    def __init__(self, usuario_id, matricula, nombre, domicilio, telefono, correo_electronico, estatus, carrera):
        self.usuario_id = usuario_id
        self.matricula = matricula
        self.nombre = nombre
        self.domicilio = domicilio
        self.telefono = telefono
        self.correo_electronico = correo_electronico
        self.estatus = estatus
        self.carrera = carrera
