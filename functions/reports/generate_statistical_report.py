from database import get_db_connection

def generate_statistical_report():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # 🏫 Obtener el total de alumnos inscritos
        cursor.execute("SELECT COUNT(*) AS total FROM Alumnos")
        total_inscritos = cursor.fetchone()
        total_inscritos = total_inscritos["total"] if total_inscritos else 0

        # 🎓 Obtener el total de egresados
        cursor.execute("SELECT COUNT(*) AS total FROM Alumnos WHERE estado = 'Egresado'")
        total_egresados = cursor.fetchone()
        total_egresados = total_egresados["total"] if total_egresados else 0

        # 📊 Obtener el promedio global por carrera
        cursor.execute("""
            SELECT carrera, COALESCE(AVG(promedio), 0) AS promedio_global
            FROM Alumnos
            GROUP BY carrera
        """)
        promedios_carreras = cursor.fetchall()

        # Calcular el promedio general de todas las carreras
        promedio_global = sum(c["promedio_global"] for c in promedios_carreras) / len(promedios_carreras) if promedios_carreras else 0
        promedio_global = round(promedio_global, 2)  # Redondear a 2 decimales

        return {
            "total_inscritos": total_inscritos,
            "total_egresados": total_egresados,
            "promedio_global": promedio_global,
            "promedios_carreras": promedios_carreras
        }

    except Exception as e:
        print(f"❌ Error al obtener estadísticas generales: {e}")
        return {
            "total_inscritos": 0,
            "total_egresados": 0,
            "promedio_global": 0,
            "promedios_carreras": []
        }

    finally:
        if db.is_connected():
            cursor.close()
            db.close()
