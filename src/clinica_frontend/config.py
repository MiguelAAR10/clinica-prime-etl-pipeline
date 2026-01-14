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
    
    