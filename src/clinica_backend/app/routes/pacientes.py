# ============================================
# DEPARTAMENTE DE GESTION DE PACIENTES
# Mision: Proveer los Endposints de la API para interactuar con los pacientes
# ============================================

from app import db # Importa la instancia de SQLAlchemy
from app.models.base import BaseModel # Importa la clase base para los modelos
from datetime import datetime, date # Importa datetime para manejo de fechas
import pytz # Importa pytz para manejo de zonas horarias

class Paciente(BaseModel):
    __tablename__ = "pacientes"
    
    id_paciente = db.Column(
        db.Integer, # Establecer el Tipo de Dato
        primary_key = True, # Establecer como `Clave Primaria`
        autoincrement = True # Auto Incremental
    )
    dni =  db.Column(
        db.String(20), # Establcer que es un Tipo de Dato Texto
        unique = True, # <- Critico: Un dni por Persona
        nullable = False # <- NO Puede ser NULL 
    )
    
    nombre_completo = db.Column(
        db.String(225),
        nullable = False 
    )
    
    sexo = db.Column(
        db.String(10),
        nullable = True
    )
    
    telefono = db.Column(db.String(25), nullable=True)
    
    nacimiento_year = db.Column(db.Integer, nullable=True)
    nacimiento_month = db.Column(db.Integer, nullable=True)
    nacimiento_day = db.Column(db.Integer, nullable=True)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # COLUMNAS: RELACIONES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    id_distrito = db.Column(
        db.Integer,
        db.ForeignKey('distritos.id_distrito'),  # ← Relación a tabla distritos
        nullable=True
    )
    # ¿Qué hace db.ForeignKey?
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 1. Crea constraint en PostgreSQL:
    #    FOREIGN KEY (id_distrito) REFERENCES distritos(id_distrito)
    #
    # 2. Garantiza integridad referencial:
    #    - No puedes poner id_distrito = 999 si no existe
    #    - Error: violates foreign key constraint
    #
    # 3. Previene orfanatos:
    #    - Si intentas DELETE un distrito con pacientes:
    #    - Error (a menos que uses CASCADE)
    #
    # FUNDAMENTO CS: Referential Integrity (Codd's Relational Model)
    
    # Relación ORM (la magia de SQLAlchemy)
    distrito = db.relationship(
        'Distrito',           # Clase del modelo relacionado
        backref='pacientes',  # Crea distrito.pacientes automáticamente
        lazy='joined'         # Estrategia de carga
    )
    # ¿Qué hace relationship?
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Permite hacer:
    # paciente = Paciente.query.first()
    # print(paciente.distrito.nombre_distrito)  ← ¡Sin JOIN manual!
    #
    # SQLAlchemy genera el JOIN automáticamente:
    # SELECT pacientes.*, distritos.*
    # FROM pacientes
    # LEFT JOIN distritos ON pacientes.id_distrito = distritos.id_distrito
    #
    # ¿Qué es lazy='joined'?
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # OPCIÓN A: lazy='select' (default)
    # - Query inicial: SELECT * FROM pacientes
    # - Al acceder distrito: SELECT * FROM distritos WHERE id = X
    # - Problema: N+1 queries (lento con muchos pacientes)
    #
    # OPCIÓN B: lazy='joined' (tu elección)
    # - Una sola query con LEFT JOIN
    # - Más rápido si SIEMPRE necesitas el distrito
    # ✅ RECOMENDADO para relaciones N:1 frecuentes
    #
    # OPCIÓN C: lazy='dynamic'
    # - Retorna query object (para relaciones 1:N grandes)
    # - Ej: paciente.consultas (podría ser 1000 consultas)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # COLUMNAS: METADATOS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    paciente_problematico = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
    # ¿Para qué sirve este flag?
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # CASO DE USO:
    # - Paciente que hace scams (paga con cheques sin fondos)
    # - Paciente violento
    # - Sistema de alertas en recepción
    #
    # Query útil:
    # pacientes_problema = Paciente.query.filter_by(
    #     paciente_problematico=True
    # ).all()
    
    created_at = db.Column(
        db.DateTime(timezone=True),  # TIMESTAMPTZ en PostgreSQL
        nullable=False,
        default=lambda: datetime.now(pytz.timezone('America/Lima'))
    )
    # ¿Por qué DateTime(timezone=True)?
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # FUNDAMENTO: Siempre usa timestamps con timezone en apps reales
    #
    # DateTime sin TZ:
    # - Guarda: '2024-01-15 10:00:00'
    # - Ambiguo: ¿UTC? ¿Lima? ¿Madrid?
    #
    # DateTime(timezone=True):
    # - Guarda: '2024-01-15 10:00:00-05:00' (Lima)
    # - PostgreSQL lo convierte a UTC internamente
    # - Al leer, convierte a tu timezone
    #
    # default=lambda: ...
    # - Se ejecuta en el MOMENTO del INSERT
    # - Usa timezone de Lima (tu configuración)
    # - Alternativa: db.func.now()
    
    def __repr__(self):
        """
        Representacion en String
        """
        return f'<Paciente {self.id_paciente} : {self.nombre_completo}'
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MÉTODOS DE INSTANCIA (LÓGICA DEL MODELO)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    @property
    def edad(self):
        """
        Calcula la edad del paciente DINÁMICAMENTE
        
        FUNDAMENTO CS: Computed Property (Data Derivation)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        ¿Por qué @property y no una columna 'edad' en la DB?
        
        OPCIÓN A (Malo): Columna 'edad INTEGER' en DB
        - Problema: Se vuelve obsoleta (hoy 30, mañana 31)
        - Requiere: Background job que actualiza todas las edades diario
        - Inconsistencia: ¿Qué pasa si el job falla?
        
        OPCIÓN B (Bueno): Calcular dinámicamente (tu elección)
        """
        if not self.nacimiento_year:
            return None
        
        hoy = date.today()
        edad = hoy.year - self.nacimiento_year
        
        # Ajustar si aun no ha cumpliado anos este ano
        if self.nacimiento_month and self.nacimiento_day:
            if (hoy.month, hoy.day) < (self.nacimiento_month, self.nacimiento_day):
                edad -= 1
        
        return edad

    @property
    def fecha_nacimiento_completa(self):
        """
        Retorna fecha de nacimiento como date Objecct
        
        Returns:
            date o None: Fecha de nacimiento Completa 
        """
        
        if not all([self.nacimiento_year, self.nacimiento_month, self.nacimiento_day]):
            return None
        
        try:
            return date(
                self.nacimiento_year,
                self.nacimiento_month,
                self.nacimiento_day
            )
        except ValueError:
            # Fecha Invalida (31 de Febrero)
            return None
    
    @property
    def alertas(self):
        """
        Genera lista de alertas sobre Datos incompletos
        
        Returns:
            list: Lista de Codigos de Alerta
            
        Ejemplo:
            paciente.alertas # ['falta_mes_dia_nacimiento', 'sin_telefono']
        """
        alertas = []
        
        if not self.nacimiento_year:
            alertas.append('falta_anio_nacimiento')
        elif not self.nacimiento_month or not self.nacimiento_day:
            alertas.append('falta_mes_dia_nacimiento')
        
        if self.fecha_nacimiento_completa is None and self.nacimiento_year:
            alertas.append('fecha_nacimiento_invalida')
        
        if not self.telefono:
            alertas.append('sin_telefono')
        
        if not self.id_distrito:
            alertas.append('sin_distrito')
        
        return alertas
    
    #--------------------------------------------------
    # MÉTODOS PERSONALIZADOS DE CLASE (QUERY HELPERS)
    #--------------------------------------------------
    
    def to_dict(self, include_relations = False):
        """
        Sobreescribir to_Dict() de BaseModel para agregar campos calculados
        
        Args:
            include_relations (bool): Incluir datos del distrito relacionado
        """
        # obtener Diccionario Base
        data = super().to_dict()
        
        # Agregar campos calculados
        data['edad'] = self.edad
        data['alertas'] = self.alertas
        
        # Formatear fecha de Nacimiento
        if self.fecha_nacimiento_completa:
            data['fechaNacimiento'] = self.fecha_nacimiento_completa.isoformat()
        else:
            data['fechaNacimiento'] = None
            
        # Incluir Datos del Distrito si se Solicita
        if include_relations and self.distrito:
            data['distrito'] = {
                'id': self.distrito.id_distrito,
                'nombre': self.distrito.nombre_distrito
            }
        
        # Convertir Keys a camelCase para FrontEnd
        data = self._to_camel_case(data)
        
        return data

    @staticmethod # Convierte a Metodo Estático ( Significa que no usa self )
    def _to_camel_case(data):
        """
        Convierte keys de snake_case a camelCase
        
        Args:
            data (dict): Diccionario con keys en snake_case
        
        Returns:
            dict: Diccionario con keys en camelCase
        
        Ejemplo:
            {'nombre_completo': 'Juan Perez'} 
            → {'nombreCompleto': 'Juan Perez'} 
        """
        
        camel_data = {}
        for key, value in data.items():
            # Convertir snake_case a camelCase
            components = key.split('_')
            camel_key = components[0] + ''.join(x.title() for x in components[1:])
            camel_data[camel_key] = value

        return camel_data
    
    @staticmethod
    def buscar_por_Dni(cls, dni):
        """
        Busca un paciente por su DNI
        
        Args:
            dni(str): DNI a Buscarq
        
        Returns: 
            Paciente o None
        
        Uso:
            paciente = Paciente.buscar_por_Dni('12345678')
        """
        
        return cls.query.filter_by(dni=dni).first()
    
    @staticmethod
    def buscar_por_nombre(cls, nombre, limit = 20):
        """
        Busca pacientes por nombre (Busqueda parcial, case-insensitive)
        
        Args:
            nombre (str): Texto s Buscar
            limit (int): Maximo de Resultados
        Returns: 
            list: Lista de Pacientes que coinciden
        
        Uso:
            pacientes = Paciente.buscar_por_nombre('Juan')
        """
        return cls.query.filter(
            cls.nombre_completo.ilike(f'%{nombre}%').limit(limit).all()
        )

