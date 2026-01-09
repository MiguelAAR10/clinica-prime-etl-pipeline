from flask import Blueprint, request
"""
`Blueprint`: Permite crear un Modulo dentro de Flask - Permite Organizar las Rutas  en archivos Separadosen lugar de Tener Todo en un app.py 
"""
from marshmallow import ValidationError
from app.services.consulta_service import ConsultaService
from app.schemas.consulta_schema import ConsultaCreateSchema, ConsultaResponseSchema 
from app.utils.response import APIResponse

consultas_bp = Blueprint('consultas', __name__)

# Instancias de Schemas (Herraminetas de Traduccion)
create_schema = ConsultaCreateSchema()
    # `create_schema`: es estricto. Revisa que vengan los Datos Obligaotrios para CREAR
response_schema = ConsultaResponseSchema()
    # `response_schema`: Es Selectivo. Formatea lo que el Usuario debe ver al Final

@consultas_bp.route('/consultas', methods = ['POST'])
def registrar_consulta(): 
    """
    REGISTRO DE ACTO MEDICO (Transaccional)
    Recibe: Paciente + Servicios + Productos Consumidos
    Accion: Guarda Consula, Detalles, consumos y Dispara TRIGGERS de Inventario
    """
    
    json_data = request.get_json()
    """
    Deserializacion
    -----------------------
    
    `json_data`: El texto plano 
    Texto Inerte (JSON) -> Estructura de Datos Vivas (Diccionarios de Python, Integers, Floats, DateObjects)
    
    """
    
    if not json_data:
        return APIResponse.error("Sin Datos JSON ", 400)
    
    try: 
        # 1. Validacion Estructural (Marshmallow)
        # Verifica que vengan los IDs que los precios sean positivos, etc. 
        data = create_schema.load(json_data)
        """
        `create_schema.load()`: Agente que escanea si pasa se convierte en `data`
        """
        
        # 2. Orquestacion de Negocio (Service)
        # Aqui ocurre la Magia ACID (Todo o Nada)
        nueva_consulta = ConsultaService.crear_consulta_completa(data)
        
        # 3. Respuesta Exitosa
        return APIResponse.success(
            data = response_schema.dump(nueva_consulta),
            message = f"Consulta #{nueva_consulta.id_consulta} registrada exitosamente. Inventario actualizado.",
            status_code = 201
        )
        
    except  ValidationError as e:
        return APIResponse.error(
            "Error de Validacion de Datos",
            400,
            details = e.messages
        )
        
    except ValueError as e:
        # Errores de Logica: "Paciente no existe", "Stock Insuficiente", etc.
        return APIResponse.error(str(e), 400)
    
    except Exception as e:
        # Errores INesperados de Servidor 
        return APIResponse.error("Error interno del servidor", 500, details = str(e))
    