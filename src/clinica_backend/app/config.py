# src/app/config.py
# Define configuraciones centralizadas para el comportamiento de Flask y SQLAlchemy.
# Incluye: Seguridad, conexión a BD, comportamiento del Debug, Zona Horaria, Validacion de Entorno
# ORM -> Object Relational Mapping (Mapeo Objeto Relacional) Conectar Bases de Datos Relacionales con Objetos en Código(Python

# `Operative System` -> Permite acceder a Variables de Entorno (Como comunicarse con el Sistema Operativo)
import os 

# `timedelta` -> Maneja diferencias entre fechas y horas
from datetime import timedelta

# Definicion de una Clase Base `Config`
class Config:
    # Encriptar Sesiones, cookies y formularios
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # SQLAlchemy(ORM) -> Configuracion de la Base de Datos
    # Evita que SQLAlchemy consuma recursos innecesarios al rastrear cambios en los objetos del modelo
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Desactiva el log de consultas SQL en la consola

    # JSON
    JSON_SORT_KEYS = False  # Desactiva la ordenación de claves en las respuestas JSON
    JSONIFY_PRETTYPRINT_REGULAR = True  # Habilita la impresión bonita en las respuestas JSON
    
    # Timezone
    TIMEZONE = os.environ.get('TIMEZONE', 'America/Lima')  # Zona horaria predeterminada

    # @staticmethod -> Decorador que convierte un método en estático, no requiere instancia de clase, no necesita acceso a la Clase
    # Se usa si queremos que una función no use ni necesite self
    # No necesita ni `self` ni `cls` como primer argumento
    @staticmethod
    def init_app(app):  # -> Método para inicializar la aplicación con configuraciones específicas
        pass
    
# Hereda de la Clase Base `Config`
# Define la configuracion de produccion de tu aplicacion
class DevelopmentConfig(Config):
    """Configuracion para el Desarrollo Local"""
    
    DEBUG = True  # Habilita el modo de depuración
    TESTING = False# Desactiva el modo de pruebas
    
    # Construir URL desde Variables Individuales
    # `os.environ.get` -> Intenta Obtener el Valor de la variable de Entorno, si no existe usa el valor por defecto
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'clinica_prime')

    # `SQLALCHEMY_DATABASE_URI` -> URI de conexion a la Base de Datos
    # `URI` -> Significa Identificador Uniforme de Recursos
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    # Ver queries SQL en Development
    SQLALCHEMY_ECHO = True  # Habilita el log de consultas SQL en la consola
    
class ProductionConfig(Config):
    """Configuracion para Produccion"""
    
    DEBUG = False  # Desactiva el modo de depuración
    TESTING = False  # Desactiva el modo de pruebas
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # Usa la variable de entorno para la URL de la BD
    
    @staticmethod
    def init_app(app):
        # Validaciones Criticas
        if not os.environ.get('DATABASE_URL'):
            raise ValueError("DATABASE_URL requerido en Produccion")

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}