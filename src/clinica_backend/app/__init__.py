# src/app/__init__.py 

"""
APPLICATION FACTORY PATTERN
- Crea y configura la Aplicacion Flask
- Permite crear multiples instancias de la aplicacion con diferentes configuraciones
- Mejora la modularidad y escalabilidad de la aplicacion
- Facilita las pruebas unitarias y de integracion
"""

# `__init___.py` ->  Se utiliza para convertir un directorio en un paquete de Python
## - Cualquier carpeta que tenga un __init__.py es reconocida como importable: puedes hacer `from package import module`

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS


#===========================================================================
# INSTANCIAS GLOBALES
# - Instancias de extensiones que se utilizarán en toda la aplicación
# - Se crean aquí para evitar problemas de importación circular
#===========================================================================    

db = SQLAlchemy()          # ORM para manejar la base de datos
migrate = Migrate()        # Manejo de migraciones de la base de datos
ma = Marshmallow()         # Serialización y deserialización de objetos

# CORS -> Cross-Origin Resource Sharing (Compartición de Recursos de Origen Cruzado)
# - Permite que los recursos restringidos en una página web sean solicitados desde otro dominio
cors = CORS()              # Manejo de CORS para permitir solicitudes desde diferentes orígenes

def create_app(config_name = 'default'):
    """
    Factory que crea la Aplicacion Flask
    
    Args:
        config_name (str): 'development', 'production', 'default'
        
    Returns:
        Flask: Instancia Configurada

    Por que una funcion y no `app = Flask(__name__)` directamente?
    
    1. TESTING: Puedes crear apps con configs diferentes
    2. MODULARIDAD: Todo se configura en un solo lugar
    3. EXTENSIONES: Se inicializan de Forma Controlada
    """
    # ================================================================
    # PASO 1: Crear Instancia Base
    # ================================================================
    app = Flask(__name__)
    
    # ================================================================
    # PASO 2: Cargar Configuracion
    # ================================================================
    from app.config import config
    # `from_object` -> Metodo de Flask usa para copiar las varibales  que estan dentro de un objeto de Python
    app.config.from_object(config[config_name])  # Cargar config segun el entorno
    config[config_name].init_app(app)            # Configuracion Especifica
    
    # ================================================================
    # PASO 3: Inicializar Extensiones
    # ================================================================
    # `.init_app(app)` -> Funcion Estatica Definida dentro de la Clase configuracion
    db.init_app(app)       # Inicializar SQLAlchemy con la app
    migrate.init_app(app, db)  # Inicializar Flask-Migrate con la app y la BD
    ma.init_app(app)       # Inicializar Marshmallow con la app
    cors.init_app(app)     # Inicializar CORS con la app
    
    # ================================================================
    # PASO 4: Registrar Blueprints
    # ================================================================
    from app.routes.health import health_bp
    # from app.routes.pacientes import pacientes_bp
    # from app.routes.inventario import inventario_bp
    
    app.register_blueprint(health_bp, url_prefix='/api')
    # app.register_blueprint(pacientes_bp, url_prefix='/api/v1')
    # app.register_blueprint(inventario_bp, url_prefix='/api/v1')
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PASO 5: Error handlers globales
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    @app.errorhandler(404)
    def not_found(error):
        return {
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Endpoint no encontrado'
            }
        }, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Rollback en caso de error
        return {
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Error interno del servidor'
            }
        }, 500
    
    return app
