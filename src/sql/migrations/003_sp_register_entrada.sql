-- ======================================================================
-- MIGRACIÓN 003: FUNCIÓN PARA REGISTRAR ENTRADAS DE STOCK
-- Misión: Crear una "receta" segura para añadir inventario al libro mayor.
-- ======================================================================

BEGIN;

-- Se elimina el parámetro p_motivo. La función es ahora más simple.
CREATE OR REPLACE FUNCTION sp_registrar_entrada_stock(
    p_id_producto INT,
    p_cantidad NUMERIC
)
RETURNS void
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF p_cantidad <= 0 THEN
        RAISE EXCEPTION 'La cantidad a ingresar debe ser positiva.';
    END IF;

    -- La inserción ahora es más limpia, sin la columna 'motivo'.
    INSERT INTO movimientos_stock (
        id_producto,
        tipo_movimiento,
        cantidad
    )
    VALUES (
        p_id_producto,
        'ENTRADA',
        p_cantidad
    );

    RAISE NOTICE 'Se registraron % unidades de ENTRADA para el producto %.', p_cantidad, p_id_producto;

END;
$BODY$;

COMMIT;