# app/schemas/paciente_schema.py
from app.extensions import ma
from app.models.paciente import Paciente
from marshmallow import fields, validate, EXCLUDE

class PacienteSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema Maestro para Pacientes.
    Maneja la conversión bidireccional: Objeto Python <-> JSON
    """
    class Meta:
        model = Paciente
        load_instance = False
            # Load_instance False- > Devuelve Diccionario 
            # Esto es vital porque el Service espera un diccionario para usar `.get()`
        unknown = EXCLUDE     # Si llegan campos extra basura, los ignora (no rompe)
        
        # ORDEN: Definimos qué campos existen y el orden en el JSON
        fields = (
            "id_paciente", "dni", "nombre_completo", "sexo", 
            "telefono", "nacimiento_year", "nacimiento_month", 
            "nacimiento_day", "paciente_problematico", "created_at",
            "distrito", "edad", "alertas" # Campos calculados o relaciones
        )

    # ─────────────────────────────────────────────────────────────────
    # CAMPOS DE SOLO LECTURA (DUMP_ONLY)
    # Estos campos el usuario NO los envía, los genera el sistema.
    # Esto soluciona tu error de "Invalid fields".
    # ─────────────────────────────────────────────────────────────────
    id_paciente = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    
    # Campos calculados (Vienen de @property en el modelo)
    edad = fields.Integer(dump_only=True)
    alertas = fields.List(fields.String(), dump_only=True)

    # ─────────────────────────────────────────────────────────────────
    # VALIDACIONES PERSONALIZADAS
    # ─────────────────────────────────────────────────────────────────
    dni = fields.String(
        required=True, 
        validate=validate.Regexp(r'^\d{8}$', error="El DNI debe tener 8 dígitos numéricos")
    )
    nombre_completo = fields.String(
        required=True, 
        validate=validate.Length(min=3, error="El nombre es muy corto")
    )
    sexo = fields.String(
        validate=validate.OneOf(["M", "F", "O"], error="Sexo inválido (M, F, O)")
    )

# ─────────────────────────────────────────────────────────────────────
# SUB-SCHEMAS ESPECIALIZADOS (HERENCIA)
# ─────────────────────────────────────────────────────────────────────

class PacienteCreateSchema(PacienteSchema):
    """
    Usado SOLO para validar la creación (POST).
    Hereda todo de PacienteSchema.
    Como definimos id y created_at como dump_only arriba, 
    NO NECESITAMOS EXCLUIRLOS AQUÍ. Marshmallow ya sabe ignorarlos en la entrada.
    """
    pass

class PacienteUpdateSchema(PacienteSchema):
    """
    Usado para actualizaciones parciales (PUT/PATCH).
    El DNI no debería poder cambiarse fácilmente, lo hacemos dump_only aquí.
    """
    dni = fields.String(dump_only=True) # En Update, el DNI es solo lectura