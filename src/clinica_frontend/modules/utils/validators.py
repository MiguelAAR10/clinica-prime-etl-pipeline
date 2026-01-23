
# src/clinica_frontend/utils/validators.py
from typing import Dict, Any, Tuple

def validate_paciente_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Valida los datos de un paciente.
    
    Args:
        data: Diccionario con los datos del paciente.
        
    Returns:
        Tuple (is_valid, error_message)
    """
    required_fields = ["dni", "nombreCompleto", "telefono", "idDistrito", "sexo", "nacimientoYear", "nacimientoMonth", "nacimientoDay"]
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"El campo '{field}' es requerido."
            
    if not data["dni"].isdigit() or len(data["dni"]) != 8:
        return False, "El DNI debe tener 8 dígitos numéricos."
        
    if not data["telefono"].isdigit() or not (9 <= len(data["telefono"]) <= 15):
        return False, "El teléfono debe tener entre 9 y 15 dígitos numéricos."
        
    if not (1900 <= data["nacimientoYear"] <= 2024):
        return False, "El año de nacimiento no es válido."
        
    if not (1 <= data["nacimientoMonth"] <= 12):
        return False, "El mes de nacimiento no es válido."
        
    if not (1 <= data["nacimientoDay"] <= 31):
        return False, "El día de nacimiento no es válido."
        
    return True, ""

