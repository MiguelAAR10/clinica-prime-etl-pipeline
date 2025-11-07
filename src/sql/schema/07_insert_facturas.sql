-- INSERTAR DATOS A FACTURAS
TRUNCATE TABLE facturas CASCADE;

INSERT INTO facturas (
    id_consulta,
    fecha_emision,
    total_bruto,
    total_historico
)

SELECT
    c.id_consulta,
    c.fecha_consulta,
    COALESCE(SUM(cs.precio_servicio), 0) + COALESCE(SUM(cp.importe_venta),0) AS total_calculado,
    COALESCE(c.total_historico,0) AS total_historico
FROM
    consultas AS c 
JOIN
    consultas_servicios AS cs 
    ON c.id_consulta  = cs.id_consulta
LEFT JOIN
    consumo_productos AS cp 
    ON cs.id_consulta_servicio = cp.id_consulta_servicio
GROUP BY 
    c.id_consulta,
    c.fecha_consulta,
    C.total_historico
ORDER BY
   c.fecha_consulta 
;
    

    