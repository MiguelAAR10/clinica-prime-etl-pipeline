# src/clinica_frontend/modules/pacientes_ui.py

import streamlit as st
import pandas as pd
from modules.api_client import api_client
from datetime import datetime

def render_pacientes_page():
    """Renderiza la página completa de gestión de pacientes."""