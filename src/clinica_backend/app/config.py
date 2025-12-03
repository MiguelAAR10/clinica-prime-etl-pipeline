# src/app/config.py
import os # Librería para hablar con el Sistema Operativo (Windows/Linux)

class Config:
    """
    CONFIGURACIÓN BASE (El Padre)
    Aquí ponemos lo que es común para TODOS los entornos.
    """
    
    # 1. LA LLAVE MAESTRA (Seguridad)
    # Flask usa esto para firmar cookies y proteger datos.
    # Le decimos: "Busca en Windows la clave 'SECRET_KEY', si no la encuentras, usa 'dev-key-insegura'"
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-insegura-por-defecto')

    # 2. OPTIMIZACIÓN DE MEMORIA
    # SQLAlchemy por defecto gasta mucha memoria rastreando cada cambio pequeño.
    # Lo apagamos porque no lo necesitamos (ahorramos recursos).
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 3. ESTÉTICA DE RESPUESTAS
    # Hace que el JSON se vea bonito y ordenado en el navegador, no todo apretado en una línea.
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # 4. ZONA HORARIA
    TIMEZONE = os.environ.get('TIMEZONE', 'America/Lima')

    # Un método vacío (Hook). A veces se usa para ejecutar código al iniciar.
    # @staticmethod significa que no necesitas crear una instancia de Config para usarlo.
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    ENTORNO DE DESARROLLO (Tu Laptop)
    Hereda de 'Config' (tiene todo lo de arriba) + cosas nuevas.
    """
    # Modo Debug: Si hay error, te muestra la pantalla interactiva con el código.
    DEBUG = True
    TESTING = False
    
    # SQL Echo: Muestra en la consola cada comando SQL que se ejecuta.
    # Vital para aprender y ver qué está haciendo tu base de datos realmente.
    SQLALCHEMY_ECHO = True 

    # CONSTRUCCIÓN DE LA URL DE LA BASE DE DATOS (Connection String)
    # Es como la dirección de casa: Protocolo://Usuario:Password@Direccion:Puerto/NombreCasa
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'clinica_prime')

    # La URL final que usa SQLAlchemy para conectarse
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class ProductionConfig(Config):
    """
    ENTORNO DE PRODUCCIÓN (El Mundo Real - AWS/Nube)
    """
    DEBUG = False   # ¡JAMÁS actives debug en producción! (Muestra agujeros de seguridad)
    TESTING = False
    SQLALCHEMY_ECHO = False # No queremos ensuciar los logs con millones de queries
    
    # En la nube, la URL de la base de datos suele venir en una sola variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    @classmethod
    def init_app(cls, app):
        # Esta función corre justo antes de arrancar en Producción.
        Config.init_app(app)
        
        # FAIL FAST (Falla Rápido)
        # Es mejor que la app NO arranque a que arranque insegura.
        # Verificamos que existan las claves críticas.
        assert os.environ.get('SECRET_KEY'), "¡CRÍTICO! Falta SECRET_KEY en Producción"
        assert os.environ.get('DATABASE_URL'), "¡CRÍTICO! Falta DATABASE_URL en Producción"

# Diccionario para elegir fácil qué configuración usar en 'run.py'
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}