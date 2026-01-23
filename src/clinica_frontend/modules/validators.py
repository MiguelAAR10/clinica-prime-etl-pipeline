# src/clinica/_frontend/modules/validators.py

# ----------------------------------------------
# VALIDADORES CENTRALIZADOS
# ----------------------------------------------

"""
Validadores de Negocio para toda la App

Principio: Single Source of Truth
    - Las Reglas de Validacion estan en un SOLO LUGAR
    - Frontend y Backend usan las mismas  reglas 
    - Si cambia una regla, se cambia en un solo archivo

Analogia: es como el Reglamento de Transito
    - No puede haber un reglamento diferente en cada ciudad 
    - Todos siguen las mismas reglas
"""

from datetime import datetime, date 
from typing import Optional

cla 

