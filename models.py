from database import db

class Alumno(db.Model):
    __tablename__ = 'alumno'  # Nombre de la tabla actualizado a "alumno"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)  # Mantén la restricción de clave foránea
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    domicilio = db.Column(db.String(200))
    telefono = db.Column(db.String(15))
    correo_electronico = db.Column(db.String(100), unique=True, nullable=False)
    estatus = db.Column(db.String(20))
    carrera = db.Column(db.String(100))
    certificado_preparatoria = db.Column(db.String(255))  # Nuevo campo
    curp = db.Column(db.String(18), nullable=False)  # Nuevo campo
    comprobante_pago = db.Column(db.String(255))  # Nuevo campo

    def __init__(self, usuario_id, matricula, nombre, domicilio, telefono, correo_electronico, estatus, carrera, certificado_preparatoria, curp, comprobante_pago):
        self.usuario_id = usuario_id
        self.matricula = matricula
        self.nombre = nombre
        self.domicilio = domicilio
        self.telefono = telefono
        self.correo_electronico = correo_electronico
        self.estatus = estatus
        self.carrera = carrera
        self.certificado_preparatoria = certificado_preparatoria
        self.curp = curp
        self.comprobante_pago = comprobante_pago

