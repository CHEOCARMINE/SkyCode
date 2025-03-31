from models import Docente

def get_docentes(
    nombre=None,
    primer_apellido=None,
    segundo_apellido=None,
    matricula=None,
    as_query=False
):
    """
    Si as_query=True, retorna la Query (ORM) para manejar la paginación.
    Si as_query=False, retorna una lista de diccionarios con los datos
    de los docentes filtrados.
    """
    query = Docente.query

    # Aplicar filtros dinámicamente
    if nombre:
        query = query.filter(Docente.nombre.ilike(f"%{nombre}%"))
    if primer_apellido:
        query = query.filter(Docente.primer_apellido.ilike(f"%{primer_apellido}%"))
    if segundo_apellido:
        query = query.filter(Docente.segundo_apellido.ilike(f"%{segundo_apellido}%"))
    if matricula:
        query = query.filter(Docente.matricula.ilike(f"%{matricula}%"))

    # Retornar la query para paginación o ejecutarla
    if as_query:
        return query

    docentes = query.all()
    return [
        {
            "matricula": docente.matricula,
            "nombre": docente.nombre,
            "primer_apellido": docente.primer_apellido,
            "segundo_apellido": docente.segundo_apellido,
            "correo_electronico": docente.correo_electronico
        }
        for docente in docentes
    ]
