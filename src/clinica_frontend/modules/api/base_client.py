# src/clinica_frontend/modules/api/base_client.py
"""
Cliente HTTP base para comunicación con Backend Flask.

Arquitectura:
- Herencia: Todos los clientes específicos heredan de BaseAPIClient
- DRY: Manejo de errores centralizado
- Logging: Entrada/Salida completa para debugging
- Validación: Endpoints seguros
- Consistencia: Respuestas siempre normalizadas

Autor: MediStock Team
Versión: 2.0
"""

import requests
from typing import Dict, Any, Optional
import logging
from clinica_frontend.config import Config

# Configurar logger
logger = logging.getLogger(__name__)


class BaseAPIClient:
    """
    Cliente HTTP genérico para comunicación con Backend.
    
    Responsabilidades:
    1. Ejecutar peticiones HTTP (GET, POST, PUT, DELETE)
    2. Manejar errores de red de forma centralizada
    3. Normalizar respuestas del servidor
    4. Loguear todas las operaciones
    5. Validar parámetros de entrada
    
    Uso:
        # Heredar en clientes específicos
        class PacientesAPI(BaseAPIClient):
            def get_lista(self):
                return self.get("/pacientes")
    """

    def __init__(self):
        """
        Inicializa cliente HTTP con configuración desde Config.
        
        Crea una sesión HTTP reutilizable (mejor performance que
        requests individuales) y configura headers por defecto.
        """
        self.base_url = Config.API_BASE_URL
        self.timeout = Config.API_TIMEOUT
        
        # Session reutiliza conexión TCP (HTTP Keep-Alive)
        self.session = requests.Session()
        
        # Headers por defecto para todas las peticiones
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "MediStock-Frontend/1.0"
        })

    # ═══════════════════════════════════════════════════════
    # MÉTODOS PRIVADOS (CORE LOGIC)
    # ═══════════════════════════════════════════════════════

    def _validate_endpoint(self, endpoint: str) -> None:
        """
        Valida que el endpoint sea seguro y correcto.
        
        Previene errores comunes:
        - Endpoint None o vacío
        - Endpoint sin "/" inicial
        - Endpoint no-string
        
        Args:
            endpoint: Ruta del endpoint (debe empezar con /)
            
        Raises:
            ValueError: Si el endpoint es inválido
            
        Ejemplos:
            ✅ "/pacientes"
            ✅ "/inventario/productos"
            ❌ "pacientes" (sin /)
            ❌ None
            ❌ ""
        """
        if not endpoint or not isinstance(endpoint, str):
            raise ValueError(
                f"Endpoint debe ser un string no-vacío. "
                f"Recibido: {repr(endpoint)}"
            )
        
        if not endpoint.startswith("/"):
            raise ValueError(
                f"Endpoint debe iniciar con '/'. "
                f"Recibido: {endpoint}"
            )

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Procesa respuesta HTTP y normaliza salida.
        
        Garantiza estructura consistente:
        {
            "success": bool,           # Siempre presente
            "status_code": int,        # Siempre presente
            "data": Any,               # Si success=True
            "error": {                 # Si success=False
                "message": str,
                "type": str
            }
        }
        
        Args:
            response: Objeto Response de requests
            
        Returns:
            Diccionario normalizado
            
        Casos manejados:
        1. Respuesta JSON válida (dict)
        2. Respuesta JSON válida (list)
        3. Respuesta no-JSON (HTML, texto plano)
        """
        # Intentar parsear JSON
        try:
            data = response.json()
        except ValueError:
            # Backend devolvió HTML o texto plano (error 500, etc.)
            logger.warning(
                f"Respuesta no-JSON. Status: {response.status_code}. "
                f"Body: {response.text[:200]}"
            )
            return {
                "success": False,
                "status_code": response.status_code,
                "error": {
                    "message": "Respuesta inválida del servidor (No JSON)",
                    "type": "invalid_response"
                }
            }

        # Normalización: Envolver siempre en estructura estándar
        # Si el backend ya devuelve un envelope con "success" y "data", lo usamos.
        if isinstance(data, dict) and "success" in data and "data" in data:
            if "status_code" not in data:
                data["status_code"] = response.status_code
            return data

        # Si es una respuesta cruda (dict o list), la envolvemos
        return {
            "success": response.ok,
            "status_code": response.status_code,
            "data": data
        }

    def _handle_error(
        self,
        endpoint: str,
        method: str,
        exception: Exception
    ) -> Dict[str, Any]:
        """
        Centraliza el manejo de excepciones (DRY).
        
        Diferencia tipos de error para dar feedback específico:
        - Timeout: Servidor lento
        - ConnectionError: Servidor apagado/red caída
        - HTTPError: Error 4xx/5xx
        - Otros: Errores inesperados
        
        Args:
            endpoint: Ruta del endpoint
            method: Método HTTP (GET, POST, etc.)
            exception: Excepción capturada
            
        Returns:
            Diccionario con error normalizado
            
        Estructura de salida:
        {
            "success": False,
            "error": {
                "message": str,  # Mensaje user-friendly
                "type": str      # Tipo para lógica en frontend
            }
        }
        """
        if isinstance(exception, requests.exceptions.Timeout):
            logger.warning(f"TIMEOUT en {method} {endpoint}")
            return {
                "success": False,
                "error": {
                    "message": "El servidor tardó demasiado en responder",
                    "type": "timeout"
                }
            }
        
        elif isinstance(exception, requests.exceptions.ConnectionError):
            logger.error(f"CONNECTION ERROR en {method} {endpoint}")
            return {
                "success": False,
                "error": {
                    "message": "No se puede conectar al servidor",
                    "type": "connection"
                }
            }
        
        elif isinstance(exception, requests.exceptions.HTTPError):
            logger.error(f"HTTP ERROR en {method} {endpoint}: {exception}")
            return {
                "success": False,
                "error": {
                    "message": f"Error HTTP: {exception}",
                    "type": "http_error"
                }
            }
        
        else:
            # Error inesperado (bug en código, etc.)
            logger.exception(f"ERROR CRÍTICO en {method} {endpoint}")
            return {
                "success": False,
                "error": {
                    "message": str(exception),
                    "type": "unknown"
                }
            }

    # ═══════════════════════════════════════════════════════
    # MÉTODOS PÚBLICOS (HTTP VERBS)
    # ═══════════════════════════════════════════════════════

    def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Realiza petición GET.
        
        Uso típico: Obtener recursos (lista o detalle)
        
        Args:
            endpoint: Ruta del endpoint (ej: "/pacientes")
            params: Parámetros query (ej: {"limit": 10, "offset": 0})
            
        Returns:
            {
                "success": bool,
                "data": [...] o {...},
                "error": {...}  # Solo si success=False
            }
            
        Ejemplo:
            result = client.get("/pacientes", params={"limit": 50})
            if result["success"]:
                pacientes = result["data"]
        """
        self._validate_endpoint(endpoint)
        
        try:
            url = f"{self.base_url}{endpoint}"
            logger.debug(f"GET {endpoint} | Params: {params}")
            
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout
            )
            
            logger.debug(f"GET {endpoint} -> {response.status_code}")
            return self._handle_response(response)
        
        except Exception as e:
            return self._handle_error(endpoint, "GET", e)

    def post(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        """
        Realiza petición POST.
        
        Uso típico: Crear recursos
        
        Args:
            endpoint: Ruta del endpoint (ej: "/pacientes")
            data: Datos a enviar en JSON
            
        Returns:
            {
                "success": bool,
                "data": {...},  # Recurso creado
                "error": {...}  # Solo si success=False
            }
            
        Ejemplo:
            result = client.post("/pacientes", {
                "dni": "12345678",
                "nombreCompleto": "Juan Pérez"
            })
            if result["success"]:
                nuevo_paciente = result["data"]
        
        Nota:
            No logueamos 'data' por seguridad (puede contener
            contraseñas, tokens, etc.)
        """
        self._validate_endpoint(endpoint)
        
        try:
            url = f"{self.base_url}{endpoint}"
            logger.debug(f"POST {endpoint}")  # Sin data por seguridad
            
            response = self.session.post(
                url,
                json=data,
                timeout=self.timeout
            )
            
            logger.debug(f"POST {endpoint} -> {response.status_code}")
            return self._handle_response(response)
        
        except Exception as e:
            return self._handle_error(endpoint, "POST", e)

    def put(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        """
        Realiza petición PUT.
        
        Uso típico: Actualizar recursos completos
        
        Args:
            endpoint: Ruta del endpoint (ej: "/pacientes/123")
            data: Datos a actualizar
            
        Returns:
            {
                "success": bool,
                "data": {...},  # Recurso actualizado
                "error": {...}  # Solo si success=False
            }
            
        Ejemplo:
            result = client.put("/pacientes/123", {
                "telefono": "987654321"
            })
            if result["success"]:
                paciente_actualizado = result["data"]
        """
        self._validate_endpoint(endpoint)
        
        try:
            url = f"{self.base_url}{endpoint}"
            logger.debug(f"PUT {endpoint}")
            
            response = self.session.put(
                url,
                json=data,
                timeout=self.timeout
            )
            
            logger.debug(f"PUT {endpoint} -> {response.status_code}")
            return self._handle_response(response)
        
        except Exception as e:
            return self._handle_error(endpoint, "PUT", e)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Realiza petición DELETE.
        
        Uso típico: Eliminar recursos
        
        Args:
            endpoint: Ruta del endpoint (ej: "/pacientes/123")
            
        Returns:
            {
                "success": bool,
                "message": str,  # Confirmación
                "error": {...}   # Solo si success=False
            }
            
        Ejemplo:
            result = client.delete("/pacientes/123")
            if result["success"]:
                st.success("Paciente eliminado")
        """
        self._validate_endpoint(endpoint)
        
        try:
            url = f"{self.base_url}{endpoint}"
            logger.debug(f"DELETE {endpoint}")
            
            response = self.session.delete(
                url,
                timeout=self.timeout
            )
            
            logger.debug(f"DELETE {endpoint} -> {response.status_code}")
            return self._handle_response(response)
        
        except Exception as e:
            return self._handle_error(endpoint, "DELETE", e)


# ═══════════════════════════════════════════════════════════
# FUNCIÓN HELPER PÚBLICA
# ═══════════════════════════════════════════════════════════

def health_check() -> Dict[str, Any]:
    """
    Verifica conectividad con el Backend.
    
    Se usa en app.py al inicio para validar que el servidor
    Flask está corriendo y responde correctamente.
    
    Returns:
        {
            "success": bool,
            "message": str  # Mensaje user-friendly
        }
        
    Ejemplo de uso en app.py:
        health = health_check()
        if not health["success"]:
            st.error(health["message"])
            st.stop()
    
    Nota:
        Usa el método get() de BaseAPIClient para reutilizar
        toda la lógica de manejo de errores (DRY).
    """
    try:
        client = BaseAPIClient()
        result = client.get("/health")
        
        if result.get("success"):
            return {
                "success": True,
                "message": "Backend operativo"
            }
        else:
            error_msg = result.get("error", {}).get("message", "Error desconocido")
            return {
                "success": False,
                "message": f"Backend no disponible: {error_msg}"
            }
    
    except Exception as e:
        logger.exception("Error crítico en health_check()")
        return {
            "success": False,
            "message": f"Error al verificar backend: {str(e)}"
        }