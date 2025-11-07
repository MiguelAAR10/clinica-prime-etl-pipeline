TRUNCATE TABLE pacientes RESTART IDENTITY CASCADE;

INSERT INTO pacientes (dni, nombre_completo, sexo, telefono, id_distrito, nacimiento_year, nacimiento_month, nacimiento_day, paciente_problematico, created_at)
SELECT DISTINCT ON (dni)
    CAST(r.dni AS VARCHAR),
    r.nombre, 
    r.sexo,
    CAST(r.teléfono AS VARCHAR),
    d.id_distrito,
    CAST(r.nacimiento_year AS INT),
    CAST(r.nacimiento_month AS INT),
    CAST(r.nacimiento_day AS INT),
    r.paciente_problematico,
    CAST(r.fecha AS TIMESTAMP)
FROM
    raw_data AS r
LEFT JOIN
    distritos AS d ON r.distrito = d.nombre_distrito
WHERE
    -- Condicion de Filtrado
    dni IS NOT NULL AND dni != ''
ORDER BY
    dni, fecha DESC NULLS LAST;
