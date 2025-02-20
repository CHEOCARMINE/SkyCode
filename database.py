import mysql.connector

# ✅ Configuración de conexión a la base de datos
db_config = {
    'host': 'bgvv1kdmcr0twofqncy5-mysql.services.clever-cloud.com',
    'user': 'umlpoc1b4jtwtv1q',
    'password': 'jXI3lPvWdYg5WowmTFBS',
    'database': 'bgvv1kdmcr0twofqncy5'
}

# ✅ Función para obtener la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(**db_config)


def test_connection():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT 1")  # Consulta de prueba
        print("✅ Conexión exitosa a la base de datos.")
        db.close()
    except Exception as e:
        print(f"❌ Error de conexión a la BD: {e}")
