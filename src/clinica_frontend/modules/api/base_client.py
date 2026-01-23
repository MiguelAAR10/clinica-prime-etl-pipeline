# src/clinica_frontend/modules/api/base_client.py

# -------------------------------------------------------------
# CLIENTE HTTP Reutilizable
# -------------------------------------------------------------
# Proposito:
#       - Base para Comunicacion con Backend Flask
#       - Centraliza todas las Llamadas a la API
# --------------------------------------------------------------

import requests
    # Libreria HTTP(HiperText Transfer Protocol) de Terceros (No viene con Python)
    # Contiene: (Clase: `Session()`, Funciones: get(), post(), put(), delete(), etc.)
    # Request Alto Nivel: Simple y Poderoso
    
from typing import Dict, List, Optional, Any    
    # Modulo Estandar Python
    #    - Proposito: Type Hints (Anotaciones d Tipo)
    #    - Mejores Practicas de Tipo Profesional

import logging
    # Modulo Estandar Python para Registro de Logs (Eventos)
    # Porposito:
    #   - Dejar Rastro  de lo que hace la Aplicacion1``
    
from config import Config

# Configuracion Logger
logger = logging.getLogger(__name__)
# ├─ Crear/obtener logger para este módulo
# ├─ Si ya existe: lo reutiliza
# ├─ Si no existe: lo crea
# └─ Resultado: objeto logger con nombre único

"""
DEBUG:     Información detallada (solo desarrollo)
INFO:      Información general (normal)
WARNING:   Advertencia (algo anormal pero sigue)
ERROR:     Error (algo falló, pero app sigue)
CRITICAL:  Crítico (app va a fallar)

Ejemplo visual:
DEBUG:    "GET /pacientes | Params: {'limit': 10}"
INFO:     "Usuario Juan inició sesión"
WARNING:  "Retry 3 de 5 en GET /pacientes"
ERROR:    "TIMEOUT en GET /pacientes"
CRITICAL: "Base de datos no disponible"
"""

class APIClient: 
    """
    Cliente HTTP para comunicarse con el Backend Flask
    
    Ventajas de Centralizar: 
        - Manejo de Errores Consistentes
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
            "Accept": "application/json",
            "User-Agent": "MediStock-Frontend/1.0"
                # User-Agent: Identificacion del Cliente HTTP
                # Carnet Identidad
        })
    
    # ---------------------------------------
    # METODOS PRIVADOS (CORE)
    # ---------------------------------------
    
    def _validate_endpoint(self, endpoint: str) -> None:
        """
        Validate que el Endpoint sea seguro y correcto
        
        Previene Errores Comunes:
            - Endpoint: None o Vacio
            - Endpoint: sin '/' inical
            - Endpoint: no-string
        
        Args:
            endpoint: Ruta del Endpoint (debe Empezar con '/')
            
        Raises:
            ValueError: Si el endpoint es invalido    
        """
        
        if not endpoint or not isinstance(endpoint, str):
            raise ValueError(
                f"Endpoint debe ser un string no-vacio."
                f"Recibo: {repr(endpoint)}"
                # ├─ Segunda parte del mensaje
                # ├─ DIAGNÓSTICO: Qué recibió realmente
                # ├─ repr(endpoint): representación Python
                # │
                # ├─ ¿Por qué repr() en lugar de str()?
                # │  ├─ repr("") = "''"  ← Muestra comillas
                # │  │                    (string vacío visible)
                # │  ├─ str("") = ""    ← Sin comillas
                # │  │                   (podría parecer nada)
                # │  │
                # │  ├─ repr(None) = "None"
                # │  │ str(None) = "None"
                # │  │
                # │  ├─ repr(123) = "123"
                # │  │ str(123) = "123"
                # │  │
                # │  └─ Con repr() es INEQUÍVOCO lo que recibiste
                # │
                # └─ EJEMPLO DE MENSAJE:
                #    "Endpoint debe ser un string no-vacio.Recibo: ''"
                #    "Endpoint debe ser un string no-vacio.Recibo: None"
                #    "Endpoint debe ser un string no-vacio.Recibo: 123"
            )

        if not endpoint.startswith("/"):
            raise ValueError(
                f"Endpoint debe iniciar con '/'. "
                f"Recibo: {endpoint}"
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
        
        # Intentar 
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
        
        # Agregar status_code a la respuesta del Backend
        if isinstance(data, dict):
            data["status_code"] = response.status_code
            return data
        
        # Si el Backend devuelve una lista directamente (raro)
        return {
            "success": response.ok,
            "status_code": response.status_code,
            "data": data
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
            
            return self._handle_response(response)
            
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
                "error": f"Error inesperafo : {str(e)}",
                "error_type": "unknown"
            }
    def put(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        
        """
        PUT request generico (Actualizar recurso completo).
        
        PUT actualiza TODOS los campos del recurso.
        Diferencia con PATCH: PUT reemplaza todo, PATCH solo lo que envías.
        
        Args:
            endpoint: Ruta relativa (ej: "/pacientes/5")
            data: Diccionario con datos a actualizar
        
        Returns:
            Dict con {"success": bool, "status_code": int, "data": dict, "error": dict}
        
        Example:
            >>> client = APIClient()
            >>> result = client.put("/pacientes/5", {"nombre": "Juan", "edad": 35})
            >>> if result["success"]:
            >>>     print("Paciente actualizado")
        """
        try:
            # LÍNEA 1: Construir URL completa
            url = f"{self.base_url}{endpoint}"
            # Ejemplo: "http://localhost:5000/api/v1" + "/pacientes/5"
            # Resultado: "http://localhost:5000/api/v1/pacientes/5"
            
            # LÍNEA 2: Hacer petición PUT
            response = self.session.put(
                url,
                json=data,           # Convierte dict a JSON automaticamente
                timeout=self.timeout  # Espera máximo 10 segundos (default)
            )
            # ¿Por qué json= ? Porque Flask espera Content-Type: application/json
            # Requests automáticamente setea el header correcto
            
            # LÍNEA 3: Procesar respuesta (success, status_code, data, error)
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            # Timeout: El servidor no respondió en 10 segundos
            return {
                "success": False,
                "error": "El servidor tardó demasiado en responder",
                "error_type": "timeout"  # ← IMPORTANTE: especificar tipo
            }
        
        except requests.exceptions.ConnectionError:
            # Connection Error: No hay conexión con el servidor
            return {
                "success": False,
                "error": "No se puede conectar al servidor",
                "error_type": "connection"
            }
        
        except Exception as e:
            # Cualquier otro error inesperado
            return {
                "success": False,
                "error": f"Error inesperado: {str(e)}",
                "error_type": "unknown"
            }


    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        DELETE request generico (Eliminar recurso).
        
        DELETE elimina completamente un recurso de la base de datos.
        Generalmente devuelve 204 No Content si tuvo éxito.
        
        Args:
            endpoint: Ruta relativa (ej: "/pacientes/5")
        
        Returns:
            Dict con {"success": bool, "status_code": int, "data": dict, "error": dict}
        
        Example:
            >>> client = APIClient()
            >>> result = client.delete("/pacientes/5")
            >>> if result["success"]:
            >>>     print("Paciente eliminado")
        """
        try:
            # LÍNEA 1: Construir URL completa
            url = f"{self.base_url}{endpoint}"
            # Ejemplo: "http://localhost:5000/api/v1" + "/pacientes/5"
            # Resultado: "http://localhost:5000/api/v1/pacientes/5"
            
            # LÍNEA 2: Hacer petición DELETE
            # IMPORTANTE: DELETE NO envía un body (no tiene json=data)
            response = self.session.delete(
                url,
                timeout=self.timeout  # Espera máximo 10 segundos
            )
            # ¿Por qué no json= ? Porque DELETE no necesita enviar datos
            # Solo le dices "elimina lo que está en esta URL"
            
            # LÍNEA 3: Procesar respuesta
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "El servidor tardó demasiado en responder",
                "error_type": "timeout"
            }
        
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "No se puede conectar al servidor",
                "error_type": "connection"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error inesperado: {str(e)}",
                "error_type": "unknown"
            }

    # ============================================
    # METODOS ESPECIFICOS (PACIENTES)
    # ===========================================
    
    def get_pacientes(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Obtiene lista de Pacientes.
        Args:
            - limit: Numero maximo de pacientes a devolver
            
        Returns: 
            - Dict con Lista de Pacientes o Error    
        """
        return self.get("/pacientes", params = {"limit": limit, "offset": offset})
    
    def get_paciente(self, paciente_id: int) -> Dict[str, Any]:
        """
        Obtiene un Paciente especifico por ID
        
        Args:
            paciente_id: ID del Paciente
        
        Returns:
            Dict con estrucutura: {success, status_code, data, error}
        """
        return self.get(f"/pacientes/{paciente_id}")
    
    def crear_paciente(self, data: Dict) -> Dict[str, Any]:
        """
        Crea un nuevo paciente.
        
        Args:
            data: Diccionario con datos del paciente
                {
                    "dni": "12345678",
                    "nombreCompleto": "Juan Pérez",
                    "telefono": "987654321",
                    "idDistrito": 1,
                    "sexo": "M",
                    "nacimientoYear": 1990,
                    "nacimientoMonth": 1,
                    "nacimientoDay": 15
                }
        
        Returns:
            Dict con estructura: {success, status_code, data, error}
        """
        return self.post("/pacientes", data)
    
    def actualizar_paciente(self, id_paciente: int, data: Dict) -> Dict[str,Any]:
        """
        Actualiza un paciente existente.
        
        Args:
            paciente_id: ID del paciente a Actualizar
            data: Diccionario con campos a Actualizar 
        
        Returns:
            Dict con estructura: {success, status_cODE }
        """
        return self.put(f"/pacientes/{id_paciente}", data)
    
    def eliminar_paciente(self, id_paciente: int) -> Dict[str, Any]:
        """
        Eliminar paciente en base al num de su id
        
        """
        return self.delete(f"/pacientes/{id_paciente}")
    
    # ==================================================
    # METODOS  ESPECIFICOS (INVENTARIO)
    # ==================================================
    
    def get_productos(
        self,
        limit: int=100,
        offset: int=0     
        ) -> Dict[str, Any]:
        """
        Obtiene lista de productos.
    
        Args:
            limit: Máximo de registros (default: 100)
            offset: Desplazamiento para paginación (default: 0)
        
        Returns:
            Dict con estructura: {success, status_code, data, error}
    
        """
        
        return self.get("/productos", params={"limit":limit, "offset":offset})
    
    def get_movimientos_stock(
        self, 
        id_producto: Optional[int] = None,
        limit: int = 100,
        offset: int = 0        
    ) -> Dict[str, Any]:
        """
        Obtiene movimientos de stock (kárdex).
        
        Args:
            id_producto: Filtrar por producto (optional)
            limit: Máximo de registros (default: 100)
            offset: Desplazamiento para paginación (default: 0)
        
        Returns:
            Dict con estructura: {success, status_code, data, error}
        """
        
        params = {"limit": limit, "offset": offset}
        
        if id_producto is not None:
            params["id_producto"] = id_producto
        
        return self.get("/inventario/movimientos", params=params)
        
    def registrar_entrada_stock(
        self,
        id_producto: int,
        cantidad: int, 
        referencia: str = None
    ):
        """
        Registra entrada de Stock para un producto.
        
        Parametros:
            id_producto: int - ID del producto (debe existir en DB)
            cantidad: int - Numero de unidades a registrar (debe ser > 0)
            referencia: str - Numero de orden de compra o referencia interna (Opcional)
        """
        if id_producto <= 0:
            raise ValueError("id_producto debe ser > 0")
        if cantidad <= 0:
            raise ValueError("cantidad debe ser > 0")
        data = {
            "id_producto": id_producto,
            "cantidad": cantidad,
            "tipo_movimiento": "ENTRADA", # <- GARANTIZADO
            "referencia": referencia
        }
        
        return self.post("/inventario/movimientos", data)
    
    def registrar_salida_stock(
        self,
        id_producto: int,
        cantidad: int,
        razon: str = "Consumo"
    ):
        data = {
            "id_producto": id_producto,
            "cantidad": cantidad,
            "tipo_movimiento": "SALIDA", 
            "razon": razon
        }
        
        return self.post("inventario/movimientos", data)
    
    # ═══════════════════════════════════════════════════════
    # MÉTODOS FALTANTES (CONSULTAS)
    # ═══════════════════════════════════════════════════════

    def get_servicios(self) -> Dict[str, Any]:
        """Obtiene catálogo de servicios (Botox, etc)."""
        return self.get("/servicios")

    def registrar_consulta(self, data: Dict) -> Dict[str, Any]:
        """
        Registra la consulta completa (Acto médico + Consumo).
        """
        return self.post("/consultas", data)

    # ==============================================
    # HEALTH CHECK
    # ==============================================
    
    def health_check(self) -> Dict[str, Any]:
        """
        Verifica si el backend esta vivo.
        
        Returns:
            Dict con status del servidor 
        """
        try: 
            # Endpoint de health (Flask)
            response = self.session.get(
                f"{self.base_url.replace('/api/v1', '')}/health", timeout=5
            )
            
            return {
                "success":response.ok, 
                "status":response.json() if response.ok else None
            }
            
        except:
            return {
                "success":False,
                "status": "offline"
            }
            
# =============================================
# INSTANCIA GLOBAL
# =============================================
    
api_client = APIClient()

"""
¿POR QUÉ SINGLETON?
-------------------
Para reutilizar la misma sesión HTTP (conexiones persistentes).

USO:
----
# En cualquier módulo:
from modules.api_client import api_client

result = api_client.get_pacientes()
if result["success"]:
    pacientes = result["data"]["data"]
"""  