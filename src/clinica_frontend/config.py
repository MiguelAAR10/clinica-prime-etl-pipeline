# CONFIGURACION CENTRALIZADA 
# Archivo Maestro de configuracion

import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar .env (Mas Robusto)
ENV_FILE = Path(__file__).parent / ".env"
load_dotenv(dotenv_path = ENV_FILE)


class Config:
    """
    Configuracion centralizada de la Aplicacion
    
    Ventajas : 
        - Un solo lugar para cambiar configuracion
        - Validacion de variables requeridas
        - Valores por Defecto Seguros 
        - Single Source of Truth
    """
    
    # API Configuracion
    
    API_BASE_URL = os.getenv(
        "API_BASE_URL",
        "http://localhost:5000/api/v1"
    )
    
    """
    URL base de Backend Flask
    
    Ejemplos:
        - Desarrollo Local: http://localhost:5000/api/v1
        - Produccion: https://api.medistock.com/v1
    """
    
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
    
    """
    Timeout para requests HTTPS (segundos)
    Valor por defecto: 10 segundos
    """
    
    # =============================
    # DEBUG 
    # =============================
    _debug_str  = os.getenv("DEBUG_MODE", "False").strip().lower()
    DEBUG_MODE = _debug_str in ("true", "1", "yes")
    
    """
    Modo Debug (Muestra errores Detallados)
    OJO: Nunca exponer en produccion (expone informacion sensible)
    """
    
    STREAMLIT_PAGE_TITLE = os.getenv("PAGE_TITLE", "🏥 MediStock ERP")
    STREAMLIT_PAGE_ICON = os.getenv("PAGE_ICON", "🏥")
    STREAMLIT_LAYOUT = os.getenv("LAYOUT", "wide")
    
    DNI_MIN_LENGTH = 6
    DNI_MAX_LENGTH = 12# Nombre
    NOMBRE_MIN_LENGTH = 3
    NOMBRE_MAX_LENGTH = 100# Teléfono
    TELEFONO_MIN_LENGTH = 7
    TELEFONO_MAX_LENGTH = 15# Edad
    EDAD_MINIMA = 0
    EDAD_MAXIMA = 120
    
    CACHE_TTL_PACIENTES = 300# 5 minutos (datos estables)
    CACHE_TTL_INVENTARIO = 60# 1 minuto (datos más dinámicos)
    
    # =============================
    # Validaion de COnfiguracion
    # =============================
    
    @classmethod
    def validate(cls):
        """
        Valida que la configuracion sea correcta
        Lanza excepcion si falta algo critico
        """
        
        # Validar API_BASE_URL
        if not cls.API_BASE_URL:
            raise ValueError("API_BASE_URL")
        
        # Validar que sea una URL Valida (basico)
        if not cls.API_BASE_URL.startswith(("http://", "https://")):
            raise ValueError(
                f"API_BASE_URL debe comenzar con http:// o https://"
            )
            
        # Validar API_TIMEOUT
        if cls.API_TIMEOUT <= 0:
            raise ValueError("API_TIMEOUT debe ser positiva")
        
        if cls.API_TIMEOUT > 120:
             print(
                f"⚠️ ADVERTENCIA: API_TIMEOUT es muy alto ({cls.API_TIMEOUT}s). "f"Considera usar un valor entre 5-30 segundos."
            )
        
        
    @classmethod
    def print_config(cls):
        """
        Imprime la configuracion actual(para debugging)
        """
        print("=" * 60)
        print("CONFIGURACIÓN DEL FRONTEND")
        print("=" * 60)
        print(f"API_BASE_URL: {cls.API_BASE_URL}")
        print(f"API_TIMEOUT: {cls.API_TIMEOUT}s")
        print(f"DEBUG_MODE: {cls.DEBUG_MODE}")
        print(f"PAGE_TITLE: {cls.PAGE_TITLE}")
        print("=" * 60)
        
# Validar configuracion al importar
Config.validate()

# Imprimir configuracion en modo debug
if Config.DEBUG_MODE:
    Config.print_config()
