from database import db

class Role(db.Model):
    __tablename__ = "Roles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_rol = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Role {self.nombre_rol}>"

class EstadoAlumno(db.Model):
    __tablename__ = "EstadosAlumnos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_estado = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<EstadoAlumno {self.nombre_estado}>"

class Cuatrimestre(db.Model):
    __tablename__ = "Cuatrimestres"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nocuatrimestre = db.Column(db.Integer, unique=True, nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Cuatrimestre {self.nocuatrimestre} - {self.descripcion}>"

class Carrera(db.Model):
    __tablename__ = "Carreras"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    creditos = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Carrera {self.nombre}>"

class Alumno(db.Model):
    __tablename__ = "Alumnos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    curp = db.Column(db.String(18), unique=True)
    domicilio = db.Column(db.String(255))
    telefono = db.Column(db.String(15))
    correo_electronico = db.Column(db.String(100))
    certificado_preparatoria = db.Column(db.LargeBinary)
    comprobante_pago = db.Column(db.LargeBinary)
    estado_id = db.Column(db.Integer, db.ForeignKey("EstadosAlumnos.id"), nullable=False)
    carrera_id = db.Column(db.Integer, db.ForeignKey("Carreras.id"), nullable=False)

    estado = db.relationship("EstadoAlumno", backref="alumnos")
    carrera = db.relationship("Carrera", backref="alumnos")

    def __repr__(self):
        return f"<Alumno {self.nombre}>"

class Usuario(db.Model):
    __tablename__ = "Usuarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contraseña = db.Column(db.String(255), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey("Roles.id"), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    alumno_id = db.Column(db.Integer, db.ForeignKey("Alumnos.id"), unique=True)

    rol = db.relationship("Role", backref="usuarios")
    # Relación uno a uno con Alumno (si corresponde)
    alumno = db.relationship("Alumno", backref=db.backref("usuario", uselist=False))

    def __repr__(self):
        return f"<Usuario ID: {self.id}>"

class Grupo(db.Model):
    __tablename__ = "Grupos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clave = db.Column(db.String(50), nullable=False)
    carrera_id = db.Column(db.Integer, db.ForeignKey("Carreras.id"), nullable=False)

    carrera = db.relationship("Carrera", backref="grupos")

    def __repr__(self):
        return f"<Grupo {self.clave}>"

class GrupoAlumno(db.Model):
    __tablename__ = "Grupo_Alumno"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey("Alumnos.id"), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey("Grupos.id"), nullable=False)

    alumno = db.relationship("Alumno", backref="grupos")
    grupo = db.relationship("Grupo", backref="alumnos")

    def __repr__(self):
        return f"<GrupoAlumno Alumno ID: {self.alumno_id}, Grupo ID: {self.grupo_id}>"

class Materia(db.Model):
    __tablename__ = "Materias"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    crn = db.Column(db.String(50))
    codigo = db.Column(db.String(50))
    creditos = db.Column(db.Integer, nullable=False)
    correlativa_id = db.Column(db.Integer, db.ForeignKey("Materias.id"))

    # Relación auto-referencial para correlativas
    correlativa = db.relationship("Materia", remote_side=[id], backref="materias_correlativas")

    def __repr__(self):
        return f"<Materia {self.nombre}>"

class PlanEstudios(db.Model):
    __tablename__ = "Plan_Estudios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    carrera_id = db.Column(db.Integer, db.ForeignKey("Carreras.id"), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey("Materias.id"), nullable=False)
    cuatrimestre = db.Column(db.Integer, db.ForeignKey("Cuatrimestres.id"), nullable=False)

    carrera = db.relationship("Carrera", backref="plan_estudios")
    materia = db.relationship("Materia", backref="plan_estudios")
    cuatrimestre_obj = db.relationship("Cuatrimestre", backref="plan_estudios")

    def __repr__(self):
        return f"<PlanEstudios Carrera ID: {self.carrera_id}, Materia ID: {self.materia_id}>"

class TipoCargaAcademica(db.Model):
    __tablename__ = "Tipos_Carga_Academica"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<TipoCargaAcademica {self.nombre}>"

class CargaAcademica(db.Model):
    __tablename__ = "Carga_Academica"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey("Alumnos.id"), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey("Materias.id"), nullable=False)
    cuatrimestre = db.Column(db.Integer, db.ForeignKey("Cuatrimestres.id"), nullable=False)
    tipo_carga_id = db.Column(db.Integer, db.ForeignKey("Tipos_Carga_Academica.id"), nullable=False)

    alumno = db.relationship("Alumno", backref="cargas_academicas")
    materia = db.relationship("Materia", backref="cargas_academicas")
    cuatrimestre_obj = db.relationship("Cuatrimestre", backref="cargas_academicas")
    tipo_carga = db.relationship("TipoCargaAcademica", backref="cargas_academicas")

    def __repr__(self):
        return f"<CargaAcademica Alumno ID: {self.alumno_id}, Materia ID: {self.materia_id}>"

class Calificacion(db.Model):
    __tablename__ = "Calificaciones"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey("Alumnos.id"), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey("Materias.id"), nullable=False)
    cuatrimestre = db.Column(db.Integer, db.ForeignKey("Cuatrimestres.id"), nullable=False)
    calificacion = db.Column(db.DECIMAL(3, 1))

    alumno = db.relationship("Alumno", backref="calificaciones")
    materia = db.relationship("Materia", backref="calificaciones")
    cuatrimestre_obj = db.relationship("Cuatrimestre", backref="calificaciones")

    def __repr__(self):
        return f"<Calificacion Alumno ID: {self.alumno_id}, Materia ID: {self.materia_id}, Nota: {self.calificacion}>"

class EvaluacionDocente(db.Model):
    __tablename__ = "EvaluacionesDocentes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey("Alumnos.id"), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey("Materias.id"), nullable=False)
    id_docente = db.Column(db.Integer, db.ForeignKey("Usuarios.id"), nullable=False)
    claridad = db.Column(db.Integer)
    puntualidad = db.Column(db.Integer)
    trato = db.Column(db.Integer)
    disponibilidad = db.Column(db.Integer)
    comentarios = db.Column(db.Text)
    fecha_evaluacion = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    alumno = db.relationship("Alumno", backref="evaluaciones_docentes")
    materia = db.relationship("Materia", backref="evaluaciones_docentes")
    docente = db.relationship("Usuario", backref="evaluaciones_docentes", foreign_keys=[id_docente])

    def __repr__(self):
        return f"<EvaluacionDocente ID: {self.id}>"

class Notificacion(db.Model):
    __tablename__ = "Notificaciones"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey("Alumnos.id"), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    leida = db.Column(db.Boolean, default=False)

    alumno = db.relationship("Alumno", backref="notificaciones")

    def __repr__(self):
        return f"<Notificacion ID: {self.id}>"

class Reporte(db.Model):
    __tablename__ = "Reportes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datos = db.Column(db.JSON)
    fecha_generacion = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    usuario_id = db.Column(db.Integer, db.ForeignKey("Usuarios.id"), nullable=False)

    usuario = db.relationship("Usuario", backref="reportes")

    def __repr__(self):
        return f"<Reporte ID: {self.id}>"
    