# ======================================================================
# 📖 TALLER DE CONOCIMIENTO V5.1 – EL GRAN GRIMORIO DE ENTIDADES
# ======================================================================

# --- 1. NOMBRES CANÓNICOS (La Única Fuente de Verdad para Servicios) ---
# Definimos los nombres oficiales para cada categoría de servicio.
# Estos son los valores que existirán en nuestra base de datos final.
S_TOXINA         = "Toxina Botulinica"
S_RELLENO_HA     = "Relleno Acido Hialuronico"
S_BIOESTIMULADOR = "Bioestimulador de Colageno"
S_MESOTERAPIA    = "Mesoterapia Skinbooster"
S_ENZIMAS        = "Enzimas Recombinantes"
S_CONSULTA       = "Consulta Medica"
S_PRODUCTO       = "Venta de Producto Dermocosmetico" # Nombre más explícito

# --- 2. LISTA DE PRIORIDAD DE SERVICIOS ---
# Define la jerarquía para resolver transacciones mixtas.
# Si una nota menciona "BOTOX" y "TIZO", el servicio principal será S_TOXINA.
LISTA_DE_PRIORIDAD_SERVICIOS = [
    S_TOXINA,
    S_RELLENO_HA,
    S_BIOESTIMULADOR,
    S_ENZIMAS,
    S_MESOTERAPIA,
    S_CONSULTA,
    S_PRODUCTO
]

# --- 3. GRIMORIO DE MARCAS (La Biblioteca de Huellas Digitales) ---
# La Anatomía: { "MARCA_CANÓNICA": {"servicio": SERVICIO_CANÓNICO, "patrones": [LISTA_DE_REGEX]} }
# Cada patrón está diseñado para ser robusto, usando \b (límite de palabra)
# y manejando errores de tipeo comunes (ej. RADIESSE?).
GRIMORIO_DE_MARCAS = {
    # =======================
    # SERVICIOS DE TRATAMIENTO
    # =======================

    # --- Neurotoxinas ---
    "BOTOX":      {"servicio": S_TOXINA, "patrones": [r'\bBOTOX\b']},

    # --- Rellenos de Ácido Hialurónico ---
    "JUVEDERM":   {"servicio": S_RELLENO_HA, "patrones": [r'\bJUVEDERM\b', r'\bVOLUMA\b', r'\bVOLIFT\b', r'\bVOLBELLA\b', r'\bVOLITE\b', r'\bVOLUX\b']},
    "ART FILLER": {"servicio": S_RELLENO_HA, "patrones": [r'\bART\s?FILLER\b', r'\bFILORGA\b']},
    "CROMA":      {"servicio": S_RELLENO_HA, "patrones": [r'\bCROMA\b', r'\bSAYPHA\b']},

    # --- Bioestimuladores de Colágeno ---
    "HARMONYCA":  {"servicio": S_BIOESTIMULADOR, "patrones": [r'\bHARMONYCA\b']},
    "RADIESSE":   {"servicio": S_BIOESTIMULADOR, "patrones": [r'\bRADIESSE?\b', r'\bRADIESE\b']}, # Radiesse? -> Radiesse o Radies
    "ELLANSE":    {"servicio": S_BIOESTIMULADOR, "patrones": [r'\bELLANSE\b']},

    # --- Mesoterapia / Skinboosters ---
    "NCTF":       {"servicio": S_MESOTERAPIA, "patrones": [r'\bNCTF\b']},
    "JALUPRO":    {"servicio": S_MESOTERAPIA, "patrones": [r'\bJALUPRO\b']}, # Se puede clasificar aquí

    # --- Enzimas ---
    "PB SERUM":   {"servicio": S_ENZIMAS, "patrones": [r'\bPB\s?SERUM\b']},

    # ==================================
    # VENTA DE PRODUCTOS DERMOCOSMÉTICOS
    # ==================================

    "TIZO": {
        "servicio": S_PRODUCTO,
        "patrones": [
            r'\bTIZO\b', r'\bTIZO\s?2\b', r'\bTIZO\s?3\b', r'\bTIZO\s?AM\b', r'\bTIZO\s?TINTED\b',
            r'\bTIZO\s?STICK\b', r'\bTIZO\s?LIPS\b', r'\bTIZO\s?MOISTURIZ' # Abarca todas las variantes de Moisturizing
        ]
    },
    "ISDIN": {
        "servicio": S_PRODUCTO,
        "patrones": [
            r'\bISDIN\b', r'AGE\s?REPAIR', r'FOTOPROTECTOR', r'OIL\s?CONTROL',
            r'COMPACT', r'HYALURONIC\s?CONCENTRATE'
        ]
    },
    "SVR": {
        "servicio": S_PRODUCTO,
        "patrones": [
            r'\bSVR\b', r'SEBIACLEAR', r'VIT\.?\s?C', r'SUN\s?SECURE',
            r'EXTREME', r'CONTORNO\s?DE?\s?OJOS?', r'JABON', r'SENSIFINE'
        ]
    },
    "HYDRAMAX": {
        "servicio": S_PRODUCTO,
        "patrones": [r'HYDRAMAX', r'HIDRA\s?MAX', r'AMPOULE\s?HYDRA']
    },
    "PHYTO":    {"servicio": S_PRODUCTO, "patrones": [r'PHYTO\s?SPOT']},
    "SKINLAB":  {"servicio": S_PRODUCTO, "patrones": [r'SKINLAB']},
    "EYE REFRESH": {"servicio": S_PRODUCTO, "patrones": [r'EYE\s?REFRESH', r'CLEAN\s?EYE', r'EYE\s?C\s?PERFECTION']},
    "B3":       {"servicio": S_PRODUCTO, "patrones": [r'\bB3\b', r'SERUM\s?B3']},
    "MICROPEEL": {"servicio": S_PRODUCTO, "patrones": [r'MICROPEEL', r'MICRO\s?PEELING']},
    "TML":      {"servicio": S_PRODUCTO, "patrones": [r'\bTML\b']} # Top Model Look como producto si se vende
}

# --- 4. GRIMORIO DE SERVICIOS GENÉRICOS ---
# Se aplica DESPUÉS del de marcas. Si no se encontró una marca,
# busca estas palabras clave para asignar un servicio genérico.
GRIMORIO_DE_SERVICIOS = {
    r'\bA\.?\s*HIALURONICO\b': S_RELLENO_HA,
    r'\bBIOESTIMULADOR\b':     S_BIOESTIMULADOR,
    r'\bENZIMAS\b':            S_ENZIMAS,
    r'\bCONSULTA\b':           S_CONSULTA,
    # El patrón de 'PRODUCTO' es deliberadamente simple para capturar
    # ventas de productos no catalogados.
    r'\bPRODUCTO\b':           S_PRODUCTO
}

# --- 5. MAPA DE MARCAS GENÉRICAS POR SERVICIO ---
# La codificación de las nuevas reglas de negocio.
# La llave es el servicio canónico, el valor es la marca canónica por defecto.
MAPA_GENERICOS_POR_SERVICIO = {
    S_RELLENO_HA: "JUVEDERM",
    S_BIOESTIMULADOR: "RADIESSE",
    S_MESOTERAPIA: "NCTF"
    # No añadimos S_TOXINA porque BOTOX es prácticamente el único.
    # No añadimos S_PRODUCTO porque usualmente tienen marca.
}