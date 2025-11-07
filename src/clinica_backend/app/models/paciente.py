# src/app/models/paciente.py
"""
Modelo Paciente - Entidad central del negocio
"""

from app import db
from app.models.base import BaseModel
from datetime import datetime, date
import pytz
from flask import current_app

# Importamos el modelo Distrito para la relación
from app.models.distrito import Distrito


class Paciente(BaseModel):
    """
    Representa un paciente de la clínica (Tabla: pacientes)
    Hereda de BaseModel.
    """
    
    __tablename__ = 'pacientes'
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # COLUMNAS (Identidad)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    id_paciente = db.Column(
        db.BigInteger,
        primary_key=True
    )
    
    dni = db.Column(
        db.String(20),
        unique=True,        # DNI único en el sistema
        index=True          # Índice para búsquedas rápidas
    )
    
    nombre_completo = db.Column(
        db.String(255),
        nullable=False,     # Campo obligatorio
        index=True          # Índice para búsquedas por nombre
    )
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # COLUMNAS (Datos Demográficos)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    sexo = db.Column(db.String(10))
    
    telefono = db.Column(db.String(25))
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # COLUMNAS (Fecha de Nacimiento - Parcial)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    nacimiento_year = db.Column(db.Integer)
    nacimiento_month = db.Column(db.Integer)
    nacimiento_day = db.Column(db.Integer)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # COLUMNAS (Metadatos)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    paciente_problematico = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
    
    created_at = db.Column(
        db.DateTime(timezone=True), # Usa TIMESTAMPTZ
        nullable=False,
        default=lambda: datetime.now(pytz.timezone(current_app.config.get('TIMEZONE', 'UTC')))
    )
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # RELACIONES (El Corazón del ORM)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # --- 1. EL ANCLA ⚓ ---
    # Esta es la columna FÍSICA en la DB.
    # Es la 'Foreign Key' que "ancla" este paciente a un distrito.
    id_distrito = db.Column(
        db.BigInteger,
        db.ForeignKey('distritos.id_distrito'), # apunta a 'tabla.columna'
        nullable=True       # Un paciente PUEDE no tener distrito
    )
    
    # --- 2. EL PORTAL MÁGICO 🌀 ---
    # Esto NO es una columna. Es la magia de SQLAlchemy (Python).
    # Crea el atributo 'paciente.distrito'
    distrito = db.relationship(
        'Distrito',  # El nombre de la CLASE a la que se conecta
        
        # 'backref' crea MÁGICAMENTE la propiedad 'distrito.pacientes'
        # en el modelo Distrito.
        backref=db.backref('pacientes', lazy='dynamic'),
        
        # 'lazy' controla CÓMO se carga esta relación.
        # 'select' (default): Se dispara un query CUANDO pides paciente.distrito
        # 'joined': SQLAlchemy hace un JOIN automático en la query original
        # 'dynamic': Devuelve un OBJETO QUERY (ideal para 1-a-Muchos)
        lazy='joined' # 'joined' es ideal para N-a-1 (siempre querrás el distrito)
    )
    
    
    def __repr__(self):
        """Representación en string"""
        return f'<Paciente {self.id_paciente}: {self.nombre_completo}>'
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PROPIEDADES CALCULADAS (El Medidor Mágico ⛽)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    @property
    def edad(self):
        """
        Calcula la edad del paciente dinámicamente.
        Se accede como 'paciente.edad' (gracias a @property)
        """
        if not self.nacimiento_year:
            return None
        
        hoy = date.today()
        edad_base = hoy.year - self.nacimiento_year
        
        # Ajustar si aún no ha cumplido años este año
        if self.nacimiento_month and self.nacimiento_day:
            try:
                if (hoy.month, hoy.day) < (self.nacimiento_month, self.nacimiento_day):
                    edad_base -= 1
            except TypeError:
                # En caso de mes/día inválido (ej. 0)
                pass 
                
        return edad_base
    
    @property
    def fecha_nacimiento_completa(self):
        """
        Retorna fecha de nacimiento como 'date object' si es válida.
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
            # Fecha inválida (ej: 31 de febrero)
            return None
    
    @property
    def alertas(self):
        """
        Genera lista de alertas sobre datos incompletos.
        Lógica de negocio VIVA dentro del modelo.
        """
        alertas = []
        
        if not self.nacimiento_year:
            alertas.append('falta_anio_nacimiento')
        elif not self.nacimiento_month or not self.nacimiento_day:
            alertas.append('falta_mes_dia_nacimiento')
        
        if self.nacimiento_year and not self.fecha_nacimiento_completa:
             alertas.append('fecha_nacimiento_invalida')
        
        if not self.telefono:
            alertas.append('sin_telefono')
        
        if not self.id_distrito:
            alertas.append('sin_distrito')
        
        return alertas
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MÉTODOS DE SERIALIZACIÓN Y DE FÁBRICA
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def to_dict_completo(self):
        """
        Sobrescribe to_dict() de BaseModel para agregar
        campos calculados y relaciones.
        
        Esta es la "tarjeta de presentación" del paciente.
        """
        # 1. Obtener diccionario base (columnas de la DB)
        data = super().to_dict()
        
        # 2. Agregar campos calculados (@property)
        data['edad'] = self.edad
        data['alertas'] = self.alertas
        
        # 3. Formatear fecha de nacimiento
        if self.fecha_nacimiento_completa:
            data['fecha_nacimiento'] = self.fecha_nacimiento_completa.isoformat()
        else:
            data['fecha_nacimiento'] = None
        
        # 4. Incluir datos del distrito (de la relación)
        if self.distrito:
            data['distrito'] = {
                'id_distrito': self.distrito.id_distrito,
                'nombre_distrito': self.distrito.nombre_distrito
            }
        else:
            data['distrito'] = None
        
        # 5. Convertir a camelCase para el Frontend
        return self._to_camel_case(data)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MÉTODOS DE FÁBRICA (El Gerente de Fábrica 🏭)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @classmethod
    def buscar_por_dni(cls, dni):
        """
        Busca un paciente por su DNI.
        Se usa como: Paciente.buscar_por_dni('123')
        """
        return cls.query.filter_by(dni=dni).first()
    
    @classmethod
    def buscar_por_nombre(cls, nombre, limit=20):
        """
        Busca pacientes por nombre (búsqueda parcial 'ilike')
        Se usa como: Paciente.buscar_por_nombre('juan')
        """
        # 'ilike' es como LIKE pero Case-Insensitive
        return cls.query.filter(
            cls.nombre_completo.ilike(f'%{nombre}%')
        ).limit(limit).all()