-- ======================================================================
-- MIGRACIÓN 002: SINCRONIZACIÓN DEL STOCK ACTUAL
-- Misión: Actualizar 'productos_catalogo.stock_actual' cada vez que
--         el libro mayor 'movimientos_stock' cambia.
-- ======================================================================

-- PASO 1: LA FUNCIÓN SINCRONIZADORA
CREATE OR REPLACE FUNCTION sincronizar_stock_actual()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $BODY$
DECLARE
    producto_id INT;
BEGIN
    -- Determinar qué producto fue afectado
    IF TG_OP = 'DELETE' THEN
        producto_id := OLD.id_producto;
    ELSE
        producto_id := NEW.id_producto;
    END IF;

    -- El Corazón: Recalcular el stock sumando ENTRADAS y restando SALIDAS
    UPDATE productos_catalogo
    SET stock_actual = (
        SELECT COALESCE(SUM(
            CASE
                WHEN tipo_movimiento = 'ENTRADA' THEN cantidad
                ELSE -cantidad
            END
        ), 0)
        FROM movimientos_stock
        WHERE id_producto = producto_id
    )
    WHERE id_producto = producto_id;

    RETURN NULL; -- Para triggers AFTER ROW que no modifican la fila, NULL está bien.
END;
$BODY$;

-- PASO 2: EL TRIGGER QUE VIGILA EL DIARIO
DROP TRIGGER IF EXISTS trig_after_movimiento_stock ON movimientos_stock;

CREATE TRIGGER trig_after_movimiento_stock
    AFTER INSERT OR UPDATE OR DELETE ON movimientos_stock
    FOR EACH ROW
    EXECUTE FUNCTION sincronizar_stock_actual();