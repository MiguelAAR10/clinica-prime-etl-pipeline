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

