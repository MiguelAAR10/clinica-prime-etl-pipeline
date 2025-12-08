-- ======================================================================
-- 🏛️ PLANO MAESTRO DEL TEMPLO V70.0 (ARQUITECTURA FINAL)
-- ======================================================================

-- --- ACTO 1: LA GRAN PURGA ---
-- Borra todas las tablas para comenzar con un lienzo limpio.
DROP TABLE IF EXISTS raw_data;
DROP TABLE IF EXISTS pagos CASCADE;
DROP TABLE IF EXISTS facturas CASCADE;
DROP TABLE IF EXISTS consumo_productos CASCADE;
DROP TABLE IF EXISTS consultas_servicios CASCADE;
DROP TABLE IF EXISTS consultas CASCADE;
DROP TABLE IF EXISTS productos_catalogo CASCADE;
DROP TABLE IF EXISTS servicios_catalogo CASCADE;
DROP TABLE IF EXISTS marcas_catalogo CASCADE;
DROP TABLE IF EXISTS pacientes CASCADE;
DROP TABLE IF EXISTS distritos CASCADE;
DROP TABLE IF EXISTS medios_de_pago CASCADE;
DROP TABLE IF EXISTS descuentos CASCADE;


-- --- ACTO 2: LOS CATÁLOGOS (Dimensiones y Métricas) ---
-- 📍 Catálogo de Distritos
CREATE TABLE distritos (
    id_distrito SERIAL PRIMARY KEY,
    nombre_distrito VARCHAR(80) UNIQUE 
);

CREATE TABLE pacientes (
    id_paciente SERIAL PRIMARY KEY,
    dni VARCHAR(20) UNIQUE,
    nombre_completo VARCHAR(255) NOT NULL,
    sexo VARCHAR(10),
    telefono VARCHAR(25),
    id_distrito INT REFERENCES distritos(id_distrito),
    nacimiento_year INT,
    nacimiento_month INT,
    nacimiento_day INT,
    paciente_problematico BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE marcas_catalogo (
    id_marca SERIAL PRIMARY KEY,
    nombre_marca VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE servicios_catalogo (
    id_servicio SERIAL PRIMARY KEY,
    nombre_servicio VARCHAR(250) UNIQUE NOT NULL,
    precio_servicio NUMERIC(10,2)
);

-- 💉 Catálogo de Productos (El Inventario Físico)
CREATE TABLE productos_catalogo (
    id_producto SERIAL PRIMARY KEY,
    id_marca INT REFERENCES marcas_catalogo(id_marca),
    nombre_producto VARCHAR(150) NOT NULL,
    unidad_de_medida VARCHAR(20) NOT NULL,
    costo_unitario NUMERIC(10, 2) NOT NULL DEFAULT 0,
    precio_venta NUMERIC(10, 2) NOT NULL DEFAULT 0,
    stock_actual NUMERIC(10, 2) NOT NULL DEFAULT 0
);

CREATE TABLE descuentos (
    id_descuento SERIAL PRIMARY KEY,
    codigo_descuento VARCHAR(50) UNIQUE NOT NULL,
    tipo_descuento VARCHAR(10) NOT NULL, -- 'PORCENTAJE' o 'FIJO'
    valor NUMERIC(5,2) NOT NULL
);

-- 💳 Catálogo de Medios de Pago
CREATE TABLE medios_de_pago (
    id_m_pago SERIAL PRIMARY KEY,
    nombre_m_pago VARCHAR(50) UNIQUE NOT NULL
);

-- --- ACTO 3: LOS EVENTOS (LOS HECHOS - EL "CÓMO, CUÁNDO y CUÁNTO") ---

-- La Visita
CREATE TABLE consultas (
    id_consulta SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL REFERENCES pacientes(id_paciente),
    fecha_consulta DATE NOT NULL,
    notas_generales TEXT,
    total_historico NUMERIC(10,2) DEFAULT 0
);

-- La "Comanda" - Qué servicios se aplicaron en una consulta
CREATE TABLE consultas_servicios (
    id_consulta_servicio SERIAL PRIMARY KEY,
    id_consulta INT NOT NULL REFERENCES consultas(id_consulta),
    id_servicio INT NOT NULL REFERENCES servicios_catalogo(id_servicio),
    -- El precio de la mano de obra en el momento de la consulta
    precio_servicio NUMERIC(10, 2), -- Un servicio solo se puede aplicar una vez por consulta
    UNIQUE(id_consulta, id_servicio)
);

-- El Informe de Materiales - Qué productos se consumieron para un servicio en una consulta
CREATE TABLE consumo_productos (
    id_consumo SERIAL PRIMARY KEY,
    -- Vinculado a un servicio específico dentro de una consulta
    id_consulta_servicio INT NOT NULL REFERENCES consultas_servicios(id_consulta_servicio),
    id_producto INT NOT NULL REFERENCES productos_catalogo(id_producto),
    cantidad_consumida NUMERIC(10,2) NOT NULL DEFAULT 1,
    -- Registramos el precio y costo en e,l momento para una contabilidad perfecta
    precio_producto NUMERIC(10, 2) NOT NULL,
    importe_venta NUMERIC(10,2), NOT NULL
    UNIQUE(id_consulta_servicio, id_producto)
);

-- La Cuenta Final
CREATE TABLE facturas (
    id_factura SERIAL PRIMARY KEY,
    id_consulta INT NOT NULL REFERENCES consultas(id_consulta) UNIQUE,
    fecha_emision TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    -- Totales que se CALCULARÁN a partir de los servicios y productos.
    total_bruto NUMERIC(12, 2) NOT NULL v, 
    id_descuento INT REFERENCES descuentos(id_descuento),
    monto_descuento NUMERIC(12, 2) DEFAULT 0,
    total_neto NUMERIC(12, 2) NOT NULL,
    -- El total del Excel, para aiuditoría.
    total_historico NUMERIC(12, 2) NOT NULL
);

-- Los Pagos
CREATE TABLE pagos(
    id_pago SERIAL PRIMARY KEY,
    id_factura INT NOT NULL REFERENCES facturas(id_factura),
    fecha_pago TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    id_medio_de_pago INT NOT NULL REFERENCES medios_de_pago(id_m_pago),
    monto_pagado NUMERIC(12,2) NOT NULL
);

DROP INDEX IF EXISTS search_notas_consulta;
CREATE INDEX search_notas_consulta 
ON consultas USING GIN (
    to_tsvector('spanish', COALESCE(notas_generales, ''))
);

-- --- ACTO 4: LA OPTIMIZACIÓN (Índices) ---
CREATE INDEX IF NOT EXISTS ix_pacientes_dni ON pacientes(dni);
CREATE INDEX IF NOT EXISTS ix_consultas_fecha ON consultas(fecha_consulta);

