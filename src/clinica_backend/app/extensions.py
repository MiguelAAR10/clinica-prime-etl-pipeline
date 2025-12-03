# src/app/extensions.py
"""
MÓDULO DE EXTENSIONES (La Caja de Herramientas Desenchufada)

Aquí creamos las herramientas vacías. NO están conectadas a nada todavía.
Se conectarán más tarde en '__init__.py' cuando la app arranque.
"""

# Importamos las librerías (las herramientas que compramos)
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

# 1. EL GESTOR DE BASE DE DATOS (SQLAlchemy)
# Es el traductor. Tú hablas Python, la base de datos habla SQL.
# Él traduce tus objetos (Pacientes) a tablas y filas.
db = SQLAlchemy()

# 2. EL TRADUCTOR DE JSON (Marshmallow)
# Es el "Portero".
# - Entrada: Revisa que el JSON que envía el Frontend sea válido.
# - Salida: Convierte tus objetos de Python a JSON para enviarlos.
ma = Marshmallow()

# 3. LA MÁQUINA DEL TIEMPO (Migrate)
# Permite hacer cambios en la estructura de la Base de Datos (ej: agregar columna 'edad')
# sin perder los datos que ya tienes guardados.
migrate = Migrate()

# 4. EL DIPLOMÁTICO (CORS)
# Cross-Origin Resource Sharing.
# Por defecto, los navegadores bloquean que una web (React) hable con un servidor (Flask)
# si están en puertos diferentes. Esto da permiso para que hablen.
cors = CORS()