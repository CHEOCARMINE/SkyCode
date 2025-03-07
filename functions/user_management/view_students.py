from models import Alumno

def get_students(nombre=None, apellido=None, segundo_apellido=None, matricula=None):
    """
    Retorna una lista de diccionarios con los datos de los alumnos filtrados por
    nombre, apellido paterno, apellido materno o matrícula. Si no se especifica algún filtro, se retornan todos los alumnos.
    """
    # Inicia la consulta utilizando el ORM de SQLAlchemy
    query = Alumno.query

    if nombre:
        query = query.filter(Alumno.primer_nombre.ilike(f"%{nombre}%"))
    if apellido:
        query = query.filter(Alumno.primer_apellido.ilike(f"%{apellido}%"))
    if segundo_apellido:
        query = query.filter(Alumno.segundo_apellido.ilike(f"%{segundo_apellido}%"))
    if matricula:
        query = query.filter(Alumno.matricula.ilike(f"%{matricula}%"))
    
    alumnos = query.all()

    # Convierte los resultados en una lista de diccionarios para facilitar su uso en la plantilla
    students = []
    for alumno in alumnos:
        student_data = {
            "matricula": alumno.matricula,
            "primer_nombre": alumno.primer_nombre,
            "primer_apellido": alumno.primer_apellido,
            "segundo_apellido": alumno.segundo_apellido
        }
        students.append(student_data)
    
    return students
