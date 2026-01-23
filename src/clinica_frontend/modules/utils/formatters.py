
# src/clinica_frontend/utils/formatters.py
import pandas as pd

def format_paciente_for_display(paciente_row):
    """
    Formatea una fila de paciente para una visualización más amigable.
    """
    # Desplegar el diccionario de distrito si existe
    distrito = paciente_row.get('distrito', {})
    distrito_nombre = distrito.get('nombre', 'N/A')
    
    # Formatear la fecha de nacimiento si está disponible
    nacimiento = "N/A"
    if paciente_row.get('nacimientoYear') and paciente_row.get('nacimientoMonth') and paciente_row.get('nacimientoDay'):
        nacimiento = f"{int(paciente_row['nacimientoDay'])}/{int(paciente_row['nacimientoMonth'])}/{int(paciente_row['nacimientoYear'])}"

    return pd.Series({
        "ID": paciente_row.get('id', 'N/A'),
        "DNI": paciente_row.get('dni', 'N/A'),
        "Nombre Completo": paciente_row.get('nombreCompleto', 'N/A'),
        "Teléfono": paciente_row.get('telefono', 'N/A'),
        "Distrito": distrito_nombre,
        "Sexo": paciente_row.get('sexo', 'N/A'),
        "Fecha de Nacimiento": nacimiento
    })
