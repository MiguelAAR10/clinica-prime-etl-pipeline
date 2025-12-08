#src/clinica_backend/app/schemas/catalogo_schema.py

'''
SCHEMA: 
    Que es un Schema?
        - Filtro/ Vigilante/ Portero
        - Conversor entre `SQL` <-> `PYTHON` <-> `JSON`  
        - Verifica que entra y sale de la API
        - Almacen necesita:
           1. orden
           2. estructura
           3. claves primarias
           4. tipos de Datos  
'''

from app.extensions import ma
from app.models.producto import Producto
from app.models.marca import Marca
from marshmallow import fields, validate, EXCLUDE

# ----------------------------------------------------------------------
# SCHEMA MARCA
# ----------------------------------------------------------------------

class MarcaSchema(ma.SQLAlchemyAutoSchema):
    # `ma.SQLAlchemyAutoSchema` crea automáticamente los campos basados en el modelo SQLAlchemy ( Significa voy a leetu Modelo SQLAlchemy (La Clase Marca) y voy a generar automaticamente los campos que corresponden a sus atributos)
    #       - Este funciona de la Siguiente Manera: 
    #         1. Crea los campos automáticamente según el modelo SQLAlchemy.
    #         2. Luego, los campos definidos explícitamente en la clase Schema sobrescriben los creados automáticamente.    
    
    class Meta:
        model = Marca # Los campos tiene que venir del Modelo `Marca` de SQLALchemy
        load_instance = False # IMPORTANTE!! Devuelve Dict no objeto
            # `Schema` NO crea Modelos
            # `Schema` NO toca la base de datos
            
        unknown = EXCLUDE # IMPORTANTE!! Ignora los campos que no están en el modelo
            # Si el Cliente envia campos que NO existen en el Schema ignoralos
    
    id_marca = ma.auto_field(dump_only = True) # `autofield` Crea un campo basaado en l oque diceel Modelo SQLAlchemy
        # `dump_only` = True -> Este campo solo se usa la mostar datos NO se acepta del usuario
    
    nombre_marca = fields.String(
        required = True,
        validate = validate.Length(min = 2)
    )
    
    # `fields.String` Indica que dbee ser Texto
    # `required` = True -> Este es obligaotio 

# ------------------------------------
# SCHEMA DE PRODUCTO
# ------------------------------------
class ProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        load_instance = False
        unknown = EXCLUDE

    id_producto = ma.auto_field(dump_only=True)
    
    # Validaciones de Negocio
    nombre_producto = fields.String(required=True, validate=validate.Length(min=3))
    costo_unitario = fields.Decimal(as_string=False, validate=validate.Range(min=0))
    precio_venta = fields.Decimal(as_string=False, validate=validate.Range(min=0))
    
    # Relación: Queremos ver el nombre de la marca, no solo el ID
    # Nested permite incrustar el JSON de la marca dentro del producto
    marca = fields.Nested(MarcaSchema, only=('id_marca', 'nombre_marca'), dump_only=True)

class ProductoCreateSchema(ProductoSchema):
    # Al crear, exigimos el ID de la marca
    id_marca = fields.Integer(required=True)

class ProductoUpdateSchema(ProductoSchema):
    pass

from app.models.servicio import Servicio

# ──────────────────────────────────────────────────────────
# 4. SCHEMA DE SERVICIO
# ──────────────────────────────────────────────────────────
class ServicioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Servicio
        load_instance = False
        unknown = EXCLUDE

    id_servicio = ma.auto_field(dump_only=True)
    nombre_servicio = fields.String(required=True, validate=validate.Length(min=3))
    precio_servicio = fields.Decimal(as_string=False, validate=validate.Range(min=0))