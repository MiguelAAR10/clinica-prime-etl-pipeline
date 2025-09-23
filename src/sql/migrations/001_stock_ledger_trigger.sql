-- MIGRACION 001: -- Stock Ledger 
-- Objetivo: 
-- -- Crear un registro inmutable de Cada movimiento de Stock y automatizar su actulizacion

BEGIN; -- TRANSACTION START (Signifca que debe completar todo o nada)

-- 1. Creacion de la tabla `movimientos stock`
-- Esta es la Unica funete de Verdad del Inventario. No se Borra nada solo se anade 
CREATE TABLE movimientos_stock (
    id_movimiento SERIAL PRIMARY KEY,
    id_producto INT NOT NULL REFERENCES productos_catalogo(id_producto),
    tipo_movimiento VARCHAR(10) NOT NULL CHECK (tipo_movimiento IN ('ENTRADA', 'SALIDA')),
    cantidad NUMERIC(10,2) NOT NULL CHECK (cantidad > 0),
    id_consumo_origen INT REFERENCES
    fecha_movimiento TIMESTAMPTZ NOT NULL DEFAULT NOW()    
);

CREATE INDEX IF NOT EXISTS idx_movimientos_stock_producto ON movimientos_stock(id_producto);

-- 2. CREACION DE LA FUNCION `registrar_salida_stock_por_consumo`
-- Esta es el cerebro que se ejecutara
-- RETURNS TRIGGER: Le dice a PostgreSQL que esta funcion sera usada por un trigger
-- AS $$ ... $$: Delimita el Cuerpo de la funcion 
-- LANGUAGE plpgsql: Especifica el lenguaje de la funcion (El estandar  de Postgres)

CREATE OR REPLACE FUNCTION registrar_salida_stock_por_consumo()
--Instrucciones que estamsos dando -> los pasos a seguir 
RETURN TRIGGER AS $$ -- Delimitacion 
BEGIN -- Inicio del Bloque de logica de la funcion
    -- La logica  principal: Inserta una nueva Fila en nuestro libro mayor.
    INSERT INTO movimientos_stock(
        id_producto,
        tipo_movimiento,
        cantidad,
        id_consumo_origen
    )
    VALUES (
        -- 'NEW' es un variable magica disponible dentro de los triggers
        -- 
        -- Representa la fila que Acaba de Ser insertada en consumo productos
        NEW.id_producto, -- Tomamos el id_producto de la nueva fila de consumo
        'SALIDA', -- Definimps el movimiento como 'SALIDA'
        NEW.cantidad_consumida, -- Tomamos la cnatidad de la nueva fila de consumo 
        NEW.id_consumo -- Creamos un vinculo directo al registro de consumo que causo este movimiento
    );
    --= Todo Trigger debe devolver algo. En un trigger 'AFTER', Devolver un NEW es un buena practica 
    RETURN NEW;
    -- `RETURN` la declaracion que finaliza la ejecucion de la funcion y devuelve un valor 
    --
END;  -- Fin del bloque logico
$$ LANGUAGE plpgsql;

-- 3. CREACIÓN DEL TRIGGER 'trig_after_insert_consumo'
-- Este es el "guardián" que vigila la tabla 'consumo_productos'.
CREATE TRIGGER trig_after_insert_consumo
    AFTER INSERT ON consumo_productos -- EVENTO: Se dispara DESPUÉS de un INSERT en la tabla.
    FOR EACH ROW -- Se ejecuta para cada fila individual que se inserte.
    EXECUTE FUNCTION registrar_salida_stock_por_consumo(); -- ACCIÓN: Llama a la función que creamos arriba.

COMMIT; -- TRANSACTION END: Si todo lo anterior funcionó, los cambios se hacen permanentes.