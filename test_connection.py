import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='bgvv1kdmcr0twofqncy5-mysql.services.clever-cloud.com',
        database='bgvv1kdmcr0twofqncy5',
        user='umlpoc1b4jtwtv1q',
        password='jXI3lPvWdYg5WowmTFBS'
    )
    if connection.is_connected():
        print("Conexión exitosa a la base de datos")
except Error as e:
    print(f"Error al conectar a la base de datos: {e}")
finally:
    if (connection.is_connected()):
        connection.close()
        print("Conexión cerrada")
