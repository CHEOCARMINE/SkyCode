from models import Coordinadores_Directivos, Usuario

def get_coordinadores_directivos(
    nombre=None,
    apellido=None,
    matricula=None,
    rol=None,
    estado=None,
    as_query=False
):
    """
    Retorna Coordinadores/Directivos filtrados.

    Parámetros:
      - nombre: Filtra por 'primer_nombre' (contiene).
      - apellido: Filtra por 'primer_apellido' (contiene).
      - matricula: Filtra por 'matricula' (contiene).
      - rol: Filtra por el rol del usuario (valor numérico, ej. 2 para coordinador, 3 para directivo).
      - estado: Filtra por el estado de la cuenta ("1" para activo, "0" para inactivo).
      - as_query: Si es True, retorna la Query (ORM) sin ejecutar (útil para paginación).

    Retorna:
      - Si as_query es False (por defecto): una lista de diccionarios con los datos.
    """
    # Inicia la consulta realizando join entre Coordinadores_Directivos y Usuario.
    query = Coordinadores_Directivos.query.join(
        Usuario, Usuario.coordinador_directivo_id == Coordinadores_Directivos.id
    )

    if nombre:
        query = query.filter(Coordinadores_Directivos.primer_nombre.ilike(f"%{nombre}%"))
    if apellido:
        query = query.filter(Coordinadores_Directivos.primer_apellido.ilike(f"%{apellido}%"))
    if matricula:
        query = query.filter(Coordinadores_Directivos.matricula.ilike(f"%{matricula}%"))
    if rol is not None:
        query = query.filter(Usuario.rol_id == rol)
    if estado is not None and estado != "":
        # Convertir estado: '1' a True, '0' a False
        estado_bool = True if str(estado) == "1" else False
        query = query.filter(Usuario.activo == estado_bool)

    if as_query:
        return query

    registros = query.all()
    coordinadores = []
    for registro in registros:
        data = {
            "id": registro.id,
            "matricula": registro.matricula,
            "primer_nombre": registro.primer_nombre,
            "primer_apellido": registro.primer_apellido,
            "rol": registro.usuario.rol_id if registro.usuario else None,
            "estado": registro.usuario.activo if registro.usuario else None
        }
        coordinadores.append(data)
    
    return coordinadores
