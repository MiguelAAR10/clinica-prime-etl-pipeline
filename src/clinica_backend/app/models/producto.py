"""
MODELO PRODUCTO
Representa el ítem físico o servicio que se vende.
Es una entidad "Hija" (Depende de una Marca).
"""
from app.extensions import db
from app.models.base import BaseModel

class Producto(BaseModel):
    __tablename__ = 'productos_catalogo'

    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # FK: El vínculo con el Padre
    id_marca = db.Column(
        db.Integer, 
        db.ForeignKey('marcas_catalogo.id_marca'), # Apunta a tabla.columna
        nullable=False
    )
    
    nombre_producto = db.Column(db.String(150), nullable=False)
    unidad_medida = db.Column(db.String(20)) # Ej: "Vial", "Caja", "Unidad"
    
    # Decimales para dinero (Numeric es mejor que Float para dinero)
    costo_unitario = db.Column(db.Numeric(10, 2), default=0.00)
    precio_venta = db.Column(db.Numeric(10, 2), default=0.00)
    
    # RELACIÓN MUCHOS-A-UNO
    # Muchos productos pertenecen a una sola marca.
    marca = db.relationship(
        'Marca',
        back_populates='productos'
    )

    def __repr__(self):
        return f'<Producto {self.nombre_producto}>'
    