from database import (
    obtener_numero_alumnos_inscritos,
    obtener_numero_alumnos_egresados,
    obtener_promedios_por_carrera,
)

def generate_statistical_report():
    """
    Genera un reporte estadístico con datos clave para los directivos.
    """
    try:
        total_alumnos = obtener_numero_alumnos_inscritos()  # Esto es un número entero (int)
        total_egresados = obtener_numero_alumnos_egresados()  # Esto también es un número entero
        promedios_carreras = obtener_promedios_por_carrera()  # Esto debería ser un diccionario

        # Si promedios_carreras no es un diccionario, devolver uno vacío
        if not isinstance(promedios_carreras, dict):
            promedios_carreras = {}

        report = {
            "total_alumnos": total_alumnos,
            "total_egresados": total_egresados,
            "promedios_carreras": promedios_carreras
        }

        return report  # <- Asegúrate de retornar SIEMPRE un diccionario

    except Exception as e:
        print(f"Error generando reporte estadístico: {str(e)}")
        return {
            "total_alumnos": 0,
            "total_egresados": 0,
            "promedios_carreras": {}
        }