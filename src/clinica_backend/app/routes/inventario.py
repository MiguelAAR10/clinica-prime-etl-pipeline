# src/clinica_backend/app/routers/inventario.py

from flask import Blueprint, request
from marshmallow import ValidationError
from app.services.inventario_service import InventarioService
from app.schemas.inventario_schema import InventarioService 
from app.schemas.inventario_schema import MovimientoStockSchema, MovimientoResponseSchema
from app.utils.response import APIResponse

# Creacion del BluePrint
inventario_bp = Blueprint('inventario', __name__)

# Schemas
entrada_schema = MovimientoStockSchema()
response_schema = MovimientoResponseSchema()
list_schema = MovimientoResponseSchema(many =True)

@inventario_bp.route('/movimientos', methods = ['POST'])
def crear_movimiento():
    """
    Registra un Movimiento Manual
    JSON: {"id_producto": 1, "tipo_movimiento": "SALIDA", "cantida":60}
    """
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("Sin Datos JSON", 400)
    
    try:
        # 1. Validacion de Formato
        data = entrada_schema.load(json_data)
        
        # 2. Ejecucion de Logica 
        nuevo_mov = InventarioService.registrar_movimiento_manual(data)
        
        # 3. Respuesta con Datos Frescos (Incluyendo el Nuevo Stock)
        return APIResponse.success(
            data = response_schema.dump(nuevo_mov),
            message = f"Movimiento {nuevo_mov.tipo_movimiento} registrado exitosamente.",
            status_code = 201
        )
        
    except ValidationError as e:
        return APIResponse.error("Datos Invalidos", 400, details = e.messages)
    except ValueError as e:
        # Errores de lógica (ej: Stock insuficiente)
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error("Error interno del servidor", 500, details=str(e))
    
@inventario_bp.route('/movimientos',methods = ['GET'])
def ver_kardex(id_producto):
    """Ver historial de un producto específico"""
    try:
        historial = InventarioService.obtener_kardex(id_producto)
        return APIResponse.success(list_schema.dump(historial))
    except Exception as e:
        return APIResponse.error(str(e), 500)