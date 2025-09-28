-- ======================================================================
-- MIGRACIÓN 001: EL LIBRO MAYOR DE STOCK (VERSIÓN PURIFICADA)
-- ======================================================================

-- Usaremos el modo --single-transaction del orquestador,
-- por lo que BEGIN/COMMIT son opcionales aquí, pero los dejamos por claridad.
BEGIN;

-- PASO 1: LA TABLA 'movimientos_stock'
-- Se añade IF NOT EXISTS para que el script se pueda ejecutar múltiples
-- veces sin fallar si la tabla ya fue creada parcialmente.
CREATE TABLE IF NOT EXISTS movimientos_stock (
    id_movimiento SERIAL PRIMARY KEY,
    id_producto INTEGER NOT NULL REFERENCES productos_catalogo(id_producto),
    tipo_movimiento VARCHAR(10) NOT NULL CHECK (tipo_movimiento IN ('ENTRADA', 'SALIDA')),
    cantidad NUMERIC(10,2) NOT NULL CHECK (cantidad > 0),
    id_consumo_origen INTEGER REFERENCES consumo_productos(id_consumo) UNIQUE,
    fecha_movimiento TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- PASO 2: LA FUNCIÓN 'registrar_salida_stock_por_consumo'
-- Reescrita con la máxima claridad sintáctica.
CREATE OR REPLACE FUNCTION registrar_salida_stock_por_consumo()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $BODY$
BEGIN
    INSERT INTO movimientos_stock (
        id_producto,
        tipo_movimiento,
        cantidad,
        id_consumo_origen
    )
    VALUES (
        NEW.id_producto,
        'SALIDA',
        NEW.cantidad_consumida,
        NEW.id_consumo
    );
    RETURN NEW;
END;
$BODY$;

-- PASO 3: EL TRIGGER 'trig_after_insert_consumo'
-- Se añade IF NOT EXISTS si usas PostgreSQL 14+. Si da error,
-- simplemente borra el trigger anterior con 'DROP TRIGGER IF EXISTS...'
DROP TRIGGER IF EXISTS trig_after_insert_consumo ON consumo_productos;
CREATE TRIGGER trig_after_insert_consumo
    AFTER INSERT ON consumo_productos
    FOR EACH ROW
    EXECUTE FUNCTION registrar_salida_stock_por_consumo();

COMMIT;


