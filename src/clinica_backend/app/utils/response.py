from flask import jsonify

"""
MODULO DE RESPUESTAS ESTANDARIZADAS (Patrón Facade para Respuestas HTTP)

¿POR QUÉ HACEMOS ESTO?
Imagina que tienes 50 endpoints. Si en cada uno escribes manualmente el JSON:
- En uno pondrás "mensaje", en otro "message", en otro "msg".
- El Frontend se volverá loco intentando adivinar qué llave leer.

SOLUCIÓN:
Creamos una "Fachada" (Facade). Todos los endpoints llaman a estas funciones.
Si mañana queremos cambiar el formato de TODA la API, solo cambiamos este archivo.
"""

class APIResponse:
    """
    Clase estática para agrupar los métodos de respuesta.
    No necesita instanciarse (no usamos `self`).
    """

    @staticmethod
    def success(data=None, message="Successful operation", status_code=200):
        """
        Respuesta estándar para casos de ÉXITO (200, 201).
        
        Estructura JSON resultante:
        {
            "success": true,
            "message": "Operación exitosa",
            "data": { ... datos ... }
        }
        
        Args:
            data (dict/list): Los datos reales (pacientes, facturas, etc.)
            message (str): Mensaje legible para el usuario final.
            status_code (int): 200 (OK) o 201 (Created).
        """
        response_structure = {
            "success": True,
            "message": message,
            "data": data
        }
        # jsonify: Convierte el diccionario de Python a String JSON compatible con HTTP
        return jsonify(response_structure), status_code

    @staticmethod
    def error(message, status_code=400, code="GENERIC_ERROR", details=None):
        """
        Respuesta estándar para ERRORES (400, 404, 500).
        
        Estructura JSON resultante:
        {
            "success": false,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "El DNI es inválido",
                "details": ["Campo requerido", "Debe ser numérico"]
            }
        }

        Args:
            message (str): Descripción del error.
            status_code (int): HTTP Status (400 Bad Request, 404 Not Found, etc.)
            code (str): Código interno para el desarrollador (ej: 'USER_NOT_FOUND').
            details (list/dict): Opcional. Errores específicos de validación.
        """
        error_structure = {
            "code": code,
            "message": message
        }
        
        # Solo agregamos 'details' si existen, para no ensuciar el JSON
        if details:
            error_structure["details"] = details

        response_structure = {
            "success": False,
            "error": error_structure
        }
        
        return jsonify(response_structure), status_code