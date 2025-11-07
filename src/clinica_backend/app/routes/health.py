# src/flask/app/routes/health.py
"""
Endpoints para health checks y status de la API
"""

from flask import Blueprint 
from app.utils.response import success_response
from app import db 

health_bp = Blueprint('health', __name__)

# Health Check Endpoints: 
# Monitorear si API Flask y DB estan corriendo

# Endpoint 1: Health Check de la API
# Util para: 
# - Saber si tu backend esta encendido
# - Verificar un frontend si el servidor esta activo
# - Integracion con Monitorizacion (Docker, Kubernetes, DataDog, etc.)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Verificar que la API esta corriendo
    
    Returns:
        JSON: Estado de salud de la API
    
    Uso:
        GET http://localhost:5000/api/health    
    """

    return success_response(
        data={
            'status': 'healthy',
            'service': "Clinica Prime API",
            'version': '1.0.0'
        }
    )

# Endpoint 2: Health Check de la Base de Datos
# Util para:
# - Verificar que la conexion a la DB esta activa
# - Integracion con Monitorizacion (Docker, Kubernetes, DataDog, etc.)
@health_bp.route('/health/db', methods=['GET'])
def health_check_db():
    """
    Verificar que la base de datos esta corriendo

    Returns:
        JSON: Estado de salud de la base de datos

    Uso:
        GET http://localhost:5000/api/health/db
    """
    try:
        
        # Ejecutar Query simple para verificar conexion
        db.session.execute('SELECT 1')

        return success_response(
            data={
                'status': 'healthy',
                'database': 'connected'
            }
        )
    except Exception as e:
        return success_response(
            data={
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e)
            },
            status_code=503
        ) 