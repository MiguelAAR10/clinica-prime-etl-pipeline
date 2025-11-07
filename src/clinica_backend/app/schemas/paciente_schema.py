# src/flask/app/schemas/paciente_schema.py

"""
Schemas de Validación para Paciente usando Marshmallow
"""

# Schema en Marchmallow: Aduana de Datos entre el Mundo externo y tu sistema. Cada vez que algo entra o sale de tu API pasa por este filtro
#   - Genera Meta-estructuras internas:
#
#       1. Mapa de Campos(fields)
#           - Tipo de Dato (estring, integer, boolean, etc)
#           - Si es requerido o puede ser nulo
#           - Que nombre tiene en JSON (data_key)
#           - Como convertirlo en Python (Attribute)
#
#       2. Registrar los Validadores (@validates) y hooks(post_load) para ejecutarlos en orden correcto
#           
#       3. Crea Metodos load() y dump() para transformar:
#           - load(): JSON -> Python (Entrada de Datos)
#           - dump(): Python -> JSON (Salida de Datos)

from app import ma  # Importamos la instancia 'ma' de Marshmallow

from flask.app.models.paciente import Paciente

from marshmallow import Schema, fields, validates, ValidationError, post_load
    #`Schema` -> Es la Clase Base define que campos esperas, como deben lucir que reglas se deben cumplir
    # `fields` -> Contiene tipos de Campo (Bloques de Construccion): `fields.Str(required = True)`
    # @validates -> Es un decrador especializado en Validar un campo especifico dentro de un Schema (Guardia de Seguridad en la puerta de Cada campo)
    # ValidationError -> Excepcion que lanzas cuando un campo no cumple las reglas
    # @post_load -> Decorador para un metodo que se ejecuta despues de que todos los campos han sido validados (Ultima linea de defensa)
    
from datetime import date

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. EL SCHEMA BASE (El ADN de la Validación)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Define todos los campos y validaciones que se
# COMPARTEN entre Crear y Actualizar.
#
# Nota la traducción:
# variable_python (snake_case) = fields.Tipo(data_key='jsonKeyCamelCase')
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PacienteBaseSchema(Schema):
    """
    Schema base con Campos Comunes
    """
    dni = fields.Str(required=True)
    nombreCompleto = fields.Str(required=True, data_key = 'nombreCompleto')
    sexo = fields.Str(allow_none=True)
    telefono = fields.Str(allow_none=True)
    idDistrito = fields.Int(allow_none=True, data_key='idDistrito')
    nacimientoYear = fields.Int(allow_none=True, data_key='nacimientoYear')
    nacimientoMonth = fields.Int(allow_none=True, data_key='nacimientoMonth')
    nacimientoDay = fields.Int(allow_none=True, data_key='nacimientoDay')
    pacienteProblematico = fields.Bool(missing=False, data_key='pacienteProblematico')
    
    @validates('dni')
    def validate_dni(self, value):
        """
        Valida Formato del DNI
        
        Args: 
            value (str): DNI a Validar
        
        Raises:
            ValidationError: Si el DNI es Invalido
        """
        
        if not value or len(value.strip()) == 0:
            raise ValidationError('El DNI no puede estar vacio.')

        if len(value) < 8:
            raise ValidationError('El DNI debe tener al menos 8 caracteres.')

        if not value.isdigit():
            raise ValidationError('El DNI debe contener solo numeros.')
    
    @validates('nombreCompleto')
    def validate_nombre(self, value):
        """
        Valida que el Nombre Completo no este Vacio
        
        Args:
            value (str): Nombre Completo a Validar
        
        Raises:
            ValidationError: Si el Nombre Completo es Vacio
        """
        if not value or len(value.strip()) < 3:
            raise ValidationError('El nombre completo no puede estar vacio.')
    
    @validates('sexo')
    def validate_sexo(self, value):
        """
        Valida que el Sexo sea Correcto

        Args:
            value (str): Sexo a Validar

        Raises:
            ValidationError: Si el Sexo es Invalido
        """
        if value is not None and value not in ['M', 'F', 'Otro']:
            raise ValidationError('El sexo debe ser "M", "F" o "Otro".')
    
    @validates('nacimientoMonth')
    def validate_nacimientoMonth(self, value):
        """
        Valida que el Mes de Nacimiento Sea Correcto

        Args:
            value (int): Mes del Year que Nacio

        Raises:
            ValidationError: Si el Mes de Nacimiento es Invalido
        """

        if value is not None and value not in range(1,13):
            raise ValidationError('El Mes debe ser un número entre el 1 y el 12')
    
    @validates('nacimientoDay')
    def validate_day(self, value):
        """Valida día de nacimiento"""
        if value is not None and (value < 1 or value > 31):
            raise ValidationError('Día debe estar entre 1 y 31')
    
    @post_load
    def validate_fecha_completa(self, data, **kwargs):
        """
        Valida que la fecha de nacimiento sea válida si está completa

        Se ejecuta Después de Validar Campos Individuales
        """

        year = data.get('nacimientoYear')
        month = data.get('nacimientoMonth')
        day = data.get('nacimientoDay')

        if year and month and day:
            try:
                date(year, month, day)
            except ValueError:
                raise ValidationError({
                    'fecha': 'Fecha de Nacimiento Inválida'
                })
        return data
    

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. SCHEMAS DE ENTRADA (Validación / Carga)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PacienteCreateSchema(PacienteBaseSchema):
    """
    Schema para CREAR un paciente.
    Hereda todas las reglas de PacienteBaseSchema.
    Los campos 'required=True' se aplican.
    """
    class Meta:
        # Le dice a Marshmallow que use las llaves de Python
        # (snake_case) del modelo al cargar.
        load_instance = True 
        model = Paciente
        exclude = ('id_paciente',) # No podemos crear con un ID

class PacienteUpdateSchema(PacienteBaseSchema):
    """
    Schema para ACTUALIZAR un paciente.
    Hereda todas las reglas de PacienteBaseSchema.
    
    En el SERVICIO, llamaremos a esto con 'partial=True'
    para permitir actualizaciones parciales (solo enviar el 'telefono').
    """
    class Meta:
        load_instance = True
        model = Paciente
        exclude = ('id_paciente', 'dni') # No permitimos cambiar DNI en un UPDATE

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. SCHEMA DE SALIDA (Serialización / Descarga)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Este es el que define cómo se VE tu API (las respuestas GET)

class PacienteSchema(PacienteBaseSchema):
    """
    Schema para LEER (serializar) un paciente.
    Hereda los campos base Y añade los campos de
    solo lectura (calculados, IDs, timestamps).
    
    ¡Nota que aquí SÍ usaste 'data_key' correctamente! ¡Bien hecho!
    """
    
    id_paciente = fields.Int(
        dump_only=True,         # dump_only = Solo Lectura (no se puede cargar)
        data_key='idPaciente'
    )
    
    # Campos calculados de tu Modelo (de @property)
    edad = fields.Int(dump_only=True)
    
    fecha_nacimiento = fields.Str(
        dump_only=True, 
        data_key='fechaNacimiento'
    )
    
    alertas = fields.List(fields.Str(), dump_only=True)
    
    # Timestamps
    created_at = fields.DateTime(
        dump_only=True, 
        data_key='createdAt'
    )
    
    # Datos de la Relación (¡Magia!)
    # Le decimos que use el 'DistritoSchema' (que crearemos)
    # para el campo 'distrito' del modelo.
    # distrito = fields.Nested('DistritoSchema', dump_only=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INSTANCIAS (Listas para usar en la app)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Exportamos instancias listas para ser importadas
# por el Servicio y las Rutas.

paciente_schema = PacienteSchema()               # Para UN paciente (GET /id)
pacientes_schema = PacienteSchema(many=True)       # Para MUCHOS pacientes (GET /)
paciente_create_schema = PacienteCreateSchema()  # Para CREAR (POST /)
paciente_update_schema = PacienteUpdateSchema()  # Para ACTUALIZAR (PUT /id)