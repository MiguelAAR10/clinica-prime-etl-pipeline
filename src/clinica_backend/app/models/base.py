# app/models/base

"""
Clase base para todos los Modelos
Proporciona Métodos y Atributos Comunees de Serialización, Validación, etc.
"""

from app.extensions import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

class BaseModel(db.Model):
    """
    Clase Abstracta base para todos los Modelos
    
     FUNDAMENTO CS: Abstracción (Hiding Implementation Details)
        
    ¿Por qué una clase base?
    
    1. REUTILIZACIÓN: Métodos comunes en un solo lugar
    2. CONSISTENCIA: Todos los modelos se comportan igual
    3. MANTENIBILIDAD: Cambias una vez, afecta a todos
    
    ¿Por qué __abstract__ = True?
        
    Le dice a SQLAlchemy: "Esta clase NO es una tabla real,
    solo es un template para otras clases".
    
    Sin __abstract__:
    - SQLAlchemy intentaría crear una tabla 'base_model'
    - Causaría errores
    
    Con __abstract__:
    - SQLAlchemy ignora esta clase
    - Solo usa su código en las clases hijas
    """

    __abstract__ = True  # No crea Tabla para esta clase
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # CRUD BÁSICO (Guardar, Eliminar)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METODOS DE FABRICA (El Gerente de Fabrica)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    @classmethod
    def get_by_id(cls, record_id):
        """
        Obtiene un registro por su ID.
        Uso: Paciente.get_by_id(1)
        """
        return cls.query.get(record_id) 
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MÉTODO DE SERIALIZACIÓN (La Tarjeta de Presentación)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def to_dict(self):
        """
        Convierte el Modelo a Diccionario Python
        
        Serialización (Object -> Data Structure)
        
        Cómo funciona?
        
        1. db.inspect(self) → Obtiene metadata del modelo
        2. .mapper.column_attrs → Lista de columnas
        3. getattr(self, c.key) → Valor de cada columna
        4. dict comprehension → {columna: valor, ...}
        
        EDGE CASE: ¿Qué pasa con relaciones?
        - Las relaciones (ej: paciente.consultas) NO se incluyen
        - Solo columnas simples
        - Para incluir relaciones, cada modelo debe override
        
        Returns:
            dict: Representación en diccionario del modelo
        
        Ejemplo:
            paciente = Paciente(dni='12345678', nombre='Juan')
            paciente.to_dict()
            # {'id_paciente': 1, 'dni': '12345678', 'nombre_completo': 'Juan', ...}
        
        """
        return {
            c.key : getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs
        }
        # `db.inspect(self)` -> Obtiene metadata del modelo actual
        # `.mapper.column_attrs` -> Lista de atributos de columna del modelo
        # `getattr(self, c.key)` -> Obtiene el valor del atributo de la columna actual  
        
    def update(self, data):
        """
        Actualiza el modelo con Datos del Diccionario
        
        Deserializacion (Data -> Object)
        
        ¿Por qué este método?
        
        - Evita escribir: paciente.nombre = data['nombre']
                          paciente.telefono = data['telefono']
                          ... (repetitivo)
        
        - Con este método: paciente.update(data) ✅
        
        ¿Por qué hasattr()?
        
        - Seguridad: Solo actualiza atributos que EXISTEN
        - Si data tiene {'campo_falso': 'valor'}, lo ignora
        - Previene inyección de atributos maliciosos
        
        Args:
            data (dict): Diccionario con valores a actualizar
        
        Ejemplo:
            paciente = Paciente.query.get(1)
            paciente.update({'telefono': '999888777', 'nombre_completo': 'Juan Pérez'})
            db.session.commit()
        
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        # self -> Instancia del modelo actual (Representa objeto Actual)
        # data.items() -> Itera sobre pares clave-valor del diccionario
        # hasattr(self, key) -> Verifica si el atributo existe en el modelo
        # setattr(self, key, value) -> Actualiza el atributo con el nuevo valor ``
        
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MÉTODO DE UTILIDAD (La Caja de Herramientas)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    @staticmethod
    def _to_camel_case(snake_case_dict):
        """
        Herramienta estática para convertir keys de un dict
        de snake_case a camelCase (para respuestas JSON).
        
        Promovido a BaseModel para que TODOS los modelos lo hereden (DRY).
        """
        camel_data = {}
        for key, value in snake_case_dict.items():
            components = key.split('_')
            camel_key = components[0] + ''.join(x.title() for x in components[1:])
            camel_data[camel_key] = value
        
        return camel_data