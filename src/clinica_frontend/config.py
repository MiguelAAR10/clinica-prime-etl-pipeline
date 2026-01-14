# CONFIGURACION CENTRALIZADA 
# Archivo Maestro de configuracion

import os
from dotenv import load_dotenv

# Cargar Variables de entorno desde .env 
load_dotenv()

class Config:
    """
    Configuracion centralizada de la Aplicacion
    
    Ventajas : 
        - Un solo lugar para cambiar configuracion
        - Validacion de variables requeridas
        - Valores por Defecto Seguros 
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
    
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False") == "True"
    
    """
    Modo Debug (Muestra errores Detallados)
    OJO: Nunca exponer en porduccion (expone infomricon sensible
    """
    
    PAGE_TITLE = os.getenv("PAGE_TITLE", "MediStock ERP")
    PAGE_ICON = os.getenv("PAGE_ICON", "")
    LAYOUT = os.getenv("LAYOUT", "wide")
    
    # Validaion de COnfiguracion
    
    @classmethod
    def validate(cls):
        """d
        Valida que la configuracion sea correcta
        Lanza excepcion si falta algo critico
        """
        if not cls.API_BASE_URL:
            raise ValueError("API_BASE_URL"):
        
        if cls.API_TIMEOUT <= 0:
            raise ValueError("API_TIMEOUT debe ser positiva")
        
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
