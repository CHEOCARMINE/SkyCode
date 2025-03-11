from models import Alumno, Carrera, EstadoAlumno

def get_students(
    nombre=None,
    apellido_paterno=None,
    apellido_materno=None,
    matricula=None,
    carrera=None,
    estado=None,
    as_query=False
):
    """
    Si as_query=True, retorna la Query (ORM) para que se maneje la paginación en la ruta.
    Si as_query=False (por defecto), retorna una lista de diccionarios con los datos
    de los alumnos filtrados.
    """
    # Inicia la consulta utilizando el ORM de SQLAlchemy
    query = Alumno.query

    if nombre:
        query = query.filter(Alumno.primer_nombre.ilike(f"%{nombre}%"))
    if apellido_paterno:
        query = query.filter(Alumno.primer_apellido.ilike(f"%{apellido_paterno}%"))
    if apellido_materno:
        query = query.filter(Alumno.segundo_apellido.ilike(f"%{apellido_materno}%"))
    if matricula:
        query = query.filter(Alumno.matricula.ilike(f"%{matricula}%"))
    if carrera:
        query = query.join(Carrera).filter(Carrera.nombre.ilike(f"%{carrera}%"))
    if estado:
        query = query.join(EstadoAlumno).filter(EstadoAlumno.nombre_estado.ilike(f"%{estado}%"))

    # Si se solicita la Query en bruto (para paginar), la retornamos sin ejecutar
    if as_query:
        return query

    # De lo contrario, se obtienen todos los resultados
    alumnos = query.all()

    # Convierte los resultados en una lista de diccionarios para facilitar su uso en la plantilla
    students = []
    for alumno in alumnos:
        student_data = {
            "matricula": alumno.matricula,
            "primer_nombre": alumno.primer_nombre,
            "primer_apellido": alumno.primer_apellido,
            "segundo_apellido": alumno.segundo_apellido,
            "carrera": alumno.carrera.nombre if alumno.carrera else "",
            "estado": alumno.estado.nombre_estado if alumno.estado else ""
        }
        students.append(student_data)
    
    return students
