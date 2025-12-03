# app/__init__.py
from flask import Flask
from app.config import config
# Importamos desde extensiones (NO CREAR AQUÍ)
from app.extensions import db, migrate, ma, cors

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # 1. Configuración
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # 2. Inicializar Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app)
    
    # 3. Registrar Rutas
    try:
        from app.routes.health import health_bp
        app.register_blueprint(health_bp, url_prefix='/api')
        
        from app.routes.pacientes import pacientes_bp
        app.register_blueprint(pacientes_bp, url_prefix='/api/v1')
        
    except Exception as e:
        print(f"⚠️ Error cargando rutas: {e}")

    # ¡¡¡ AQUÍ NO DEBE HABER NADA MÁS !!! 
    # NADA DE app.schemas = ...
    # NADA DE import schemas...
    
    return app