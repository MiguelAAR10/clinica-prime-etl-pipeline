-- ======================================================================
-- 🏛️ PLANO 02: FORJA DE CATÁLOGOS (LÓGICA REFINADA V2.2)
-- ======================================================================

-- --- 💥 ACTO 1: PURGA PREPARATORIA ---
TRUNCATE TABLE marcas_catalogo RESTART IDENTITY CASCADE;
TRUNCATE TABLE servicios_catalogo RESTART IDENTITY CASCADE;


-- Insertar a Catalogo de Marcas
-- -- 1. COMMON TABLE EXPRESSION (CTE 1) -> 'regexp_split_to_table' -> Permite hacer el split de las filas
WITH 
marcas_desenrolladas AS (
SELECT
    regexp_split_to_table(marcas_detectadas, ',') AS marca_sucia
FROM 
    raw_data
),
-- -- 2. COMMON TABLE EXPRESSION (CTE 2) -> 'TRIM': Elimina Espacios Vacios, 'UPPER': Convierte a Mayusculas Todo
-- -- regexp_replace(fuente, patron, reemplazo, banderas)
-- -- g: Bandera Global sognifica todas la coincidencias posibles
marcas_purificadas AS (
SELECT
    TRIM(UPPER(regexp_replace(marca_sucia, '[^a-zA-Z0-9\s]', '', 'g'))) AS nombre_marca
FROM 
    marcas_desenrolladas
)
INSERT INTO marcas_catalogo(nombre_marca)
SELECT
    DISTINCT nombre_marca
FROM
    marcas_purificadas
WHERE
    nombre_marca IS NOT NULL AND nombre_marca != '';







-- ===================================================================================
-- Insertar a Catalogo de Servicios
-- -- 1. COMON TABLE EXPRESION (CTE 1) -> 'regexp_split_to_table' -> Permite hacer el split de las filas
WITH 
servicios_desenrrollados AS (
SELECT
    regexp_split_to_table(servicios_realizados, ',') AS servicio_sucio
FROM 
    raw_data
),
-- -- 2. COMMON TABLE
servicios_purificados AS (
SELECT
    TRIM(UPPER(regexp_replace(servicio_sucio, '[^a-zA-Z0-9\s]', '', 'g'))) AS nombre_servicio
FROM
    servicios_desenrrollados
)
INSERT INTO servicios_catalogo(nombre_servicio)
SELECT
    DISTINCT nombre_servicio
FROM
    servicios_purificados
WHERE 
    nombre_servicio IS NOT NULL AND nombre_servicio != ''
ON CONFLICT(nombre_servicio) DO NOTHING;








-- Actualiza el precio de la 'CONSULTA' a un valor de mercado realista
UPDATE servicios_catalogo
SET precio_servicio = 120.00
WHERE nombre_servicio = 'CONSULTA';
-- Actualiza el precio de la 'MESOTERAPIA SKINBOOSTER'
UPDATE servicios_catalogo
SET precio_servicio = 80.00
WHERE nombre_servicio = 'MESOTERAPIA SKINBOOSTER';
-- Actualiza el precio de 'VENTA DE PRODUCTO' (costo por tiempo de asesoría)
UPDATE servicios_catalogo
SET precio_servicio = 0.00
WHERE nombre_servicio = 'VENTA DE PRODUCTO DERMOCOSMETICO';
-- Actualiza el precio de 'TOXINA BOTULINICA' (el costo de la mano de obra del doctor)
UPDATE servicios_catalogo
SET precio_servicio = 85.00
WHERE nombre_servicio = 'TOXINA BOTULINICA';
-- Actualiza el precio de 'BIOESTIMULADOR DE COLAGENO' (el costo de la mano de obra del doctor)
UPDATE servicios_catalogo
SET precio_servicio = 150.00
WHERE nombre_servicio = 'BIOESTIMULADOR DE COLAGENO';
-- Actualiza el precio de 'RELLENO CIDO HIALURNICO' (el costo de la mano de obra del doctor)
UPDATE servicios_catalogo
SET precio_servicio = 100.00
WHERE nombre_servicio = 'RELLENO ACIDO HIALURONICO';
-- Actualiza el precio de 'ENZIMAS RECOMBINANTES' (el costo de la mano de obra del doctor)
UPDATE servicios_catalogo
SET precio_servicio = 100.00
WHERE nombre_servicio = 'ENZIMAS RECOMBINANTES';
-- 
