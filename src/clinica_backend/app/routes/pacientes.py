# src/clinica_backend/app/routes/pacientes.py
"""
BLUEPRINT DE PACIENTES (El Mesero)
Recibe pedidos (HTTP Requests), se los da al Chef (Service) y entrega el plato (JSON).
"""

from flask import Blueprint, request, current_app
from marshmallow import ValidationError

# 1. IMPORTAMOS EL CHEF (Lógica de Negocio)
# Validado: Coincide con tu estructura de carpetas
from app.services.paciente_service import PacienteService

# 2. IMPORTAMOS LOS GUARDIANES (Schemas)
# Validado: Importación explícita para evitar errores de 'current_app'
from app.schemas.paciente_schema import PacienteSchema, PacienteCreateSchema, PacienteUpdateSchema

# 3. IMPORTAMOS EL EMPAQUETADOR (Respuestas)
from app.utils.response import APIResponse

pacientes_bp = Blueprint('pacientes', __name__)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INSTANCIAS DE SCHEMAS (Para usar dentro de las rutas)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
paciente_schema = PacienteSchema()                      # Para un solo paciente
pacientes_list_schema = PacienteSchema(many=True)       # Para una lista de pacientes
create_schema = PacienteCreateSchema()                  # Validador estricto para crear
update_schema = PacienteUpdateSchema()                  # Validador flexible para actualizar

# --------------------------------------------------------
# ENDPOINT 1: CREAR (POST)
# --------------------------------------------------------
@pacientes_bp.route('/pacientes', methods=['POST'])
def crear_paciente():
    """
    Crea un nuevo paciente en la base de datos.
    """
    # 1. Recibir los ingredientes crudos (JSON)
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos JSON", status_code=400)
    
    try:
        # 2. El Guardián revisa los ingredientes (Validación)
        data_validada = create_schema.load(json_data)
        
        # 3. El Chef cocina (Llamada al Servicio)
        nuevo_paciente = PacienteService.crear_paciente(data_validada)
        
        # 4. Empaquetar para llevar (Serialización)
        result = paciente_schema.dump(nuevo_paciente)
        
        # 5. Entregar al cliente
        return APIResponse.success(
            data=result,
            message="Paciente creado exitosamente",
            status_code=201
        )
    
    except ValidationError as e:
        # Error: El JSON estaba mal formado (ej: DNI con letras)
        return APIResponse.error("Error de validación", status_code=400, details=e.messages)
    except ValueError as e:
        # Error: Regla de negocio rota (ej: DNI duplicado)
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        # Error: Se incendió la cocina (Error de servidor)
        return APIResponse.error(str(e), status_code=500)

# --------------------------------------------------------
# ENDPOINT 2: LISTAR (GET)
# --------------------------------------------------------
@pacientes_bp.route('/pacientes', methods=['GET'])
def get_pacientes():
    """
    Obtiene lista paginada de pacientes.
    Params URL: ?page=1&per_page=10&search=juan
    """
    try:
        # 1. Leer la comanda (Query Params)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', None, type=str)
        distrito_id = request.args.get('distrito_id', None, type=int)
        
        # 2. El Chef prepara el buffet (Servicio)
        # ⚠️ CORRECCIÓN CRÍTICA: El nombre del método es 'listar_pacientes'
        resultado = PacienteService.listar_pacientes(
            page=page, 
            per_page=per_page, 
            search=search,
            distrito_id=distrito_id
        )
        
        # 3. Empaquetar la lista
        items_json = pacientes_list_schema.dump(resultado['items'])
        
        response_data = {
            'items': items_json,
            'pagination': {
                'total': resultado['total'],
                'page': resultado['page'],
                'pages': resultado['pages'],
                'per_page': resultado['per_page']
            }
        }
        return APIResponse.success(data=response_data)
    
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)

# --------------------------------------------------------
# ENDPOINT 3: OBTENER UNO (GET BY ID)
# --------------------------------------------------------
@pacientes_bp.route('/pacientes/<int:id_paciente>', methods=['GET'])
def get_paciente_by_id(id_paciente): 
    try:
        paciente = PacienteService.obtener_paciente(id_paciente)
        
        if not paciente:
            return APIResponse.error("Paciente no encontrado", status_code=404)
        
        # Usamos to_dict_completo() del modelo si queremos datos extra (edad, alertas)
        # O usamos el schema. Usaremos schema por consistencia.
        return APIResponse.success(data=paciente_schema.dump(paciente))

    except Exception as e:
        return APIResponse.error(str(e), status_code=500)

# --------------------------------------------------------
# ENDPOINT 4: ACTUALIZAR (PUT)
# --------------------------------------------------------
@pacientes_bp.route('/pacientes/<int:id_paciente>', methods=['PUT'])
def update_paciente(id_paciente):
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)
    
    try:
        # Validación Parcial (partial=True) permite enviar solo 1 campo (ej: telefono)
        data_validada = update_schema.load(json_data, partial=True)
        
        if not data_validada:
            return APIResponse.error("Sin datos válidos para actualizar", status_code=400)
        
        paciente_actualizado = PacienteService.actualizar_paciente(id_paciente, data_validada)
        
        return APIResponse.success(data=paciente_schema.dump(paciente_actualizado))
    
    except ValidationError as e:
        return APIResponse.error("Error de validación", status_code=400, details=e.messages)
    except ValueError as e:
        status = 404 if "no encontrado" in str(e).lower() else 400
        return APIResponse.error(str(e), status_code=status)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)

# --------------------------------------------------------
# ENDPOINT 5: ELIMINAR (DELETE)
# --------------------------------------------------------
@pacientes_bp.route('/pacientes/<int:id_paciente>', methods=['DELETE'])
def delete_paciente(id_paciente):
    try:
        PacienteService.eliminar_paciente(id_paciente)
        return APIResponse.success(message="Paciente eliminado correctamente")

    except ValueError as e:
        status = 404 if "no encontrado" in str(e).lower() else 400
        return APIResponse.error(str(e), status_code=status)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)