
# src/clinica_frontend/app.py

import streamlit as st
from modules.pacientes_ui import show_pacientes_ui
from modules.consultas_ui import show_consultas_ui
from modules.inventario_ui import show_inventario_ui
from modules.auth import show_auth_ui

def main():
    """
    Función Principal de la Aplicación Frontend
    """
    st.set_page_config(
        page_title="MediStock",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # --- Autenticación ---
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        show_auth_ui()
    else:
        # --- Barra Lateral de Navegación ---
        st.sidebar.title("MediStock")
        st.sidebar.markdown("---")
        
        menu = {
            "Pacientes": show_pacientes_ui,
            "Consultas": show_consultas_ui,
            "Inventario": show_inventario_ui
        }
        
        selection = st.sidebar.radio("Menú", list(menu.keys()))
        
        st.sidebar.markdown("---")
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state.authenticated = False
            st.experimental_rerun()

        # --- Contenido Principal ---
        page = menu[selection]
        page()

if __name__ == "__main__":
    main()
