-- ======================================================================
-- 🏛️ PROTOCOLO DE POBLACIÓN DE CATÁLOGOS V99.6 (FORJADO EN LOTE)
-- ======================================================================

-- --- PASO ÚNICO: INSERCIÓN EN LOTE DESDE UNA FUENTE DE VERDAD VIRTUAL ---
-- La Anatomía: INSERT INTO ... SELECT ... FROM (VALUES ...) AS ...
-- El Propósito: Esta es la forma más poderosa y eficiente de insertar
-- datos estáticos en PostgreSQL.
-- 1. `(VALUES ...)`: Creamos una "tabla virtual" en la memoria con todos nuestros datos.
-- 2. `FROM ... AS v(...)`: Le damos un nombre a esta tabla virtual (`v`) y a sus columnas.
-- 3. `SELECT ... JOIN ...`: Hacemos un `SELECT` desde nuestra tabla virtual,
--    uniéndola con `marcas_catalogo` UNA SOLA VEZ para obtener todos los `id_marca`
--    de forma eficiente.
-- 4. `ON CONFLICT DO NOTHING`: Es nuestro seguro de vida. Si intentamos insertar
--    un producto que ya existe (basado en una restricción de unicidad),
--    PostgreSQL simplemente ignorará esa fila y continuará.

-- Asegúrate de tener una restricción de unicidad en tu tabla para que ON CONFLICT funcione.
-- Si no la tienes, añádela primero:
-- ALTER TABLE productos_catalogo ADD CONSTRAINT uq_producto_nombre UNIQUE (nombre_producto);

TRUNCATE TABLE productos_catalogo RESTART IDENTITY CASCADE;


INSERT INTO productos_catalogo (
    id_marca,
    nombre_producto,
    unidad_de_medida,
    costo_unitario,
    precio_venta
)
SELECT
    mc.id_marca,
    v.nombre_producto,
    v.unidad_de_medida,
    v.costo_unitario,
    v.precio_venta
FROM (
    VALUES
        -- Formato: (nombre_marca, nombre_producto, unidad, costo, precio)
        -- Tratamientos Principales
        ('BOTOX',      'Toxina Botulinica',         'unidad',   10.50,    21.00),
        ('JUVEDERM',   'Relleno Acido Hialuronico',              'jeringa', 565.00,   800.00),
        ('ART FILLER', 'Relleno Acido Hialuronico',            'jeringa', 475.00,   700.00),
        ('CROMA',      'Relleno Acido Hialuronico',                 'jeringa', 415.00,   625.00),
        ('HARMONYCA',  'Bioestimulador de Colágeno','vial',  1425.00,  3000.00),
        ('RADIESSE',   'Bioestimulador de Colágeno', 'jeringa', 700.00,   2000.00),
        ('ELLANSE',    'Bioestimulador de Colágeno',  'jeringa', 760.00,   1800.00),
        ('NCTF',       'Mesoterapia Skinbooster',                 'vial',    150.00,   400.00),
        ('PB SERUM',   'Enzima - PB Serum',                  'vial',    475.00,   900.00),
        
        -- Productos de Venta / Genéricos
        ('ISDIN',      'Producto ISDIN General',             'unidad',   50.00,   100.00),
        ('B3',         'Producto B3 General',                'unidad',   40.00,    90.00),
        ('HYDRAMAX',   'Producto Hydramax General',          'unidad',  150.00,   350.00),
        ('EYE REFRESH','Contorno Ojos Eye Refresh',          'unidad',  120.00,   300.00),
        ('SVR',        'Producto SVR General',               'unidad',   80.00,   200.00),
        ('SKINLAB',    'Producto SkinLab Genérico',          'unidad',  100.00,   220.00),
        ('TML',        'Producto TML General',               'unidad',   90.00,   200.00),
        ('MICROPEEL',  'Micropeel General',                  'unidad',  120.00,   300.00),
        ('JALUPRO',    'Mesoterapia Skinbooster',       'vial',    250.00,   550.00),
        ('PHYTO',      'Producto PHYTO General',             'unidad',   70.00,   160.00),
        ('TIZO',       'Protector Solar Tizo Genérico',      'unidad',   40.00,    90.00)

) AS v(nombre_marca, nombre_producto, unidad_de_medida, costo_unitario, precio_venta)
JOIN
    marcas_catalogo mc ON v.nombre_marca = mc.nombre_marca;