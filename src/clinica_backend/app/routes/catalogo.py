#src/clinica_backend/app/routes/catalogo.py

#--------------------------------------------------------------------------------
# RUTAS (Blueprints) - Conexion
#   - Como funcionan: 
#       - Requests, schemas, services y respuestas
#   - Que es un Blueprint? seccion del sistema (Como una cajita donde agrupas rutas realacionadas
#   - Cada Modulo tien sus rutas agrupadas , es esclable, ordenado y modular (Mini-microservicio dentro de Flask)
#--------------------------------------------------------------------------------


# ================================================================================
# IMPORTACIONES
# ================================================================================

from flask import Blueprint, request
    # `Blueprint` permite crear moduleos de Rutas
    # `request` trae lo que el cliente envio (JSON, headers, query params)
    # Cliente → HTTP Request → Flask → request.get_json() → Service → Response

from marshmallow import ValidationError
    # Permite Caputar los ERRORES cuando los errores no son validos
    
from app.services.catalogo_service import CatalogoService
    # `CatalogoService` -> Cerebro del Negocio: contiene toda la logica del Negocio
    
from app.schemas.producto_schema import MarcaSchema, ProductoSchema, ProductoCreateSchema 
    # `Schemas` son lo guardianes los porteros los filtros de Datos
'''
    Schema.load()  ← limpia, transforma, valida
       ↓
    dict limpio  ← listo para el servicio
'''

from app.utils.response import APIResponse
    # Encapsula la repsuesta con el formato Estandar 
    
# ================================================================================


# ================================================================================
# BLUEPRINT
# ================================================================================

catalogo_bp = Blueprint('catalogo', __name__)
# Crea el Modulo de rutas llamado `catalago`
# La app principal(create_app) registra este Blueprint con un prefix

# ================================================================================


# ===================================================================================
# SCHEMAS
# ===================================================================================

marca_schema = MarcaSchema()
    # Validar un Jsin qhe llegue por POST
    # Convertir un objeto Marca a JSON (Marca(nombre = 'Loreal) -> Schema.dump() -> JSON)
marcas_list_schema = MarcaSchema(many=True)
    # `many = True`: Transformar una lista de objetos a una Lista de JSONs
producto_schema = ProductoSchema()
    # Sirve para mostrar un producto al Cliente 
productos_list_schema = ProductoSchema(many = True)
    # Sirve para mostrar una lista de productos al Cliente
producto_create_schema = ProductoCreateSchema()
    # Crear un `Schema` aparte ya que al crear un producto:
    #   - Debe enviarse `id_marca`
    #   - No debe enviarse `id_producto`
    #   - Pueden ser obligatorios ciertos campos
    
# ===================================================================================


# ==================================================================================
# ENDPOINT - RUTAS - MARCAS
# ==================================================================================

@catalogo_bp.route('/marcas', methods = ['POST'])
def crear_marca():
    json_data = request.get_json()
    # `request`: Objeto global de Flask qcrea para repreentar la peticion  HTTP actual
    # `.get_json()`: Lee el cuerpo de la peticion, detecta si json es valido, lo convierte a python
    if not json_data:
        return APIResponse.error('No se enviaron datos', 400)

    try:
        data = marca_schema.load(json_data)
        #   - Valida el JSON
        #   - Aplica Regla (Required, length, type)
        #   - Limpia el Input
        #   - Transforma json -> Dict Seguro
        #   - Excluye camps desconocidos
        #   - Previene Ataques (Overposting)
        nueva_marca = CatalogoService.crear_marca(data)
        #   - Service Layer: Verifica Duplicado, Creo Objetp (Marca(**data)), lo agrega a la session, commit, retorna el objeto con el id designado
        #   -  NO debe tener(no SQL, no acceso directo a BD)
        #   -  SI dehe tener(Reglas de Negocio, validaciones internas, interaccion con ORM, commit, rollback)
        return APIResponse.succes(marca_schema.dump(nueva_marca), 201)
        # Serializar el Objeto Marca a JSON para: 
        #   - Evitar exponer atributos internos
        #   - Evitar Devolver objetos Python no Serializables
        #   - Devoluciones Inconsistentes
    
    except ValidationError as e:
        return APIResponse.error("Error de Validacion", 400, details=e.messages)
    except ValueError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error(str(e), 500)
    
@catalogo_bp.route('/marcas', methods = ['GET'])
def listar_marcas():
    try:
        marcas  = CatalogoService.listar_marcas()
        return APIResponse.success(marcas_list_schema.dump(marcas))
    except Exception as e:
        return APIResponse.error(str(e), 500)
# ==================================================================================

# ==================================================================================
# ENDPOINT - RUTAS - PRODUCTOS
# ==================================================================================    

@catalogo_bp.routes('/productos', methods = ['POST'])
def crear_productos():
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error('Sin Datos JSON', 400)
    
    try:
        #Usamos el Schema CREATE (que exige id_marca)
        data = producto_schema.load(json_data)
        nuevo_prod = CatalogoService.crear_producto(data)
        return APIResponse.success(producto_schema.dump(nuevo_prod), "Producto Creado", 201)
    
    except ValidationError as e:
        return APIResponse.error("Error de Validacion", 400. details = e.messages)
    
    except ValueError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error(str(e), 500)
    
@catalogo_bp.route('/productos', methods = ['GET'])
def listar_productos():
    try:
        productos = CatalogoService.listar_productos()
        return APIResponse.sucess(productos_list_schema.dump(productos))
    except Exception as e:
        return APIResponse.error(str(e), 500)