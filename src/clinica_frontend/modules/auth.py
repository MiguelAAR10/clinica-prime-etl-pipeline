
# src/clinica_frontend/modules/auth.py
import streamlit as st

def show_auth_ui():
    st.title("Inicio de Sesión")
    
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar Sesión"):
        # Logica de autenticacion (simulada)
        if username == "admin" and password == "admin":
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
