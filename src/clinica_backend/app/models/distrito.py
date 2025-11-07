# app/models/distrito.py

"""
Modelo Distrito
Representa la Tabla de distritos en la base de datos
Representa las zonas geográficas donde viven los pacientes
"""

from app import db
from app.models.base import BaseModel

class Distrito(BaseModel):
    """
    Modelo para la Tabla `distritos`
    """
    __tablename__ = 'distritos'
    # ¿Por qué '__tablename__'?
    # - Le dice a SQLAlchemy el nombre EXACTO de la tabla en PostgreSQL
    # - Sin esto, SQLAlchemy usaría 'distrito' (nombre de la clase en minúscula)
    # - Pero tu tabla se llama 'distritos' (plural)
    
    # ===============================================================
    # COLUMNAS DEFINICION
    # ===============================================================
    id_distrito = db.Column(
        db.Integer, # Tipo de Datos SQL INTEGER
        primary_key=True, # Clave Primaria
        autoincrement=True # Auto Incremental   
    )
    
    # DESGLOSE LÍNEA POR LÍNEA:
    # db.Column        → Declara una columna en la tabla
    # db.Integer       → Tipo INTEGER en SQL (números enteros)
    # primary_key=True → Esta columna identifica únicamente cada fila
    #                    - No puede ser NULL
    #                    - Debe ser UNIQUE
    #                    - Crea un índice automáticamente (búsquedas rápidas)
    # autoincrement    → PostgreSQL genera: 1, 2, 3, ... automáticamente
    #                    - No necesitas especificar el ID al insertar
    
    nombre_distrito = db.Column(
        db.String(80), # Tipo VARCHAR(80) en SQL
        unique = True, # Valores únicos
        nullable = False # No puede ser NULL
    )
    # DESGLOSE:
    # db.String(80)  → VARCHAR(80) en SQL
    #                  ¿Por qué 80? → Nombres de distrito no son largos
    #                  "San Juan de Lurigancho" = 24 caracteres
    #                  80 da margen suficiente sin desperdiciar espacio
    #
    # unique=True    → Constraint UNIQUE en PostgreSQL
    #                  Previene: INSERT INTO distritos VALUES ('Lima'), ('Lima')
    #                  Error: duplicate key value violates unique constraint
    #
    # nullable=False → Constraint NOT NULL en PostgreSQL
    #                  Previene: INSERT INTO distritos (id) VALUES (1)
    #                  Error: null value in column "nombre_distrito
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # RELACIONES (ORM MAGIC)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Relación inversa: distrito.pacientes
    # backref='distrito' crea automáticamente paciente.distrito
    # lazy='dynamic' retorna una query (no carga todos los pacientes de inmediato)
    
    # ESTO LO DESCOMENTARÁS cuando crees el modelo Paciente
    pacientes = db.relationship('Paciente', backref='distrito', lazy='dynamic')
    
    def __repr__(self):
        """
        Representacion en String del Objeto (Para Debugging)
        Object Representation (Debugging Aid)
        ¿Para qué sirve __repr__?
        
        Sin __repr__:
        >>> distrito = Distrito.query.first()
        >>> print(distrito)
        <Distrito object at 0x7f8b8c0a3d90>  ← No útil
        
        Con __repr__:
        >>> print(distrito)
        <Distrito 1: San Isidro>  ← Descriptivo
        
        Uso:
        - Debugging en terminal
        - Logs más legibles
        - Testing más claro
        
        Returns:
            str: Representación legible del objeto
        """
        return f'<Distrito {self.id_distrito}: {self.nombre_distrito}>'
        
        
        