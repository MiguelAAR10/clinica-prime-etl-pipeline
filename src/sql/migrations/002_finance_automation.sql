-- ======================================================================
-- MIGRACIÓN 002: INTELIGENCIA FINANCIERA AUTOMÁTICA
-- Misión: Añadir campos de estado y deuda, y automatizar sus cálculos
-- basados en los pagos y las facturas.
-- ======================================================================
BEGIN;

-- 1. MODIFICACIÓN DE LAS TABLAS EXISTENTES
-- Añadimos columnas con 'ADD COLUMN IF NOT EXISTS' para que el script
-- se pueda ejecutar varias veces sin fallar.
ALTER TABLE facturas 
    ADD COLUMN IF NOT EXISTS estado VARCHAR(20) DEFAULT 'PENDIENTE' CHECK (estado IN ('PENDIENTE', 'PAGADA', 'ANULADA'));

ALTER TABLE pacientes 
    ADD COLUMN IF NOT EXISTS deuda_total_calculada NUMERIC(10,2) DEFAULT 0,
    ADD COLUMN IF NOT EXISTS es_paciente_problematico BOOLEAN DEFAULT FALSE;

-- 2. CREACIÓN DE LA FUNCIÓN 'actualizar_finanzas_post_pago'
CREATE OR REPLACE FUNCTION actualizar_finanzas_post_pago()
RETURNS TRIGGER AS $$
-- DECLARE: Aquí definimos variables locales que usaremos dentro de la función.
DECLARE
    factura_afectada_id INT;
    paciente_afectado_id INT;
    deuda_recalculada NUMERIC;
BEGIN
    -- 'TG_OP' es otra variable MÁGICA. Nos dice qué operación disparó el trigger ('INSERT', 'UPDATE', 'DELETE').
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        -- Si es un pago nuevo o modificado, la factura afectada es la de la nueva fila de pago ('NEW').
        factura_afectada_id := NEW.id_factura;
    ELSIF TG_OP = 'DELETE' THEN
        -- Si se borra un pago, la factura afectada es la de la fila que se borró ('OLD').
        -- 'OLD' representa el estado de la fila ANTES de la operación.
        factura_afectada_id := OLD.id_factura;
    END IF;
    
    -- Lógica para actualizar el estado de la factura.
    UPDATE facturas f
    SET estado = CASE 
        WHEN f.total_neto <= (SELECT COALESCE(SUM(monto_pagado), 0) FROM pagos p WHERE p.id_factura = f.id_factura) 
        THEN 'PAGADA'
        ELSE 'PENDIENTE'
    END
    WHERE f.id_factura = factura_afectada_id
    -- 'RETURNING ... INTO ...': Una cláusula de PostgreSQL muy potente.
    -- Ejecuta el UPDATE y, en lugar de no devolver nada, nos devuelve el valor de 'id_paciente'
    -- de la fila actualizada y lo guarda en nuestra variable 'paciente_afectado_id'.
    RETURNING f.id_paciente INTO paciente_afectado_id;

    -- Lógica para recalcular la deuda total del paciente afectado.
    SELECT COALESCE(SUM(total_neto), 0) INTO deuda_recalculada
    FROM facturas
    WHERE id_paciente = paciente_afectado_id AND estado = 'PENDIENTE';
    
    UPDATE pacientes
    SET 
        deuda_total_calculada = deuda_recalculada,
        es_paciente_problematico = (deuda_recalculada > 500.00) -- El umbral de negocio.
    WHERE id_paciente = paciente_afectado_id;
    
    RETURN NEW; -- O NULL si es un DELETE.
END;
$$ LANGUAGE plpgsql;

-- 3. CREACIÓN DEL TRIGGER 'trig_after_pago_modificado'
CREATE TRIGGER trig_after_pago_modificado
    -- Este trigger se activa con CUALQUIER cambio en la tabla de pagos.
    AFTER INSERT OR UPDATE OR DELETE ON pagos
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_finanzas_post_pago();

COMMIT;