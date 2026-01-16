# src/clinica_frontend/modules/api_client.py

# -------------------------------------------------------------
# CLIENTE HTTP Reutilizable
# Centraliza todas las Llamadas a la API
# --------------------------------------------------------------

import requests
from typing import Dict, List, Optional, Any
from config import Config

class APIClient: 
    """
    Cliente HTTP para comunicarse con el Backend Flask
    
    Ventajas de Centralizar: 
        - Manejo de Errores Consistentes]
        - Headers Comunes (auth, content-type)
        - logging Centralizado
        - Facil de TRestear (mock)
        
    Patron de Diseno: Singleton (una sola instancia)
    """

    def __init__(self): 
        self.base_url = Config.API_BASE_URL
        self.timeout = Config.API_TIMEOUT
        self.session = requests.Session() # Reutiliza Conexiones
        
        # Headers Comunes para todas las requests
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    # ---------------------------------------
    # METODOS GENERICOS (HTTP)
    # ---------------------------------------
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Maneja la Repsuesta HTTP de forma consistente.
        Args: 
            response: Objeto Response de Requests
        
        Returns:
            Dict con los Datos o informacion del Error        
        
        Raises:
            No lanza Excepeciones, devuelve un dict con error
        """
        
        try:
            # Intentar parsear JSON
            data = response.json()
        except ValueError:
            # Si no es JSON, devolver texto plano
            data = {"message": response.text}
        
        # Agrgear Metadata a la Repsuesta
        return {
            "success": response.ok, # True si status 200-299
            "status_code": response.status_code,
            "data": data if response.ok else None,
            "error": data if not response.ok else None
        }
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        GET request generico.
        
        Args: 
            endpoint: Ruta Relativa 
            params : Query paramteters
            
        Returns:
            Dict con la Repsuesta procesada
        
        Example:
            >>> client = APIClient()
            >>> result = client.get("/pacientes", params={"limit": 10})
            >>> if result["success"]:
            >>>     pacientes = result["data"]["data"]
            
        """    
        
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(
                url,
                params = params,
                timeout = self.timeout
            )
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "El servidor tardo demasiado en Responder",
                "error_Type": "Timeout"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "No se puede conectar al Servidor",
                "error_type": "connection"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error Inesperado {str(e)}",
                "error_type": "unknown"
            }
    
    def post(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        """
        POST request generico
        
        Args:
            - endpoint: Ruta Relativa
            - data: Datos a Enviar (Se convierte a JSON Automaticamente)
            
        Returns:
            Dict con la Repsuesta procesada
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.post(
                url,
                json = data,
                timeout = self.timeout
            )
            return self._handle_response(response)
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "El servidor tardo demasiado en responder",
                "error_type": "timeout"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "No se puede conectar al Servidor",
                "error_type": "connection"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Eror inesperafo : {str(e)}",
                "error_type": "unknown"
            }
            