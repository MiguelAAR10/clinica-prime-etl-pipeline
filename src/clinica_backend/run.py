# run.py (en la raíz del proyecto)
"""
Punto de entrada para ejecutar el servidor de desarrollo
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar la factory
from app import create_app

# Crear la aplicación
config_name = os.environ.get('FLASK_ENV', 'default')
app = create_app(config_name)

if __name__ == '__main__':
    """
    Ejecutar servidor de desarrollo
    
    NUNCA usar app.run() en producción.
    En producción usa: gunicorn, uwsgi, etc.
    """
    app.run(
        host='0.0.0.0',  # Accesible desde red local
        port=5000,
        debug=True       # Solo en development
    )