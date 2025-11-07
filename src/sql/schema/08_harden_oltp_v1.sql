-- Modulo 1: Refinar esquema con Integridad (UUIDs, Constraints Tolerantes)

-- Extension  permite Crear los UUIDs
CREATE EXTENSION IF NOT EXISTS pgcrypto;

ALTER TABLE pacientes

    -- `gen_random_uuid()`  - Genera de manera aleatoria los UUIDs
    ADD COLUMN uuid_id UUID DEFAULT gen_random_uuid(),

    -- BYTEA es el tipo de dato  para almacenar binario crudo como el texto cifrado
    ADD COLUMN dni_encrypted BYTEA,
    ADD COLUMN telefono_encrypted BYTEA;

-- --- 3. El Trasvase y Cifrado de Datos ---
UPDATE pacientes
SET
    dni_encrypted = pgp_sym_encrypt(dni, 'clave_secreta'),
    telefono_encrypted = pgp_sym_encrypt(COALESCE(telefono, ''), 'clave_secreta');

-- --- 4. Re-Arquitectura de las Llaves (Primary & Foreign Key)

-- 1. Eliminamos la vieja llave primaria (Basada en el id_paciente numerico)
ALTER TABLE pacientes DROP CONSTRAINT paciente_pkey;
ALTER TABLE pacientes ADD PRIMARY KEY (uuid_id);
ALTER TABLE pacientes ADD CONSTRAINT uq_dni_natural UNIQUE (dni);

-- 2. Declaramos Nuestra llave maestra, UUID
-- Primero, añadimos una nueva columna `id_paciente_uuid` a la tabla `consultas`.
ALTER TABLE consultas ADD COLUMN id_paciente_uuid UUID;


-- Ahora, llenamos esta nueva columna. Hacemos un `UPDATE` con un `JOIN`.
-- "Para cada consulta, busca el `id_paciente` numérico en la tabla `pacientes`
--  y copia el `uuid_id` de ese paciente en mi nueva columna."
UPDATE consultas c
SET id_paciente_uuid = p.uuid_id
FROM pacientes p
WHERE c.id_paciente = p.id_paciente;

-- Ahora que los datos están migrados, podemos remodelar el puente.
-- 1. Eliminamos el puente viejo que usaba el ID numérico.
ALTER TABLE consultas DROP CONSTRAINT consultas_id_paciente_fkey;
-- 2. Eliminamos la vieja columna de ID numérico.
ALTER TABLE consultas DROP COLUMN id_paciente;
-- 3. Renombramos nuestra nueva columna UUID para que tome el lugar de la vieja.
ALTER TABLE consultas RENAME COLUMN id_paciente_uuid TO id_paciente;
-- 4. Hacemos la columna `NOT NULL` porque es una relación obligatoria.
ALTER TABLE consultas ALTER COLUMN id_paciente SET NOT NULL;
-- 5. Finalmente, construimos el nuevo puente de acero, apuntando a la `uuid_id`.
ALTER TABLE consultas ADD CONSTRAINT fk_consultas_pacientes
    FOREIGN KEY (id_paciente) REFERENCES pacientes(uuid_id);