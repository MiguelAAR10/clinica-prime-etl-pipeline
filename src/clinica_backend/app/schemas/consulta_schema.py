# src/clinica_backend/app/schemas/consulta_schema.py

from app.extensions import ma
    # `ma` una instancia de Marshmallow configurada para trabajar  con SQLAlchemy (ORM)

from app.models.consulta import (
    Consulta, 
    ConsultaServicio,
    ConsumoProducto
    )
"""
¿QUÉ SON ESTOS MODELOS?
------------------------
Son clases Python que representan tablas SQL en la base de datos.

    ¿POR QUÉ IMPORTAR LOS MODELOS?
------------------------------
Porque SQLAlchemyAutoSchema necesita saber:
- Qué columnas tiene la tabla
- Qué tipo de datos son
- Qué relaciones existen
"""

from marshmallow import fields, validate, EXCLUDE
"""
¿QUÉ ES 'fields'?
-----------------
Son los tipos de datos que Marshmallow puede validar.

Ejemplos:
- fields.Integer() → Valida números enteros
- fields.String() → Valida texto
- fields.Decimal() → Valida números decimales
- fields.Date() → Valida fechas
- fields.List() → Valida listas/arrays
- fields.Nested() → Valida objetos anidados

ANALOGÍA: Tipos de Enchufes
----------------------------
- fields.Integer = Enchufe de 2 patas
- fields.String = Enchufe de 3 patas
- fields.Decimal = Enchufe industrial

Si intentas meter un enchufe de 3 patas en uno de 2,
Marshmallow dice: "Error: tipo incorrecto".

¿QUÉ ES 'validate'?
-------------------
Son reglas adicionales para los campos.

Ejemplos:
- validate.Range(min=0, max=100) → Número entre 0 y 100
- validate.Length(min=1, max=50) → Texto de 1 a 50 caracteres
- validate.OneOf(['A', 'B']) → Solo puede ser 'A' o 'B'
- validate.Email() → Debe ser email válido

ANALOGÍA: Reglas del Juego
---------------------------
- fields.Integer = "Debe ser un número"
- validate.Range(min=0) = "Además, debe ser positivo"

¿QUÉ ES 'EXCLUDE'?
------------------
Es una estrategia para manejar campos desconocidos.

Ejemplo:
Frontend envía:
{
    "id_paciente": 1,
    "campo_inventado": "hola"  ← No existe en el modelo
}

Opciones:
1. EXCLUDE → Ignora 'campo_inventado' (tu elección)
2. RAISE → Lanza error "Campo desconocido"
3. INCLUDE → Acepta el campo (peligroso)

¿POR QUÉ EXCLUDE?
-----------------
Porque el frontend puede enviar datos extra (ej: tokens, flags)
que no necesitas guardar en la DB.

EXCLUDE = "Solo toma lo que necesito, ignora el resto"
    
"""

class ConsumoProductoSchema(ma.SQLAlchemyAutoSchema):
    """
    Valida:
        - Valida Cada linea individual
    """
    class Meta:
        """
        Clase Interna que configura el comportamiento de Schema.
        
        Metadata: Datos sobre Datos
        
        - Analogia:
            - model: Tipo de Papel
            - load_instance: Imprimir a blanco o negro?
            - unknown: Que hacer con pagina Extra
        """
        model = ConsumoProducto
        # Model Usa Estrucutra de Model (Tabla) lee las columnas de ConsumoProducto, Crea campos deValidacion para cada columna. Infieraa los Tipos de Datos.
        
        load_instance = False
        """
        ¿QUÉ HACE 'load_instance'?
        ---------------------------
        Controla QUÉ devuelve el schema después de validar.
        
        load_instance = True:
            schema.load(data)
            # Devuelve: Objeto ConsumoProducto (instancia de SQLAlchemy)
            # Listo para hacer db.session.add(objeto)
        
        load_instance = False:
            schema.load(data)
            # Devuelve: Diccionario Python puro
            # {'id_producto': 10, 'cantidad': 1.5, ...}
        
        ¿POR QUÉ False EN TU CASO?
        --------------------------
        Porque en tu servicio (consulta_service.py) TÚ creas
        los objetos manualmente:
        
            data = schema.load(json_data)  # Diccionario
            nuevo_consumo = ConsumoProducto(**data)  # Tú creas el objeto
            db.session.add(nuevo_consumo)
        
        Ventaja: Más control sobre la creación del objeto.
        
        ¿CUÁNDO USAR True?
        ------------------
        Para operaciones simples:
        
            data = {"id_producto": 10, "cantidad": 1}
            consumo = schema.load(data)  # Ya es un objeto
            db.session.add(consumo)
            db.session.commit()
        
        Más rápido, menos código.
        """
        
        unknown = EXCLUDE
        
    id_producto = fields.Integer(
        required = True
        )
    
    """
    ¿POR QUÉ REDEFINIR ESTE CAMPO?
    -------------------------------
    Porque aunque SQLAlchemyAutoSchema crea campos automáticamente,
    a veces necesitas AGREGAR validaciones extra.
    
    SINTAXIS COMPLETA:
    ------------------
    fields.Integer(
        required=True,           # ¿Es obligatorio?
        allow_none=False,        # ¿Puede ser null?
        validate=None,           # Validaciones extra
        error_messages={},       # Mensajes de error personalizados
        load_default=None,       # Valor por defecto al cargar
        dump_default=None        # Valor por defecto al serializar
    )
    
    ¿QUÉ HACE 'required=True'?
    --------------------------
    Si el JSON no incluye 'id_producto', Marshmallow rechaza:
    
    # JSON sin id_producto:
    {"cantidad": 1, "precio": 100}
    
    # Error:
    {
        "id_producto": ["Missing data for required field."]
    }
    
    ¿POR QUÉ Integer?
    -----------------
    Porque id_producto es una Foreign Key (número entero).
    
    Marshmallow valida:
    ✓ "10" → Convierte a 10 (acepta strings numéricos)
    ✓ 10 → Acepta
    ✗ "hola" → Rechaza ("Not a valid integer")
    ✗ 10.5 → Rechaza ("Not a valid integer")
    ✗ null → Rechaza (required=True)
    """
    
    cantidad_consumida = fields.Decimal(
        required = True,
        validate = validate.Range(min =0.01)
        )
    
    """
    ¿POR QUÉ Decimal Y NO Float?
    ----------------------------
    Ya lo vimos antes: precisión decimal para dinero/inventario.
    
    ¿QUÉ HACE validate.Range(min=0.01)?
    -----------------------------------
    Valida que el número sea >= 0.01
    
    SINTAXIS COMPLETA:
    ------------------
    validate.Range(
        min=0.01,                # Mínimo (inclusive)
        max=None,                # Máximo (None = sin límite)
        min_inclusive=True,      # ¿Incluir el mínimo?
        max_inclusive=True,      # ¿Incluir el máximo?
        error="Mensaje custom"   # Mensaje de error
    )
    
    EJEMPLOS:
    ---------
    ✓ 0.01 → Acepta (justo en el mínimo)
    ✓ 1.5 → Acepta
    ✓ 1000 → Acepta
    ✗ 0 → Rechaza ("Must be greater than or equal to 0.01")
    ✗ -5 → Rechaza
    ✗ "hola" → Rechaza (ni siquiera es número)
    
    ¿POR QUÉ min=0.01 Y NO min=0?
    -----------------------------
    Porque una cantidad de 0 no tiene sentido lógico.
    Si no consumiste nada, no deberías registrar el consumo.
    
    Regla de negocio: "Toda cantidad debe ser positiva"
    """ 
    precio_producto = fields.Decimal(
        required = True, 
        validate = validate.Range(min = 0)
    )
    

# Schema para El Servicio Aplicado (Nivel Medio)
class ConsultaServicioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ConsultaServicio
        load_instance = False # Devuelve Diccionario Python ya que permite más control
        unknown = EXCLUDE
    
    id_servicio = fields.Integer(
        required = True
    )
    
    precio_servicio = fields.Decimal(
        required = True,
        validate = validate.Range(min = 0)
    )
    
    # Lista Anidad de Productos
    productos_usados = fields.List(
        fields.Nested(ConsumoProductoSchema),
        required = False,
        load_default = []  
    )
    
    """
    ------------------
    
    1. fields.List(...)
       ----------------
       Valida que 'productos_usados' sea una LISTA (array).
       
       ✓ []
       ✓ [{"id_producto": 10, ...}]
       ✓ [{"id_producto": 10, ...}, {"id_producto": 11, ...}]
       ✗ {"id_producto": 10}  ← No es lista
       ✗ "hola"  ← No es lista
       ✗ 123  ← No es lista
    
    2. fields.Nested(ConsumoProductoSchema)
       ------------------------------------
       Valida que CADA elemento de la lista sea un objeto
       que cumpla con ConsumoProductoSchema.
       
       ANALOGÍA: Cajas dentro de Cajas
       --------------------------------
       - Lista = Caja grande
       - Nested = Cada caja pequeña dentro debe tener
                  la forma de ConsumoProductoSchema
       
       Marshmallow hace esto:
       
       for producto in productos_usados:
           ConsumoProductoSchema().load(producto)
           # Si alguno falla, rechaza todo
    
    3. required=False
       --------------
       Un servicio PUEDE no consumir productos.
       
       Ejemplo: "Consulta de Evaluación" (solo mano de obra)
       
       ✓ {"id_servicio": 5, "precio": 500}
         # Sin 'productos_usados' → OK
       
       ✓ {"id_servicio": 5, "precio": 500, "productos_usados": []}
         # Lista vacía → OK
    
    4. load_default=[]
       ---------------
       Si el JSON NO incluye 'productos_usados', Marshmallow
       automáticamente pone una lista vacía.
       
       JSON recibido:
       {"id_servicio": 5, "precio": 500}
       
       Después de validar:
       {
           "id_servicio": 5,
           "precio": 500,
           "productos_usados": []  ← Marshmallow lo agregó
       }
       
       ¿POR QUÉ?
       ---------
       Para que tu código no tenga que hacer:
       
       if 'productos_usados' in data:
           for producto in data['productos_usados']:
               # ...
       
       Siempre puedes asumir que existe:
       
       for producto in data['productos_usados']:  # Siempre funciona
           # ...
    
    EJEMPLO COMPLETO DE VALIDACIÓN:
    --------------------------------
    
    # JSON válido:
    {
        "id_servicio": 5,
        "precio": 500,
        "productos_usados": [
            {"id_producto": 10, "cantidad": 1, "precio": 100}
        ]
    }
    # ✅ Pasa validación
    
    # JSON inválido (producto sin cantidad):
    {
        "id_servicio": 5,
        "precio": 500,
        "productos_usados": [
            {"id_producto": 10, "precio": 100}  ← Falta 'cantidad'
        ]
    }
    # ❌ Error:
    {
        "productos_usados": {
            "0": {  ← Índice del array
                "cantidad_consumida": ["Missing data for required field."]
            }
        }
    }
    
    # JSON inválido (cantidad negativa):
    {
        "id_servicio": 5,
        "precio": 500,
        "productos_usados": [
            {"id_producto": 10, "cantidad": -5, "precio": 100}
        ]
    }
    # ❌ Error:
    {
        "productos_usados": {
            "0": {
                "cantidad_consumida": ["Must be greater than or equal to 0.01."]
            }
        }
    }
    """
    
# ═══════════════════════════════════════════════════════════
# SCHEMA NIVEL 3: ConsultaCreateSchema
# Valida la consulta completa (cabecera + servicios + productos)
# ═══════════════════════════════════════════════════════════

class ConsultaCreateSchema(ma.SQLAlchemyAutoSchema):
    """
    ¿QUÉ VALIDA?
    ------------
    El JSON COMPLETO que envía el frontend:
    
    {
        "id_paciente": 1,
        "notas": "Paciente sensible",
        "fecha_consulta": "2025-01-15",
        "servicios": [
            {
                "id_servicio": 5,
                "precio": 500,
                "productos_usados": [
                    {"id_producto": 10, "cantidad": 1, "precio": 100}
                ]
            }
        ]
    }
    
    ANALOGÍA: Orden Completa de Restaurante
    ----------------------------------------
    - Consulta = Orden completa
    - id_paciente = Mesa #1
    - notas = "Sin cebolla"
    - servicios = Lista de platos
        - Cada plato tiene ingredientes (productos)
    """
    
    class Meta:
        model = Consulta
        load_instance = False
        unknown = EXCLUDE
    
    id_paciente = fields.Integer(required=True)
    
    notas_generales = fields.String(allow_none=True)
    """
    ¿QUÉ ES 'allow_none=True'?
    --------------------------
    Permite que el campo sea null/None.
    
    ✓ {"id_paciente": 1, "notas_generales": "Texto"}
    ✓ {"id_paciente": 1, "notas_generales": null}
    ✓ {"id_paciente": 1}  ← Sin el campo (se convierte a None)
    
    DIFERENCIA CON required=False:
    ------------------------------
    - required=False: El campo puede NO existir en el JSON
    - allow_none=True: El campo puede existir pero ser null
    
    Puedes combinarlos:
    fields.String(required=False, allow_none=True)
    # El campo es opcional, y si existe puede ser null
    """
    
    fecha_consulta = fields.Date(required=False)
    """
    ¿QUÉ HACE fields.Date?
    ----------------------
    Valida y convierte fechas.
    
    FORMATOS ACEPTADOS:
    -------------------
    ✓ "2025-01-15" (ISO 8601)
    ✓ "2025-01-15T10:30:00" (con hora, extrae solo la fecha)
    ✗ "15/01/2025" (formato no estándar)
    ✗ "hola" (no es fecha)
    
    CONVERSIÓN AUTOMÁTICA:
    ----------------------
    JSON: "2025-01-15" (string)
    Después de validar: date(2025, 1, 15) (objeto Python)
    
    ¿POR QUÉ required=False?
    ------------------------
    Porque si no se envía, tu modelo tiene:
    fecha_consulta = db.Column(db.Date, server_default=func.current_date())
    
    PostgreSQL pondrá la fecha actual automáticamente.
    """
    
    # ═══════════════════════════════════════════════════════
    # LISTA ANIDADA DE SERVICIOS (Nivel 2 de anidación)
    # ═══════════════════════════════════════════════════════
    
    servicios = fields.List(
        fields.Nested(ConsultaServicioSchema),
        required=True,
        validate=validate.Length(min=1, error="La consulta debe tener al menos un servicio.")
    )
    """
    DESGLOSE COMPLETO:
    ------------------
    
    1. fields.List(...)
       ----------------
       'servicios' debe ser una lista.
    
    2. fields.Nested(ConsultaServicioSchema)
       -------------------------------------
       Cada elemento de la lista debe cumplir ConsultaServicioSchema.
       
       Y ConsultaServicioSchema tiene:
       productos_usados = fields.List(fields.Nested(ConsumoProductoSchema))
       
       ¡ANIDACIÓN DE 3 NIVELES!
       
       Consulta
         └─ servicios[] (Lista)
             └─ ConsultaServicioSchema
                 └─ productos_usados[] (Lista)
                     └─ ConsumoProductoSchema
    
    3. required=True
       -------------
       Una consulta SIN servicios no tiene sentido.
       
       ✗ {"id_paciente": 1}
         # Error: "Missing data for required field."
       
       ✗ {"id_paciente": 1, "servicios": null}
         # Error: "Field may not be null."
    
    4. validate.Length(min=1, ...)
       ---------------------------
       La lista debe tener AL MENOS 1 elemento.
       
       ✗ {"id_paciente": 1, "servicios": []}
         # Error: "La consulta debe tener al menos un servicio."
       
       ✓ {"id_paciente": 1, "servicios": [{"id_servicio": 5, ...}]}
         # OK
       
       SINTAXIS COMPLETA:
       ------------------
       validate.Length(
           min=1,                    # Mínimo de elementos
           max=None,                 # Máximo (None = sin límite)
           equal=None,               # Exactamente N elementos
           error="Mensaje custom"    # Mensaje de error
       )
       
       EJEMPLOS:
       ---------
       validate.Length(min=1, max=10)
       # Entre 1 y 10 servicios
       
       validate.Length(equal=3)
       # Exactamente 3 servicios
    
    FLUJO DE VALIDACIÓN COMPLETO:
    -----------------------------
    
    JSON recibido:
    {
        "id_paciente": 1,
        "servicios": [
            {
                "id_servicio": 5,
                "precio": 500,
                "productos_usados": [
                    {"id_producto": 10, "cantidad": 1, "precio": 100}
                ]
            }
        ]
    }
    
    Marshmallow hace:
    
    1. Valida 'id_paciente' (Integer, required)
    2. Valida 'servicios' (List, required, min=1)
    3. Para cada servicio en 'servicios':
        a. Valida 'id_servicio' (Integer, required)
        b. Valida 'precio' (Decimal, required, min=0)
        c. Valida 'productos_usados' (List, optional)
        d. Para cada producto en 'productos_usados':
            i. Valida 'id_producto' (Integer, required)
            ii. Valida 'cantidad' (Decimal, required, min=0.01)
            iii. Valida 'precio' (Decimal, required, min=0)
    
    Si TODO pasa → Devuelve diccionario limpio
    Si ALGO falla → Devuelve diccionario de errores
    """
    
# ═══════════════════════════════════════════════════════════
# SCHEMA DE RESPUESTA: ConsultaResponseSchema
# Para serializar (convertir objetos Python → JSON)
# ═══════════════════════════════════════════════════════════

class ConsultaResponseSchema(ma.SQLAlchemyAutoSchema):
    """
    ¿PARA QUÉ SIRVE?
    ----------------
    Los schemas anteriores son para ENTRADA (validar JSON del frontend).
    Este schema es para SALIDA (convertir objetos de DB → JSON).
    
    FLUJO:
    ------
    1. Frontend envía JSON → ConsultaCreateSchema valida
    2. Backend guarda en DB
    3. Backend lee de DB → ConsultaResponseSchema serializa
    4. Frontend recibe JSON
    
    ANALOGÍA: Traductor Bidireccional
    ----------------------------------
    - ConsultaCreateSchema = Español → Inglés (entrada)
    - ConsultaResponseSchema = Inglés → Español (salida)
    """
    
    class Meta:
        model = Consulta
        # NO tiene load_instance (no se usa para cargar)
        # NO tiene unknown (no se usa para validar entrada)
    
    id_consulta = ma.auto_field()
    """
    ¿QUÉ ES 'ma.auto_field()'?
    --------------------------
    Le dice a Marshmallow: "Usa el campo tal cual está en el modelo".
    
    Equivalente a:
    id_consulta = fields.Integer()
    
    Pero más corto y automático.
    
    ¿CUÁNDO USAR auto_field()?
    --------------------------
    Cuando NO necesitas validaciones extra.
    
    Para respuestas, generalmente no necesitas validar
    (porque los datos ya están en la DB y son correctos).
    """
    
    fecha_consulta = ma.auto_field()
    total_historico = ma.auto_field()
    
    """
    EJEMPLO DE USO:
    ---------------
    
    # En tu ruta (route):
    @app.route('/consultas/<int:id>', methods=['GET'])
    def get_consulta(id):
        consulta = Consulta.query.get(id)
        schema = ConsultaResponseSchema()
        return schema.dump(consulta)
    
    # Objeto Python:
    consulta = Consulta(
        id_consulta=1,
        fecha_consulta=date(2025, 1, 15),
        total_historico=Decimal('600.00')
    )
    
    # Después de schema.dump(consulta):
    {
        "id_consulta": 1,
        "fecha_consulta": "2025-01-15",
        "total_historico": "600.00"
    }
    
    ¡Conversión automática de tipos Python → JSON!
    """
    