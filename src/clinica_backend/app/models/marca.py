# src/clinica_backend/app/models/marca.py

'''
Modelo Marca
- Representa al Fabricante 
- Es una entidad Padre (NO depende de nadie)
'''

from app.extensions import db
from app.models.base import BaseModel

class Marca(BaseModel):
    
    __tablename__ = 'marcas_catalogo'
    
    id_marca = db.Column(
        db.Integer, 
        primary_key = True,
        autoincrement = True
    )
    
    # Relacion 1-A-Muchos
    # Una Marca tiene muchos Productores.
    
    productos = db.relationship(
        'Producto',
        back_populates = 'marca',
        lazy =  'dynamic'
    )
    
    def __repr__(self):
        return f'<Marca {self.nombre_marca}>'
