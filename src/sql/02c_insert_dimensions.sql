

  -- Insertar descuentos en un solo statement
INSERT INTO descuentos (codigo_descuento, tipo_descuento, valor) 
  VALUES
    ('DOC100', 'FIJO', 100.00),
    ('CONOCIDOS15', 'PORCENTAJE', 15.00),
    ('RECURRENTE10', 'PORCENTAJE', 10.00),
    ('VERANO2025', 'PORCENTAJE', 20.00)
  ON CONFLICT (codigo_descuento) DO NOTHING;

INSERT INTO medios_de_pago (nombre_m_pago) 
  VALUES
    ('YAPE'),
    ('PLIN'),
    ('TRANSFERENCIA BANCARIA'),
    ('TARJETA DE CREDITO/DEBITO'),
    ('EFECTIVO'),
    ('OTRO')
  ON CONFLICT (nombre_m_pago) DO NOTHING;
