-- Paso 0: limpiar (ejecuta en llamada aparte si quieres vaciar siempre)
-- TRUNCATE TABLE consumo_productos;

-- Paso 1: generar raw_explotado
CREATE TEMP TABLE raw_explotado AS
WITH raw_explotado_inicial AS (
    SELECT
        rd.dni,
        rd.fecha::date,
        regexp_replace(marca,    '[^A-Z0-9\s]', '', 'g') AS nombre_marca_sucio,
        regexp_replace(servicio, '[^A-Z0-9\s]', '', 'g') AS nombre_servicio_sucio,
        regexp_replace(consumo,  '[^A-Z0-9\s]', '', 'g') AS cantidad_consumida_sucia
    FROM raw_data AS rd
    CROSS JOIN LATERAL unnest(
        regexp_split_to_array(upper(trim(rd.marcas_detectadas)),   ',\s*'),
        regexp_split_to_array(upper(trim(rd.servicios_realizados)),',\s*'),
        regexp_split_to_array(upper(trim(rd.consumos_detectados)), ',\s*')
    ) AS u(marca, servicio, consumo)
)
SELECT
    dni,
    fecha,
    CASE
        WHEN nombre_marca_sucio <> '' THEN nombre_marca_sucio
        WHEN nombre_servicio_sucio LIKE '%RELLENO%'        THEN 'JUVEDERM'
        WHEN nombre_servicio_sucio LIKE '%BIOESTIMULADOR%' THEN 'RADIESSE'
        WHEN nombre_servicio_sucio LIKE '%MESOTERAPIA%'    THEN 'NCTF'
        WHEN nombre_servicio_sucio LIKE '%VENTA DE PRODUCTO%' THEN 'TIZO'
    END AS nombre_marca,
    nombre_servicio_sucio AS nombre_servicio,
    COALESCE(NULLIF(trim(cantidad_consumida_sucia), ''), '1')::int AS cantidad_consumida
FROM raw_explotado_inicial;

-- Paso 2: insertar consolidando y evitando duplicados
INSERT INTO consumo_productos (
    id_consulta_servicio,
    id_producto,
    cantidad_consumida,
    precio_producto,
    importe_venta
)
SELECT
    cs.id_consulta_servicio,
    pc.id_producto,
    SUM(re.cantidad_consumida)                            AS cantidad_consumida,
    pc.precio_venta                                       AS precio_producto,
    SUM(re.cantidad_consumida) * pc.precio_venta::numeric AS importe_venta
FROM raw_explotado AS re
JOIN pacientes          AS p  ON re.dni = p.dni
JOIN marcas_catalogo    AS mc ON re.nombre_marca = mc.nombre_marca
JOIN productos_catalogo AS pc ON mc.id_marca    = pc.id_marca
JOIN servicios_catalogo AS sc ON re.nombre_servicio = sc.nombre_servicio
JOIN consultas          AS c  ON p.id_paciente = c.id_paciente
                               AND re.fecha = c.fecha_consulta::date
JOIN consultas_servicios AS cs ON c.id_consulta = cs.id_consulta
                                AND sc.id_servicio = cs.id_servicio
GROUP BY cs.id_consulta_servicio, pc.id_producto, pc.precio_venta
ON CONFLICT (id_consulta_servicio, id_producto) DO UPDATE
SET cantidad_consumida = EXCLUDED.cantidad_consumida,
    precio_producto    = EXCLUDED.precio_producto,
    importe_venta      = EXCLUDED.importe_venta;

-- Paso 3: limpiar tabla temporal
DROP TABLE raw_explotado;
