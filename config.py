import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    """
    Configuración base de la aplicación.
    Define parámetros comunes que se heredan en los distintos entornos.
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = False
    TESTING = False

    # Configuración de la base de datos utilizando PyMySQL
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "default_password")
    DB_NAME = os.getenv("DB_NAME", "default_db")
    DB_PORT = os.getenv("DB_PORT", 3306)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DB_URI", 
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Limitar el tamaño máximo de la solicitud (por ejemplo, para archivos subidos)
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB

    # Configuración de Flask-Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ["true", "1", "yes"]
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

class DevelopmentConfig(Config):
    """
    Configuración para el entorno de desarrollo.
    Activa el modo debug y muestra las consultas SQL.
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """
    Configuración para el entorno de testing.
    Utiliza una base de datos en memoria para pruebas rápidas.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProductionConfig(Config):
    """
    Configuración para el entorno de producción.
    Desactiva el modo debug y no muestra las consultas SQL.
    """
    DEBUG = False
    SQLALCHEMY_ECHO = False

# Diccionario para seleccionar la configuración según el entorno deseado
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
