#src/clinica_backend/app/models/servicio.py

'''
MODELO SERVICIO
Representa la mano de obra de procedimientos 
A diferencia de Producto el serivico no tiene stcok Fisico
'''

from app.extensions import db
from app.models.base import BaseModel

class Servicio(BaseModel):
    
    __tablename__ = 'servicios_catalogo'
    id_servicio = db.Column(db.Integer, primary_key = True )
    nombre_servicio = db.Column(db.String(250), unique =True, nullable = False)
    precio_servicio = db.Column(db.Numeric(10,2))

    def __repr__(self):
        return f'<Servicio {self.nombre_servicio} - ${self.precio_servicio}>'    