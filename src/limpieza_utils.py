# ======================================================
# 🏛️ TALLER DE HERRAMIENTAS - limpieza_utils.py (ACTUALIZADO)
# ======================================================
import pandas as pd

import re # Necesitaremos el bisturí de texto



def convertir_a_fechas(df: pd.DataFrame, nombre_columna: str) -> pd.DataFrame:
    
    """
    Convertir una Columna a formato fecha, con manejo de Errores.
    """
    
    print(f"\n ----- Columna a Analizar {nombre_columna} ----- \n")
    
    if nombre_columna in df.columns:
        df[nombre_columna] = pd.to_datetime(df[nombre_columna],format='%Y-%m-%d', errors = 'coerce' )
    else:
        print(f"\n ----- ⚠️Advertencia: No se encontró la columna-----")
    return df


def limpiar_num_cols(df: pd.DataFrame, nombre_col ) -> pd.DataFrame: 
    
    """
    Eliminar Caracteres difernetes a Números
    """
    for col in nombre_col:
        if col in df.columns:
            df[col] = df[col].astype(str) #Asegurar que esta en Formato Texto
            df[col] = df[col].str.replace(r'[^\d.]', '', regex = True)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            print(f'Se convirtio correctamente a numero la columna: {col}')
        else:
            print(f'\n ----- ⚠️Advertencia: No se encontró la columna {col}------')
            
    
    
            

def limpiar_y_convertir_a_numerico(df: pd.DataFrame, nombre_columna: str) -> pd.DataFrame:
    """
    Limpia una columna de texto (quitando no-dígitos) y la convierte a numérico.
    """
    print(f"  -> Aplicando herramienta: 'limpiar_y_convertir_a_numerico' en '{nombre_columna}'...")
    if nombre_columna in df.columns:
        # Primero, nos aseguramos de que todo sea texto para poder usar `.str`
        df[nombre_columna] = df[nombre_columna].astype(str)
        
        # El Bisturí Regex: `str.replace(r'[^\d.]', '', regex=True)`
        # `[^\d.]` significa "encuentra cualquier carácter que NO SEA (`^`) un dígito (`\d`)
        # o un punto literal (`.`)". Lo reemplaza con nada ('').
        # 'S/. 1,500.50' se convierte en '1500.50'.
        df[nombre_columna] = df[nombre_columna].str.replace(r'[^\d.]', '', regex=True)
        
        # `pd.to_numeric` es el conversor de números.
        # `errors='coerce'` convierte cualquier cosa que quede y no sea un número
        # (ej. una celda que solo contenía "CANCELADO", ahora vacía) en `NaN`.
        try:
            df[nombre_columna] = pd.to_numeric(df[nombre_columna], errors='coerce')
        except:
            df[nombre_columna] = pd.to_numeric(df[nombre_columna], errors='coerce')

    else:
        print(f"     ⚠️ Advertencia: No se encontró la columna '{nombre_columna}'. Saltando.")
    return df



def reconstruir_identidades(df: pd.DataFrame) -> pd.DataFrame:
    """
    Usa el DNI para rellenar nombres faltantes y viceversa.
    Usa el método .loc para evitar advertencias y asegurar la modificación.
    """
    print("  -> Aplicando herramienta REFORJADA: 'reconstruir_identidades'...")
    
    # ... (El PASO PREVIO y la CONSTRUCCIÓN DEL MAPA son iguales) ...
    if 'dni' not in df.columns or 'nombre' not in df.columns:
        print("     ⚠️ Advertencia: Columnas 'dni' y/o 'nombre' no existen.")
        return df


    df['dni'] = df['dni'].astype(str).str.replace(r'\.0$', '', regex=True).replace({'<NA>': None, 'None': None, 'nan': None, '': None})
    df['nombre'] = df['nombre'].replace({'<NA>': None, 'None': None, 'nan': None, '': None})
    df_mapa = df.dropna(subset=['dni', 'nombre']).copy()
    mapa_dni_a_nombre = df_mapa.drop_duplicates(subset=['dni'], keep='last').set_index('dni')['nombre']
    mapa_nombre_a_dni = df_mapa.drop_duplicates(subset=['nombre'], keep='last').set_index('nombre')['dni']
    
    print(f"     -> Mapa de la verdad creado con {len(mapa_dni_a_nombre)} DNI únicos.")

    # --- LA CIRUGÍA DE RECONSTRUCCIÓN (LA TÉCNICA DEL MAESTRO) ---
    
    # 1. Rellenar nombres usando el DNI
    #    La Condición: `df['nombre'].isnull()` -> Dame las filas donde el nombre es NULO.
    #    La Columna a Modificar: `'nombre'`
    #    El Valor a Asignar: `df['dni'].map(mapa_dni_a_nombre)` -> La traducción del DNI a nombre.
    condicion_nombre_nulo = df['nombre'].isnull()
    df.loc[condicion_nombre_nulo, 'nombre'] = df.loc[condicion_nombre_nulo, 'dni'].map(mapa_dni_a_nombre)
    print(f"     -> 📜 Se intentó rellenar nombres...")

    # 2. Rellenar DNIs usando el nombre
    condicion_dni_nulo = df['dni'].isnull()
    df.loc[condicion_dni_nulo, 'dni'] = df.loc[condicion_dni_nulo, 'nombre'].map(mapa_nombre_a_dni)
    print(f"     -> 🆔 Se intentó rellenar DNIs...")
    
    return df


# ======================================================================
# 🏛️ CAMPO DE PRUEBAS PARA DEPURACIÓN
# ======================================================================
# La Anatomía: `if __name__ == "__main__":`
# El Propósito del Artesano: Esta es una construcción mágica en Python.
# El código dentro de este `if` SOLO se ejecutará cuando corras este archivo
# .py DIRECTAMENTE. Nunca se ejecutará cuando lo importes desde tu notebook.
# Es el lugar perfecto y seguro para poner código de prueba.

if __name__ == "__main__":
    print("--- 🔬 Iniciando ejecución en modo de prueba directa 🔬 ---")
    
    # 1. Creamos un DataFrame de prueba que simule nuestro problema.
    #    Tiene DNIs duplicados y nombres/DNIs faltantes.
    datos_de_prueba = {
        'dni': ['123', '456', '123', None, '789'],
        'nombre': ['Juan Perez', 'Ana Gomez', None, 'Juan Perez', 'Luis Paez']
        
        # Añade más columnas si tus funciones las necesitan
    }
    df_prueba = pd.DataFrame(datos_de_prueba)
    
    print("\n--- DataFrame de Prueba Inicial ---")
    print(df_prueba)
    
    # 2. Llamamos a la herramienta que queremos depurar.
    print("\n--- Llamando a la función 'reconstruir_identidades'... ---")
    df_resultado = reconstruir_identidades(df_prueba)
    
    # 3. Imprimimos el resultado final.
    print("\n--- DataFrame Resultado ---")
    print(df_resultado)

def convertir_a_categoria(df: pd.DataFrame, lista_columnas: list) -> pd.DataFrame:
    """
    Convierte las columnas especificadas en una lista a tipo 'category'.
    Verifica la existencia de cada columna antes de la conversión para evitar errores.
    """
    print(f"  -> ⚙️  Aplicando herramienta de optimización: 'convertir_a_categoria'...")
    
    # La Anatomía: `for col in lista_columnas:`
    # El Propósito del Artesano: Iteramos sobre la lista de columnas que
    # queremos convertir. Este es el enfoque correcto.
    for col in lista_columnas:
        
        # --- EL PASO DE SEGURIDAD CRÍTICO ---
        # La Anatomía: `if col in df.columns:`
        # El Propósito del Artesano: ANTES de intentar convertir una columna,
        # verificamos si realmente existe en el DataFrame. Esto hace que
        # nuestra función sea robusta y a prueba de errores.
        if col in df.columns:
            df[col] = df[col].astype('category')
            print(f"     -> Columna '{col}' convertida a 'category'.")
        else:
            # Si la columna no existe, no rompemos el programa.
            # Simplemente informamos al artesano y continuamos.
            print(f"     -> ⚠️ Advertencia: La columna '{col}' no se encontró en el DataFrame. Saltando.")
            
    return df



import re

def desglosar_fecha(df: pd.DataFrame, nombre_columna: str, prefijo: str) -> pd.DataFrame:
    """
    Toma una columna de fecha y la desglosa en columnas de año, mes y día.
    Es eficiente porque solo realiza la conversión a datetime una vez.
    """
    print(f"  -> 🗓️  Aplicando herramienta: 'desglosar_fecha' en '{nombre_columna}'...")
    if nombre_columna in df.columns:
        # La conversión a datetime se hace UNA SOLA VEZ y se guarda.
        fecha_dt = pd.to_datetime(df[nombre_columna], errors='coerce')
        
        df[f'{prefijo}_year'] = fecha_dt.dt.year.astype('Int64')
        df[f'{prefijo}_month'] = fecha_dt.dt.month.astype('Int64')
        df[f'{prefijo}_day'] = fecha_dt.dt.day.astype('Int64')
        
        # Eliminamos la columna original después de haberla usado.
        df.drop(columns=[nombre_columna], inplace=True)
        print(f"     -> Columna '{nombre_columna}' desglosada y eliminada.")
    else:
        print(f"     ⚠️ Advertencia: No se encontró la columna '{nombre_columna}'. Saltando.")
    return df


import unicodedata


def _strip_accents(s: pd.Series) -> pd.Series:
    # Normaliza a ASCII, quita acentos y caracteres raros
    return (s.astype(str)
              .fillna("")
              .apply(lambda x: unicodedata.normalize("NFKD", x))
              .str.encode("ascii", "ignore")
              .str.decode("ascii"))

def _prep_text(df: pd.DataFrame, cols_fuente) -> pd.Series:
    if isinstance(cols_fuente, str):
        cols_fuente = [cols_fuente]
    cols_fuente = [c for c in cols_fuente if c in df.columns]
    if not cols_fuente:
        raise ValueError("Ninguna de las columnas fuente existe en el DataFrame.")
    txt = df[cols_fuente].astype(str).agg(" ".join, axis=1)
    txt = _strip_accents(txt).str.upper()
    # Espacios uniformes; dejamos letras/numeros y + para combos (BOTOX+JUVEDERM)
    txt = (txt.str.replace(r"[^A-Z0-9+ ]", " ", regex=True)
              .str.replace(r"\s+", " ", regex=True)
              .str.strip())
    return txt

def extraer_producto_principal(df: pd.DataFrame, cols_fuente, col_salida="producto_principal") -> pd.DataFrame:
    '''
    Escane el texto de toal la columns usando el Catalogo para crear una nueva columna 
    '''
    print(f"  -> 🔬 Regex mejorada: buscando marcas en {cols_fuente}…")

    txt = _prep_text(df, cols_fuente)
    out = pd.Series("OTRO", index=df.index, dtype="object")

    # === DICCIONARIO DE PATRONES (orden = prioridad) ===
    # Usa grupos no capturantes (?: ) y variantes comunes. \b = límite de palabra.
    patrones = [
        # --- TOXINAS botulínicas ---
        (r"\b(?:BOTOX|VISTABEL)\b",                         "BOTOX"),
        (r"\b(?:DYSPORT|ABOBO(?:TULIN|TOX)A?|\bABOBO\b)\b", "DYSPORT"),
        (r"\b(?:XEOMIN|INCOBO(?:TULIN|TOX)A?)\b",           "XEOMIN"),
        (r"\b(?:J(E|I)UVEAU|PRABO(?:TULIN|TOX)A?)\b",       "JEUVEAU"),
        (r"\b(?:NABOTA)\b",                                 "NABOTA"),
        (r"\b(?:NEURONOX)\b",                               "NEURONOX"),
        (r"\b(?:BOTULAX)\b",                                "BOTULAX"),
        (r"\b(?:REVANESSE TOX|LETYBO)\b",                   "LETYBO"),  # según mercado
        # --- BIOESTIMULADORES (CaHA, PLLA, PCL, híbridos) ---
        (r"\b(?:RADIESSE|RADIESE|RADESSE)\b",               "RADIESSE"),
        (r"\b(?:SCULPTRA|PLLA)\b",                          "SCULPTRA"),
        (r"\b(?:ELLANSE|ELLANCE)\b",                        "ELLANSE"),
        (r"\b(?:HARMONYCA|HARMON(Y|I)CA|H ARMONYCA|HA RMONYCA)\b", "HARMONYCA"),  # HA + CaHA (Allergan)
        # --- HA FILLERS (familias y sub-marcas) ---
        (r"\b(?:JUVEDERM|J(U|V)EDERM|VOLUMA|VOLIFT|VOLBELLA|VOLITE|VOLUX)\b", "JUVEDERM"),
        (r"\b(?:RESTYLANE|LYFT|REFYNE|DEFYNE|KYSSE|SKINBOOSTERS? RESTYLANE?)\b", "RESTYLANE"),
        (r"\b(?:BELOTERO|INTENSE|BALANCE|SOFT|VOLUME)\b",   "BELOTERO"),
        (r"\b(?:TEOSYAL|TEOXANE|RHA ?[1-4])\b",             "TEOSYAL"),
        (r"\b(?:STYLAGE)\b",                                 "STYLAGE"),
        (r"\b(?:PRINCESS|SAYPHA|CROMA)\b",                   "CROMA/SAYPHA"),
        (r"\b(?:REVANESSE|VERSA)\b",                         "REVANESSE"),
        (r"\b(?:NEAUVIA)\b",                                 "NEAUVIA"),
        (r"\b(?:YVOIRE)\b",                                  "YVOIRE"),
        (r"\b(?:ALIA?XIN)\b",                                "ALIAXIN"),
        (r"\b(?:ART ?FILLER|ARTFILLER|FILORGA)\b",           "ART FILLER"),
        # --- SKINBOOSTERS / PROFILADO ---
        (r"\b(?:PROFHILO)\b",                                "PROFHILO"),
        (r"\b(?:SUNEKOS)\b",                                 "SUNEKOS"),
        (r"\b(?:NCTF|MESOESTETIC|MESOESTETIC ?NCTF)\b",     "NCTF"),
        # --- ENZIMAS/OTROS ADYUVANTES ---
        (r"\b(?:PB ?SERUM|PBSERUM)\b",                       "PB SERUM"),
        (r"\b(?:TIZO)\b",                                    "TIZO"),
    ]

    # Aplica patrones por prioridad; primera coincidencia gana
    for pat, marca in patrones:
        mask = txt.str.contains(pat, regex=True)
        out = out.mask(mask & (out == "OTRO"), marca)

    df[col_salida] = out
    return df


# --- HERRAMIENTA 1: BISTURÍ DE UNIDADES ---
def extraer_unidades(df, col_fuente) -> pd.DataFrame:
    """
    Extrae la PRIMERA cantidad numérica asociada a una unidad de medida
    conocida ('U', 'Jeringa', 'Caja', etc.) de una columna de texto.
    """
    print(f"  -> Applying Multi-Consumption Extractor to '{col_fuente}'...")
    if col_fuente in df.columns:
                # --- EL HECHIZO MAESTRO DE BÚSQUEDA MÚLTIPLE ---
        # La Anatomía: Es casi idéntico al anterior, pero ahora con
        # dos grupos de captura.
        # Grupo 1 `(\d+(?:\.\d+)?)`: Captura la cantidad (entero o decimal).
        # Grupo 2 `(U|UND...|JERINGA...)`: Captura la UNIDAD que se encontró.
        patron_universal = r'\b(\d+(?:\.\d+)?)\s*(?:U|UND|UNIDADES|JERINGA|J|JERINGAS|CAJA|CAJAS)\b'
        
        # La Anatomía: `.str.findall()`
        # El Propósito del Artesano: Esta es la herramienta mágica. En lugar
        # de devolver solo la primera coincidencia, `findall` devuelve una
        # LISTA de TODAS las coincidencias encontradas en el texto.
        # Como nuestro patrón tiene dos grupos de captura, cada elemento
        # de la lista será una tupla de dos valores: (cantidad, unidad).
        df['consumos_detectados'] = df[col_fuente].str.findall(
            patron_universal,
            flags=re.IGNORECASE
        )
        
        print("     -> ✅ Columna 'consumos_detectados' creada con listas de tuplas (cantidad, unidad).")
    return df
    
    
    """
    Extrae unidades (ej. 50U, 64 UND) de una columna de texto.
    
    print(f"  -> Aplicando bisturí de 'unidades' en '{col_fuente}'...")
    if col_fuente in df.columns:
        pat_unidades = r'(?i)\b(\d+(?:[.,]\d{3})*|\d+)\s*(?:U(?:ND|NID|NIDADES)?)\b'
        df['unidades'] = (df[col_fuente].astype(str)
                                      .str.extract(pat_unidades, expand=False)
                                      .str.replace(r'[.,]', '', regex=True)
                                      .astype('Int64'))
    return df
    """

# --- HERRAMIENTA 2: SENSOR DE DEUDA ---
def marcar_deuda(df: pd.DataFrame, col_fuente: str = 'notas') -> pd.DataFrame:
    """
    Crea una columna booleana 'deuda' si la palabra 'DEUDA' aparece.
    """
    print(f"  -> Aplicando sensor de 'deuda' en '{col_fuente}'...")
    if col_fuente in df.columns:
        df['deuda'] = df[col_fuente].astype(str).str.contains(r'(?i)\bDEUDA\b', na=False)
    return df

# --- HERRAMIENTA 3: EXTRACTOR DE MONTO DE DEUDA ---
def extraer_monto_deuda(df: pd.DataFrame, col_fuente: str = 'notas') -> pd.DataFrame:
    """
    Extrae un monto numérico asociado a la palabra 'DEUDA'.
    """
    print(f"  -> Aplicando extractor de 'monto_deuda' en '{col_fuente}'...")
    if col_fuente in df.columns:
        notas_str = df[col_fuente].astype(str)
        pat1 = r'(?i)DEUDA[^0-9]*[S$\/]*\s*(?:USD|US\$|S\/|\$)?\s*(\d+(?:[.,]\d{3})*(?:[.,]\d{2})?)'
        pat2 = r'(?i)DEUDA[^0-9]*([\d.,]+)\s*(?:USD|US\$|DOLARES?|SOLES?)?'
        monto1 = notas_str.str.extract(pat1, expand=False)
        monto2 = notas_str.str.extract(pat2, expand=False)
        
        monto_combinado = monto1.fillna(monto2).str.replace(r'[.,](?=\d{3}\b)', '', regex=True)
        df['deuda_monto'] = pd.to_numeric(monto_combinado.str.replace(',', '.', regex=False), errors='coerce')
    return df



def consolidar_marcador_problematico(df: pd.DataFrame) -> pd.DataFrame: 
    '''
    Crea una Unica Columna Booleana `paciente_problematico` a partir de do fuentes:
        - Columna `nombre`: Se idnica en algunos Registro entre Parentesisi los     siguiente "(PP)" Indicando esto
        - En la Misma Columns (pp)
    '''
    print( "\n -> consolidating `problematic patient` markers ....")
    
    nombre_contiene_pp = df['nombre'].astype(str).str.contains(r'\(PP\)', na = False)
    
    # `.notnull()` nos da `True` para cualquier fila donde 'pp' NO sea nulo.

    pp_no_es_nulo = df['pp'].notnull() if 'pp' in df.columns else pd.Series(False, index = df.index)
    
    # `|` (La Barra Vertical) es el operador "O" en Pandas
    # El Proposito: un paciente es problmetico (True/False)
    
    df['paciente_problematico'] = nombre_contiene_pp | pp_no_es_nulo 
    
    #Descartamos la column Original 'PP'  ahora que es redundante. 
    if 'pp' in df.columns:
        df.drop(columns = ['pp'], inplace = True)
        
    print("\n -> Columns 'paciente_problematico' creada y 'pp' eliminada " )
    return df

def limpiar_nombre_problematico(df: pd.DataFrame) -> pd.DataFrame: 
        """
        Eliminar el Marcador '(PP)'  y espacios extra de la columna 'nombre'
        """
        print("\n  ->  Cleaning Problematic patient markers from 'nombre' ...")
        if 'nombre' in df.columns: 
            # Usamos el Mismo patron para reemplazarlo con nada y luego limpiar espacios
            df['nombre'] = (df['nombre'].astype(str).str.replace(r'\s*\([^)]*\)', '' , regex = True).str.strip())
        return df
                    



def marcar_deuda_con_contexto_reforjado(df: pd.DataFrame, col_fuente: str = 'notas') -> pd.DataFrame:
    """
    Crea una columna booleana 'deuda_generada' usando una estrategia de
    dos pasos para evitar el error de 'fixed-width look-behind'.
    """
    print(f"  ->  Applying reinforced contextual debt sensor to '{col_fuente}'...")
    if col_fuente in df.columns:
        notas_str = df[col_fuente].astype(str).str.upper()
        
        # --- PASO 1: Marcar TODAS las posibles deudas (El Guardia Ingenuo) ---
        deuda_potencial = notas_str.str.contains(r'\bDEUDA\b', na=False)
        
        # --- PASO 2: Marcar las EXCEPCIONES (La Lista Negra) ---
        # Buscamos los patrones que anulan una deuda.
        patron_excepcion = r'(?:CANCEL[AO]|PAGO)\s+\bDEUDA\b'
        es_excepcion = notas_str.str.contains(patron_excepcion, na=False)
        
        # --- PASO 3: LA LÓGICA FINAL ---
        # Una deuda es real si es una deuda potencial Y NO es una excepción.
        df['deuda_generada'] = deuda_potencial & (~es_excepcion)
        
        print("     -> Columna 'deuda_generada' creada con lógica de contexto reforjada.")
    
    # Renombramos la columna `deuda` si existe de una ejecución anterior.
    if 'deuda' in df.columns:
        df.drop(columns=['deuda'], inplace=True, errors='ignore')
        
    return df

# ======================================================
# 🏛️ TALLER DE HERRAMIENTAS - EL "COALESCE" DE PANDAS
# ======================================================
import pandas as pd

def consolidar_informacion_paciente(df: pd.DataFrame, columnas_a_consolidar: list) -> pd.DataFrame:
    """
    Simula la función COALESCE de SQL a nivel de grupo.
    Para cada paciente (agrupado por DNI), rellena los valores nulos en las
    columnas especificadas usando la información más reciente de otras visitas.
    """
    print(f"  -> ✨ Aplicando COALESCE de Pandas para las columnas: {columnas_a_consolidar}...")
    
    if 'dni' not in df.columns:
        print("     ⚠️ Advertencia: No se encontró la columna 'dni'. Abortando consolidación.")
        return df
    
    # Bucle sobre cada atributo que queremos consolidar (telefono, distrito, etc.)
    for col in columnas_a_consolidar:
        if col in df.columns:
            print(f"     -> Consolidando '{col}'...")
            
            # --- EL HECHIZO MÁGICO ---
            # 1. Agrupar por DNI: Crea "expedientes" para cada paciente.
            # 2. Seleccionar la Columna: Enfócate solo en la columna actual (ej. 'telefono').
            # 3. Transform('last'):
            #    - DENTRO de cada expediente, encuentra el último valor no nulo.
            #    - CREA una nueva columna en memoria donde ese valor se "transmite"
            #      a todas las filas de ese paciente.
            valores_propagados = df.groupby('dni')[col].transform('last')
            
            # --- LA CIRUGÍA DE TRASPLANTE ---
            # `fillna()` rellena los `NaN` en la columna original
            # con los valores de nuestra columna recién creada en memoria.
            # Es como decir: "Si el teléfono de esta visita es nulo,
            # usa el teléfono maestro que encontramos para este paciente".
            df[col] = df[col].fillna(valores_propagados)

    return df

# Funcion para poder Estandarizar el Texto de las Filas a Explorar porfavor

import re
import unicodedata




def estandarizar_texto(df: pd.DataFrame, nombre_columna: str) -> pd.DataFrame: 
    """
    Realiza una limpieza profunda sobre una columna de texto y provee un informe
    de auditoría para asegurar que no se pierda información.
    """
    print(f"\n--- 💧 Aplicando Purificación Profunda (Auditada) en '{nombre_columna}' ---")
    
    if nombre_columna not in df.columns:
        print(f"     ⚠️ Advertencia: No se encontró la columna '{nombre_columna}'. Saltando.")
        return df

    # --- Auditoría Inicial ---
    conteo_antes = df[nombre_columna].notna().sum()
    print(f"     -> 📊 Estado Inicial: {conteo_antes} valores no nulos.")

    # --- El Proceso de Purificación (Sintaxis Moderna) ---
    texto_series = df[nombre_columna].fillna('').astype(str)

    # El Hechizo Moderno para quitar acentos:
    # La Anatomía:
    # 1. `unicodedata.normalize('NFKD', x)`: Descompone 'é' en 'e' + '´'.
    # 2. `.encode('ascii', 'ignore')`: Convierte el resultado a BYTES. Ignora
    #    cualquier cosa que no sea ASCII (el acento '´' es descartado).
    # 3. `.decode('ascii')`: Convierte los BYTES de vuelta a un STRING limpio.
    #    Ahora, el hechizo .decode() se aplica al objeto de BYTES, lo cual es correcto.
    def quitar_acentos(texto: str) -> str:
        return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')

    texto_sin_acentos = texto_series.apply(quitar_acentos)
    
    texto_limpio = (texto_sin_acentos
                    .str.lower()
                    .str.strip()
                   )
    
    df[nombre_columna] = texto_limpio.replace('', None)
    
    # --- Auditoría Final ---
    conteo_despues = df[nombre_columna].notna().sum()
    print(f"     -> 📊 Estado Final:   {conteo_despues} valores no nulos.")
    # ... (lógica de veredicto) ...
           
    perdida_de_datos = conteo_antes - conteo_despues
    if perdida_de_datos < conteo_antes * 0.90: 
           print(f" -> Peridad de Informacion minima")
    else: 
        print(f"\nPerdida de datos: {perdida_de_datos} mayor a lo espera.\nRequiere Revisar!!")
        
    return df



# --- Importando el cerebro desde nuestro taller de conocimiento ---
# Esto asume que 'catalogo_conocimiento.py' está en la misma carpeta 'src'.


# --- HERRAMIENTA 2: EXTRACTOR/INFERIDOR DE SERVICIOS ---
# En `limpieza_utils.py`
import pandas as pd
import re
from src.catalogo import GRIMORIO_DE_MARCAS, GRIMORIO_DE_SERVICIOS, S_TOXINA # Importamos los grimorios
'''
# --- HERRAMIENTA 1: DETECTOR DE MARCAS ---
def extraer_marcas(df: pd.DataFrame, col_fuente: str) -> pd.DataFrame:
    """Escanea el texto y extrae una lista de MARCAS canónicas."""
    print(f"  -> 🏷️  Aplicando Detector de Marcas en '{col_fuente}'...")
    
    def encontrar_marcas(texto: str) -> list:
        if pd.isna(texto): return []
        encontradas = set()
        for marca_canon, data in GRIMORIO_DE_MARCAS.items():
            for patron in data['patrones']:
                if re.search(patron, texto, re.IGNORECASE):
                    encontradas.add(marca_canon)
        return list(encontradas)
    
    df['marcas_detectadas'] = df[col_fuente].apply(encontrar_marcas)
    return df

# --- HERRAMIENTA 2: EXTRACTOR/INFERIDOR DE SERVICIOS ---
def extraer_servicios(df: pd.DataFrame, col_fuente: str) -> pd.DataFrame:
    """
    Extrae una lista de SERVICIOS. Infiere el servicio a partir de las
    marcas detectadas y también busca términos de servicios genéricos.
    """
    print(f"  -> ⚙️  Aplicando Extractor/Inferidor de Servicios en '{col_fuente}'...")
    
    def encontrar_servicios(row) -> list:
        texto = row[col_fuente]
        marcas_ya_detectadas = row['marcas_detectadas']
        
        if pd.isna(texto) and not marcas_ya_detectadas: return []
        
        servicios_encontrados = set()
        
        # 1. Inferir desde las marcas (la lógica más importante)
        for marca in marcas_ya_detectadas:
            servicio_asociado = GRIMORIO_DE_MARCAS[marca]['servicio']
            servicios_encontrados.add(servicio_asociado)

        # 2. Buscar servicios genéricos en el texto
        for patron, servicio_canon in GRIMORIO_DE_SERVICIOS.items():
            if re.search(patron, texto, re.IGNORECASE):
                servicios_encontrados.add(servicio_canon)
        
        # 3. Caso especial para 'botox' que es marca y servicio a la vez
        if "BOTOX" in marcas_ya_detectadas:
             servicios_encontrados.add(S_TOXINA)

        return list(servicios_encontrados)

    # `.apply(..., axis=1)` es crucial. Le dice a Pandas que pase la FILA ENTERA
    # a nuestra función, para que podamos acceder tanto a 'texto_consulta' como a 'marcas_detectadas'.
    df['servicios_realizados'] = df.apply(encontrar_servicios, axis=1)
    return df
'''

# ======================================================
# 🏛️ TALLER DE HERRAMIENTAS - V4.1 (Con Extracción Ordenada)
# ======================================================
from src.catalogo import GRIMORIO_DE_MARCAS, GRIMORIO_DE_SERVICIOS

# --- HERRAMIENTA 1: DETECTOR DE MARCAS (ORDENADO) ---
def extraer_marcas_ordenado(df: pd.DataFrame, col_fuente: str) -> pd.DataFrame:
    """Escanea el texto y extrae una lista de MARCAS canónicas EN EL ORDEN EN QUE APARECEN."""
    print(f"  -> 🏷️  Aplicando Detector de Marcas Ordenado en '{col_fuente}'...")
    
    def encontrar_marcas(texto: str) -> list:
        if pd.isna(texto): return []
        
        # La Anatomía: `re.finditer()`
        # El Propósito del Artesano: En lugar de un simple `search`, `finditer`
        # es un hechizo que encuentra TODAS las apariciones de un patrón
        # y nos devuelve su posición en el texto.
        
        hallazgos = []
        for marca_canon, data in GRIMORIO_DE_MARCAS.items():
            for patron in data['patrones']:
                for match in re.finditer(patron, texto, re.IGNORECASE):
                    # Guardamos la marca y su posición de inicio.
                    hallazgos.append((match.start(), marca_canon))
        
        # Ordenamos los hallazgos por su posición de inicio.
        hallazgos.sort()
        
        # Eliminamos duplicados manteniendo el orden.
        marcas_ordenadas_unicas = []
        for _, marca in hallazgos:
            if marca not in marcas_ordenadas_unicas:
                marcas_ordenadas_unicas.append(marca)
                
        return marcas_ordenadas_unicas
    
    df['marcas_detectadas'] = df[col_fuente].apply(encontrar_marcas)
    return df

# En `limpieza_utils.py`
from src.catalogo import GRIMORIO_DE_MARCAS, GRIMORIO_DE_SERVICIOS, LISTA_DE_PRIORIDAD_SERVICIOS

# (La función `extraer_marcas` puede seguir siendo la ordenada o la simple, no es tan crítico aquí)

def extraer_servicios_jerarquico(df: pd.DataFrame, col_fuente: str) -> pd.DataFrame:
    """
    Extrae una lista de SERVICIOS y la devuelve ORDENADA según la
    jerarquía de negocio definida en LISTA_DE_PRIORIDAD_SERVICIOS.
    """
    print(f"  -> 👑 Aplicando Extractor Jerárquico de Servicios en '{col_fuente}'...")
    
    def encontrar_y_ordenar_servicios(row) -> list:
        texto = row[col_fuente]
        marcas_detectadas = row['marcas_detectadas']
        
        if pd.isna(texto) and not marcas_detectadas: return []
        
        # Usamos un SET para la detección inicial, por su eficiencia y manejo de duplicados.
        servicios_encontrados_set = set()
        
        # 1. Inferir desde las marcas
        for marca in marcas_detectadas:
            servicio_asociado = GRIMORIO_DE_MARCAS.get(marca, {}).get('servicio')
            if servicio_asociado:
                servicios_encontrados_set.add(servicio_asociado)

        # 2. Buscar servicios genéricos
        for patron, servicio_canon in GRIMORIO_DE_SERVICIOS.items():
            if re.search(patron, texto, re.IGNORECASE):
                servicios_encontrados_set.add(servicio_canon)
        
        # 3. EL ORDENAMIENTO FINAL (La Lógica Maestra)
        # La Anatomía: `sorted(lista, key=LISTA_DE_PRIORIDAD.index)`
        # El Propósito del Artesano: Este es un hechizo de ordenamiento avanzado.
        # Le decimos a Python: "Ordena `servicios_encontrados_set`, pero no lo
        # hagas alfabéticamente. En su lugar, para cada servicio, busca su
        # POSICIÓN (`.index()`) en mi `LISTA_DE_PRIORIDAD_SERVICIOS` y
        # ordena basándote en ese número de posición (de menor a mayor)."
        # Es la implementación directa de tu visión.
        servicios_ordenados = sorted(
            list(servicios_encontrados_set),
            key=lambda s: LISTA_DE_PRIORIDAD_SERVICIOS.index(s) if s in LISTA_DE_PRIORIDAD_SERVICIOS else 999
        )
        
        return servicios_ordenados

    df['servicios_realizados'] = df.apply(encontrar_y_ordenar_servicios, axis=1)
    return df


'''
# ======================================================
# 🏛️ TALLER DE HERRAMIENTAS - EL EXTRACTOR DE EVENTOS COMPUESTOS
# ======================================================
import pandas as pd
import re
from src.catalogo import GRIMORIO_DE_MARCAS, LISTA_DE_PRIORIDAD_SERVICIOS

def extraer_eventos_de_consulta(df: pd.DataFrame, col_fuente: str) -> pd.DataFrame:
    """
    Extrae una lista de "objetos" (diccionarios), donde cada objeto representa
    un servicio/producto consumido, con su cantidad y unidad asociadas.
    """
    print(f"  -> ⚛️  Aplicando Extractor de Eventos Compuestos en '{col_fuente}'...")
    
    def encontrar_eventos(texto: str) -> list:
        if pd.isna(texto): return []
        
        # --- 1. Detección de Marcas y sus Posiciones ---
        hallazgos_marcas = []
        for marca_canon, data in GRIMORIO_DE_MARCAS.items():
            for patron in data['patrones']:
                for match in re.finditer(patron, texto, re.IGNORECASE):
                    hallazgos_marcas.append({
                        "posicion": match.start(),
                        "marca": marca_canon,
                        "servicio": data['servicio']
                    })
        
        # --- 2. Detección de Cantidades y sus Posiciones ---
        hallazgos_cantidades = []
        patron_cant = r'\b(\d+(?:\.\d+)?)\s*(U|UND|UNIDADES|JERINGA|JERINGAS|CAJA|CAJAS)\b'
        for match in re.finditer(patron_cant, texto, re.IGNORECASE):
            hallazgos_cantidades.append({
                "posicion": match.start(),
                "cantidad": float(match.group(1)),
                "unidad": match.group(2).upper()
            })
            
        # --- 3. El Algoritmo de Vinculación: "El Vecino Más Cercano" ---
        eventos_finales = []
        for marca_info in sorted(hallazgos_marcas, key=lambda x: x['posicion']):
            evento = {
                "marca_detectada": marca_info['marca'],
                "servicio_inferido": marca_info['servicio'],
                "cantidad_detectada": None,
                "unidad_detectada": None
            }
            
            # Buscamos la cantidad más cercana a la marca
            cantidad_mas_cercana = None
            menor_distancia = float('inf')
            
            for cant_info in hallazgos_cantidades:
                distancia = abs(marca_info['posicion'] - cant_info['posicion'])
                if distancia < menor_distancia and distancia < 20: # Umbral de 20 caracteres
                    menor_distancia = distancia
                    cantidad_mas_cercana = cant_info
            
            if cantidad_mas_cercana:
                evento['cantidad_detectada'] = cantidad_mas_cercana['cantidad']
                # Normalizamos la unidad
                unidad = cantidad_mas_cercana['unidad']
                if unidad in ['U', 'UND', 'UNIDADES']:
                    evento['unidad_detectada'] = 'unidades'
                elif unidad in ['J', 'JERINGA', 'JERINGAS']:
                    evento['unidad_detectada'] = 'jeringas'
                else:
                    evento['unidad_detectada'] = 'cajas' # Asumimos por defecto
                
                # Removemos la cantidad usada para que no se asigne a otra marca
                hallazgos_cantidades.remove(cantidad_mas_cercana)

            eventos_finales.append(evento)
            
        return eventos_finales

    df['eventos_consulta'] = df[col_fuente].apply(encontrar_eventos)
    return df
'''

# ... (dentro de limpieza_utils.py) ...

from src.catalogo import MAPA_GENERICOS_POR_SERVICIO

def asignar_marcas_genericas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Inspecciona las filas donde 'marcas_detectadas' está vacío pero
    'servicios_detectados' no lo está, y asigna una marca genérica
    basada en la lógica de negocio del MAPA_GENERICOS_POR_SERVICIO.
    """
    print("  -> 🤖 Aplicando asignador de marcas genéricas contextuales...")

    # --- La Lógica de Aplicación por Fila ---
    # La Anatomía: `.apply(funcion, axis=1)`
    # El Propósito: `.apply` con `axis=1` es una herramienta poderosa pero lenta.
    # Le dice a Pandas: "Toma cada fila, una por una, y pásala a la
    # función que te doy". Es perfecta para lógicas condicionales complejas
    # que dependen de múltiples columnas en la misma fila.
    def logica_por_fila(fila):
        servicios = fila['servicios_realizados']
        marcas = fila['marcas_detectadas']

        # Condición: Si no hay marcas, PERO sí hay servicios...
        if not marcas and servicios:
            # Iteramos sobre los servicios de esta fila
            for servicio in servicios:
                # Consultamos nuestro mapa de genéricos
                if servicio in MAPA_GENERICOS_POR_SERVICIO:
                    # Si encontramos una regla, añadimos la marca genérica y salimos.
                    marcas.append(MAPA_GENERICOS_POR_SERVICIO[servicio])
                    break # Solo asignamos una marca genérica por fila.
        return marcas # Devolvemos la lista de marcas (modificada o no)

    # Aplicamos la lógica a la columna 'marcas_detectadas'
    df['marcas_detectadas'] = df.apply(logica_por_fila, axis=1)
    
    print("     -> Asignación completada.")
    return df
