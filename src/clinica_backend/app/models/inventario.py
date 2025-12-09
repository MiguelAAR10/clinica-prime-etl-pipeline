# src/clinica_backend/app/models/inventario.py

from app.extensions import db # `db` Motor ORM
    # Contiene: 
    #   - Conexion PostgreSQL
    #   - Column, Foregin Key, DateTime, etc.
     
from app.models.base import BaseModel # Clase Base para todos los Modelos
    # Contiene:
    #   - Métodos CRUD (save, delete)
    #   - Serialización genérica
    #   - Manejo de errores
    
from sqlalchemy.sql import func # Funciones SQL (ej: NOW())
    # Contiene:
    #   - NOW() para fechas automáticas
    #   - COUNT, SUM, AVG, etc.

class MovimientoStock(BaseModel):
    """
    MODELO KARDEX (Integrado con Triggers SQL)
    - No Actualizamos 'stock_actual' en Python. Dejemps que el Trigger de DB lo haga 
    - Python solo registra el Hecho
    """
    
    __tablename__ = 'movimientos_stock'
    
    id_movimiento = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    
    id_producto = db.Column(
        db.Integer,
        db.ForeignKey('productos_catalogo.id_producto'),
        nullable = False
    )
    
    # Check Constraint esta en DB ('ENTRADA', 'SALIDA')
    tipo_movimiento = db.Column(
        db.String(10),
        nullalble = False
    )
    
    cantidad = db.Column(
        db.Numeric(10,2),
        nullable = False
    )
    
    id_consumo_origen = db.Column(
        db.Integer,
        unique = True,
        nullable = True
    )
    
    fecha_movimiento = db.Column(
        db.DateTime(timezone=True),
        server_default = func.now()
    )
    
    producto = db.relationship(
        'Producto',
        backref = 'movimientos'
    )
    
    def __repr__(self):
        return f'<Movimiento {self.tipo_movimiento} x {self.cantidad}>'
    
    