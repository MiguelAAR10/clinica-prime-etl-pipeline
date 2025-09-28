-- ======================================================================
-- MIGRACIÓN 004: RECONSTRUCCIÓN HISTÓRICA DEL LIBRO MAYOR (BACKFILL)
-- Misión: Poblar 'movimientos_stock' basado en los datos que ya existen
--         y luego forzar una sincronización total de 'stock_actual'.
-- ESTE SCRIPT ESTÁ DISEÑADO PARA EJECUTARSE UNA SOLA VEZ.
-- ======================================================================
BEGIN;

-- PASO 1: REGISTRAR LAS 'SALIDAS' HISTÓRICAS
-- Leemos todos los consumos que ocurrieron ANTES de que nuestro sistema
-- de triggers existiera y creamos su correspondiente entrada en el diario.
RAISE NOTICE 'Paso 1/3: Registrando salidas históricas desde consumo_productos...';
INSERT INTO movimientos_stock (
    id_producto,
    tipo_movimiento,
    cantidad,
    id_consumo_origen,
    fecha_movimiento -- Importante: tratamos de usar la fecha de la consulta
)
SELECT
    cp.id_producto,
    'SALIDA',
    cp.cantidad_consumida,
    cp.id_consumo,
    c.fecha_consulta -- Usamos la fecha de la consulta como la fecha del movimiento
FROM consumo_productos cp
-- Unimos con consultas_servicios y consultas para obtener la fecha
JOIN consultas_servicios cs ON cp.id_consulta_servicio = cs.id_consulta_servicio
JOIN consultas c ON cs.id_consulta = c.id_consulta
-- ON CONFLICT: Si por alguna razón este script se ejecuta dos veces,
-- esto previene errores de duplicados. No hará nada si el movimiento
-- para ese consumo ya existe.
ON CONFLICT (id_consumo_origen) DO NOTHING;
RAISE NOTICE '... Salidas históricas registradas.';


-- PASO 2: REGISTRAR LAS 'ENTRADAS' INICIALES
-- Aquí asumimos la lógica de negocio que me diste: "cada producto
-- se stockeó inicialmente con 200 unidades".
RAISE NOTICE 'Paso 2/3: Registrando la carga inicial de inventario (200 unidades por producto)...';
INSERT INTO movimientos_stock (
    id_producto,
    tipo_movimiento,
    cantidad
)
SELECT
    id_producto,
    'ENTRADA',
    200.00
FROM productos_catalogo
-- Esto es para evitar insertar estas 200 unidades cada vez que corres el script.
-- Solo insertará para productos que NO tengan NINGÚN movimiento de ENTRADA todavía.
WHERE id_producto NOT IN (SELECT id_producto FROM movimientos_stock WHERE tipo_movimiento = 'ENTRADA');
RAISE NOTICE '... Carga inicial registrada.';


-- PASO 3: FORZAR LA SINCRONIZACIÓN TOTAL
-- Ahora que el diario 'movimientos_stock' está completo con toda la historia,
-- ejecutamos la misma lógica del backfill que te propuse antes.
RAISE NOTICE 'Paso 3/3: Forzando la sincronización masiva de stock_actual...';
UPDATE productos_catalogo pc
SET stock_actual = subquery.balance
FROM (
    SELECT
        id_producto,
        COALESCE(SUM(
            CASE
                WHEN tipo_movimiento = 'ENTRADA' THEN cantidad
                ELSE -cantidad
            END
        ), 0) AS balance
    FROM movimientos_stock
    GROUP BY id_producto
) AS subquery
WHERE pc.id_producto = subquery.id_producto;
RAISE NOTICE '... Sincronización masiva completada.';

COMMIT;