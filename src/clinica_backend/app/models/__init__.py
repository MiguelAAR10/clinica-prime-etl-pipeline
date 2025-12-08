# src/app/models/__init__.py
"""
Este archivo convierte la carpeta 'models' en un Paquete Python.
Se usa como Fachada (Facade Pattern) para exponer los modelos
de dominio (Paciente, Distrito) y la clase base (BaseModel)
a toda la aplicación.
"""

# Importa tu clase Base que contiene los métodos de persistencia
# desde el archivo 'base.py' en el mismo directorio.
from .base import BaseModel

# Importa el Modelo Distrito desde el archivo 'distrito.py'
from .distrito import Distrito

# Importa el Modelo Paciente desde el archivo 'paciente.py'
from .paciente import Paciente

# Ahora, el resto de la aplicación puede hacer la importación limpia:
# from app.models import Paciente, Distrito, BaseModel

from .marca import Marca
from .producto import Producto
from .servicio import Servicio