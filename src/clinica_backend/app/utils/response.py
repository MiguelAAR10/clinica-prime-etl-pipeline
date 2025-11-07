# src/app/utils/response.py
"""
Helper para estandarizar respuestas JSON de la API
"""

from flask import jsonify

def success_response(data=None, message=None, status_code=200):
    """
    Respuesta exitosa estandarizada
    
    Args:
        data: Datos a retornar
        message: Mensaje opcional
        status_code: Código HTTP (default 200)
    
    Returns:
        tuple: (response, status_code)
    
    Ejemplo:
        return success_response(
            data={'id': 123, 'nombre': 'Juan'},
            message='Paciente creado',
            status_code=201
        )
    """
    response = {'success': True}
    
    if data is not None:
        response['data'] = data
    
    if message:
        response['message'] = message
    
    return jsonify(response), status_code


def error_response(code, message, details=None, status_code=400):
    """
    Respuesta de error estandarizada
    
    Args:
        code: Código de error (ej: 'VALIDATION_ERROR')
        message: Mensaje descriptivo
        details: Detalles adicionales (opcional)
        status_code: Código HTTP (default 400)
    
    Returns:
        tuple: (response, status_code)
    
    Ejemplo:
        return error_response(
            code='NOT_FOUND',
            message='Paciente no encontrado',
            status_code=404
        )
    """
    response = {
        'success': False,
        'error': {
            'code': code,
            'message': message
        }
    }
    
    if details:
        response['error']['details'] = details
    
    return jsonify(response), status_code