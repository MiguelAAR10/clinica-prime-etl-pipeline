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