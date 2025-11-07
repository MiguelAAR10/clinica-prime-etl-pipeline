TRUNCATE TABLE consultas RESTART IDENTITY CASCADE;

-- La Inserccion Final
INSERT INTO consultas(id_paciente,fecha_consulta, notas_generales, total_historico)
SELECT
    p.id_paciente,
    r.fecha,
    CAST(r.texto_consulta AS TEXT) AS notas_generales,
    CAST(r.total AS NUMERIC) AS total_historico
FROM
    raw_data AS r
INNER JOIN
    pacientes AS p
ON r.dni = p.dni
WHERE
    r.fecha IS NOT NULL
;