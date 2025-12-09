# src/clinica_backend/app/schemas/inventario_schema.py

from app.extensions import ma # Instancia de Marshmallow configurada para usar SQLAlchemy
#     - Este proporciona:
#         - `autofield`: Crea automáticamente campos de esquema basados en el modelo SQLAlchemy
#         - SQLAlchemyAutoSchema: Clase base para esquemas que mapean modelos SQLAlchemy
#         - Integracion ORM -> JSON: Convierte objetos de base de datos a JSON y viceversa

from app.models.inventario import MovimientoStock 
#   - Importa tu Modelo ORM: MovimientoStock
#   - Contiene:
#       - Definición de tabla y columnas
#       - Relaciones con otras tablas
#       - Métodos CRUD heredados de BaseModel   

from marshmallow import fields, validate, EXCLUDE # Utilidades de Marshmallow
#   - `fields.*`: Definir tipos manuales por ejemplo, String, Integer, Nested, etc.
#   - `validate`: Aplicar Reglas y Validaciones para campos (ej: Longitud
#   - `EXCLUDE`: Configuración para ignorar campos desconocidos durante la deserialización

class MovimientoStockSchema(ma.SQLAlchemyAutoSchema):
    # Hereda `SQLAlchemyAutoSchema`
    #   - Marshmallow lee tu Modelo SQLAlchemy 
    #   - Auto-genera campos automaticamente
    #   - Permite override para validaciones adicionales
    #   - Permite convertir objetos ORM -> JSON
    class Meta:
        model = MovimientoStock # Modelo ORM asociado -> Significado: Mis campos 
        load_instance = False # Devuelve un Dictno un objeto ORM
        unknown = EXCLUDE # Ignorar campos desconocidos al deserializar
    
    # Campos Automativos y solo para la Salida
    id_movimiento = ma.auto_field(dump_only = True)
    fecha_movimiento = ma.auto_field(dump_only = True)
    # `dump_only = True`: El Cliente no puede asignarlos, solo incluye una resuesta
    
    # Validaciones Alineadas con SQL
    id_producto = fields.Integer(required = True)
    
    tipo_movimiento = fields.String(
        required = True,
        validate = validate.OneOf(["ENTRADA", "SALIDA"])
    )
    
    cantidad = fields.Decimal(
        required = True, 
        validate = validate.Range(min = 0.01)
    )
 
# Sub-schema para respuestas que incluye datos del producto    
class MovimientoResponseSchema(MovimientoStockSchema):
    # Nested fields para mostrar nombre del producto en el JSON
    nombre_producto = fields.Function(lambda obj: obj.producto.nombre_producto if obj.producto else None)
    stock_nuevo = fields.Function(lambda obj: obj.producto.stock_actual if obj.producto else None)
    
    
    