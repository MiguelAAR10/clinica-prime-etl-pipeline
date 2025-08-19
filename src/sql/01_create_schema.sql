DROP TABLE IF EXISTS pacientes CASCADE;
DROP TABLE IF EXISTS consultas CASCADE;
DROP TABLE IF EXISTS cobranzas CASCADE;

CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    dni VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(200),
    sexo VARCHAR(10), 
    teléfono VARCHAR(15),
    distrito VARCHAR(50),
    nacimiento_year INTEGER,
    nacimiento_month INTEGER,
    nacimiento_day INTEGER,
    paciente_problematico BOOLEAN DEFAULT FALSE
       
);

CREATE TABLE consultas (
    id_consulta SERIAL PRIMARY KEY,
    id_paciente INTEGER NOT NULL REFERENCES pacientes(id),
    fecha DATE,
    tratamiento VARCHAR(250),
    producto_principal VARCHAR(150),
    unidades INTEGER,
    jeringas INTEGER,
    notas TEXT
);

CREATE TABLE facturas (
    id_factura SERIAL PRIMARY KEY,
    -- LA CORRECCIÓN CRÍTICA: La referencia ahora apunta a 'consultas(id_consulta)'.
    id_consulta INTEGER NOT NULL REFERENCES consultas(id_consulta),
    fecha DATE,
    total NUMERIC(10, 2) NOT NULL DEFAULT 0,
    deuda_generada BOOLEAN,
    deuda_monto NUMERIC(10,2)
    total NUMERIC(10, 2) NOT NULL DEFAULT 0
);

