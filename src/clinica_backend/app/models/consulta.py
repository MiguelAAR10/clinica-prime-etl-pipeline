# src/clinica_backend/app/models/consulta.py

""" 
MODELOS DE CONSULTA MEDICA (El nucleo Transaccional)
Aqui se unen Pacientes, Servicios y Productos
"""

from app.extensions import db # Instancia de SQLAlchemy
                              # Conectado a PostgreSQL
from app.models.base import BaseModel # Clase base para todos los modelos
                                      #     - Tiene (Metodos comunes)
from sqlalchemy.sql import func # Funciones SQL
                                #   - SQLAlchemy genera funciones Nativas SQL (CURRENT_DATE, NOW, COUNT(), SUM())

#1. La Cabecera (La Cita)
class Consulta(BaseModel):
    __tablename__ = 'consultas'
    
    id_consulta = db.Column(
        db.Integer,
        primary_key = True, 
        autoincrement=True
        )
    
    # Relacion con Paciente
    id_paciente = db.Column(
        db.Integer,
        db.ForeignKey('pacinetes.id_paciente'),
        nullable = False
    )
    
    fecha_consulta = db.Column(
        db.Date,
        nullable = False,
        server_default=func.current_date()
    )
    notas_generales = db.Column(
        db.Text
     )
    
    # Auditoria: Guardamoes cuanto Costo en Total ese Dia (SnapShot)
    total_historico = db.Column(
        db.Numeric(10,2),
        default = 0.00
    )
    
    # Relaciones
    paciente = db.relationship(
        'Paciente',
        backref = 'consultas'
    )
    
    # Casacade = 'all, delete-orphan':Si borro la consulta se borran sus servicios
    
    servicios = db.relationship(
        'ConsultaServicio',
        backref = 'consulta',
        cascade = 'all, delete-orphan'
    )
    
    def __repre__(self):
        return f'<Consulta #{self.id_consulta} - Paciente {self.id_paciente} - Fecha: {self.fecha_consulta}>'
    
# 2. DETALLE DE SERVICIOS (Que le hicieron?)
class ConsultaServicio(BaseModel):
    __tablename__ = 'consultas_servicios'
    
    id_consulta_servicio = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    
    id_consulta = db.Column(
        db.Integer,
        db.ForeignKey('consultas.id_consulta'),
        nullable = False
    )
    
    id_servicio = db.Column(
        db.Integer,
        db.relationship('servicios_catalogo.id_servicio'),
        nullable = False
    )
    
    precio_servicio = db.Column(
        db.Numeric(10,2),
        nullable = False
    )
    
    
    # ----------- db.relationship ------------  
    # Es una Relacion Entre objetos Python no entre tablas SQL
    # ORM
    #   - Crea un puente para navegar entre objetos como si fuerna atributos
    servicio = db.relationship(
        'Servicio'
    )
    # Un servicio puedo consumir N productos (ej: 1 Botox consume 1 + 1 Vial)
    
    consumos = db.relationship(
        'ConsumoProducto',
        backref = 'consulta_servicio',
        cascade = 'all, delete-orphan'
    )
    
# 3. EL CONSUMO DE MATERIALES (lo que resta inventario)
class ConsumoProducto(BaseModel):
    __tablename__ = "consumo_productos"
    
    id_consumo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    id_consulta_servicio = db.Column(db.Integer, db.ForeignKey('consultas_servicios.id_consulta_servicio'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos_catalogo.id_producto'), nullable=False)
    
    cantidad_consumida = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Precio congelado del producto (Costo)
    precio_producto = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Calculado: cantidad * precio
    importe_venta = db.Column(db.Numeric(10, 2))

    # Relaciones
    producto = db.relationship('Producto')