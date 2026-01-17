
# src/clinica_frontend/modules/pacientes_ui.py

import streamlit as st
import pandas as pd
from modules.api_client import APIClient
from utils.formatters import format_paciente_for_display
from utils.validators import validate_paciente_data

# Instancia del cliente de API
client = APIClient()

def show_pacientes_ui():
    """
    Muestra la interfaz de usuario para la gestión de pacientes.
    """
    st.title("Gestión de Pacientes")

    # Obtener y mostrar pacientes
    if 'pacientes' not in st.session_state:
        st.session_state.pacientes = []

    if st.button("Refrescar Pacientes"):
        result = client.get_pacientes()
        if result["success"]:
            st.session_state.pacientes = result["data"]["data"]
            st.success("Pacientes actualizados.")
        else:
            st.error(f"Error al obtener pacientes: {result['error']}")

    if st.session_state.pacientes:
        df_pacientes = pd.DataFrame(st.session_state.pacientes)
        df_display = df_pacientes.apply(format_paciente_for_display, axis=1)
        st.dataframe(df_display)
    else:
        st.info("No hay pacientes para mostrar. Haz clic en 'Refrescar Pacientes' para cargarlos.")

    st.subheader("Acciones")
    
    action = st.selectbox("Seleccionar Acción", ["Crear Paciente", "Actualizar Paciente", "Eliminar Paciente"])

    if action == "Crear Paciente":
        with st.form("crear_paciente_form"):
            st.header("Crear Nuevo Paciente")
            
            dni = st.text_input("DNI")
            nombre_completo = st.text_input("Nombre Completo")
            telefono = st.text_input("Teléfono")
            id_distrito = st.number_input("ID Distrito", min_value=1, step=1)
            sexo = st.selectbox("Sexo", ["M", "F", "Otro"])
            nacimiento_year = st.number_input("Año de Nacimiento", min_value=1900, max_value=2024, step=1)
            nacimiento_month = st.number_input("Mes de Nacimiento", min_value=1, max_value=12, step=1)
            nacimiento_day = st.number_input("Día de Nacimiento", min_value=1, max_value=31, step=1)

            submitted = st.form_submit_button("Crear Paciente")
            if submitted:
                data = {
                    "dni": dni,
                    "nombreCompleto": nombre_completo,
                    "telefono": telefono,
                    "idDistrito": id_distrito,
                    "sexo": sexo,
                    "nacimientoYear": nacimiento_year,
                    "nacimientoMonth": nacimiento_month,
                    "nacimientoDay": nacimiento_day
                }
                
                is_valid, error_message = validate_paciente_data(data)
                if is_valid:
                    result = client.crear_paciente(data)
                    if result["success"]:
                        st.success("Paciente creado exitosamente.")
                        st.session_state.pacientes.append(result["data"])
                    else:
                        st.error(f"Error al crear paciente: {result['error']}")
                else:
                    st.error(f"Datos inválidos: {error_message}")

    elif action == "Actualizar Paciente":
        if st.session_state.pacientes:
            paciente_options = {p["id"]: f"{p['nombreCompleto']} (ID: {p['id']})" for p in st.session_state.pacientes}
            paciente_id = st.selectbox("Seleccionar Paciente a Actualizar", options=list(paciente_options.keys()), format_func=lambda x: paciente_options[x])
            
            if paciente_id:
                paciente_seleccionado = next((p for p in st.session_state.pacientes if p['id'] == paciente_id), None)
                if paciente_seleccionado:
                    with st.form("actualizar_paciente_form"):
                        st.header(f"Actualizar Paciente: {paciente_seleccionado['nombreCompleto']}")
                        
                        telefono = st.text_input("Teléfono", value=paciente_seleccionado.get("telefono", ""))
                        id_distrito = st.number_input("ID Distrito", min_value=1, step=1, value=paciente_seleccionado.get("idDistrito", 1))

                        submitted = st.form_submit_button("Actualizar Paciente")
                        if submitted:
                            data = {
                                "telefono": telefono,
                                "idDistrito": id_distrito
                            }
                            result = client.actualizar_paciente(paciente_id, data)
                            if result["success"]:
                                st.success("Paciente actualizado exitosamente.")
                                # Actualizar la lista de pacientes en session_state
                                for i, p in enumerate(st.session_state.pacientes):
                                    if p['id'] == paciente_id:
                                        st.session_state.pacientes[i].update(data)
                                        break
                            else:
                                st.error(f"Error al actualizar paciente: {result['error']}")

    elif action == "Eliminar Paciente":
        if st.session_state.pacientes:
            paciente_options = {p["id"]: f"{p['nombreCompleto']} (ID: {p['id']})" for p in st.session_state.pacientes}
            paciente_id = st.selectbox("Seleccionar Paciente a Eliminar", options=list(paciente_options.keys()), format_func=lambda x: paciente_options[x])

            if st.button("Eliminar Paciente Seleccionado"):
                result = client.eliminar_paciente(paciente_id)
                if result["success"]:
                    st.success("Paciente eliminado exitosamente.")
                    st.session_state.pacientes = [p for p in st.session_state.pacientes if p['id'] != paciente_id]
                else:
                    st.error(f"Error al eliminar paciente: {result['error']}")

