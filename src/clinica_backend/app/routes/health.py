# src/clinica_backend/app/routes/health.py
"""
Endpoints para health checks y status de la API
"""

from flask import Blueprint
# 🔴 ANTES DECÍA: from app.utils.response import success_response (ESTO YA NO EXISTE)
# 🟢 AHORA DEBE DECIR:
from app.utils.response import APIResponse
from app.extensions import db
from sqlalchemy import text

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    # Usamos la nueva clase
    return APIResponse.success(
        data={
            'status': 'healthy',
            'service': "Clinica Prime API",
            'version': '1.0.0'
        }
    )

@health_bp.route('/health/db', methods=['GET'])
def health_check_db():
    try:
        # Ejecutar Query simple
        db.session.execute(text('SELECT 1'))

        return APIResponse.success(
            data={
                'status': 'healthy',
                'database': 'connected'
            }
        )
    except Exception as e:
        # Usamos la nueva clase para errores también
        return APIResponse.error(
            message=str(e),
            status_code=503,
            code="DB_CONNECTION_ERROR"
        )