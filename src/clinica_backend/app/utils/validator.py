from marshmallow import ValidationError
from datetime import date
import re

def validate_past_date(value):
    """Valida que la fecha no sea futura (ej. nacimiento)"""
    if value > date.today():
        raise ValidationError("La fecha no puede estar en el futuro.")

def validate_future_date(value):
    """Valida que la fecha sea futura (ej. cita médica)"""
    if value < date.today():
        raise ValidationError("La fecha no puede estar en el pasado.")

def validate_dni_or_ruc(value):
    """Valida formato DNI (8 dígitos)"""
    if not value:
        return
    
    # Regex simple para 8 dígitos numéricos
    if not re.match(r'^\d{8}$', value):
        raise ValidationError("El DNI debe tener exactamente 8 dígitos numéricos.")