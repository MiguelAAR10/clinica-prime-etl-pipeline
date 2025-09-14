-- ======================================================================
-- PLANO 03: FORJA DE 'consultas' (REFORJADO ANTI-NULOS V35.0)
-- ======================================================================

TRUNCATE TABLE consultas_servicios RESTART IDENTITY CASCADE;

-- La Anatomia usamos multiples CTEs para desmantelar el problema
INSERT INTO consultas_servicios (id_consulta, id_servicio, precio_servicio)

WITH
-- 1. Explotamos los Servicios de raw_data
raw_servicios_explotados AS (
    SELECT
        dni,
        fecha,
        TRIM(UPPER(regexp_split_to_table(servicios_realizados, ','))) AS nombre_servicio_sucio,
        texto_consulta
    FROM 
        raw_data
),

raw_servicios_purificados AS (
    SELECT
        dni,
        fecha,
        regexp_replace(nombre_servicio_sucio, '[^a-zA-Z0-9\s]', '','g') AS nombre_servicio,
        texto_consulta
    FROM 
        raw_servicios_explotados
)

SELECT
    -- Unimos nuestras Tablas Explotadas con los Catalogos y las Consultas
    c.id_consulta,
    s.id_servicio,
    s.precio_servicio
FROM
    raw_servicios_purificados AS rs
INNER JOIN
    servicios_catalogo AS s ON rs.nombre_servicio = s.nombre_servicio
-- Unimos con pacientes para obtenenr el `id_paciente` necesario para poder encontrar la consula
INNER JOIN 
    pacientes AS p ON rs.dni = p.dni
-- Unimos consultas para obtenenr el id_consulta
INNER JOIN
    consultas AS c ON p.id_paciente = c.id_paciente AND CAST(rs.fecha AS DATE) = c.fecha_consulta
-- `LEFT JOIN` con marcas, porque un servicio puede no tener un Marca Asociada.
WHERE
    rs.nombre_servicio IS NOT NULL AND rs.nombre_servicio != '';


     