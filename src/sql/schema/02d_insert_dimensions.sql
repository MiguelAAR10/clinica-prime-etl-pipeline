INSERT INTO distritos (nombre_distrito)
SELECT DISTINCT TRIM(UPPER(distrito)) 
FROM raw_data 
WHERE distrito IS NOT NULL AND distrito != '';