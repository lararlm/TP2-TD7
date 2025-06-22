-- file: dbt_tp/models/marts/mart_proporcion_genero_denunciantes.sql
{{
    config(
        materialized='table'
    )
}}

-- Paso 1: Contar el número de denunciantes por género
WITH gender_counts AS (
    SELECT
        genero,
        COUNT(dni) AS numero_de_denunciantes
    FROM
        {{ source('raw_data', 'Solicitante') }}
    GROUP BY
        genero
),

-- Paso 2: Contar el total de denunciantes
total_counts AS (
    SELECT
        COUNT(dni) AS total_denunciantes
    FROM
        {{ source('raw_data', 'Solicitante') }}
)

-- Paso 3: Calcular la proporción y presentar el resultado final
SELECT
    gc.genero,
    gc.numero_de_denunciantes,
    tc.total_denunciantes,
    -- Calculamos el porcentaje y lo redondeamos a 2 decimales
    ROUND((gc.numero_de_denunciantes::numeric / tc.total_denunciantes) * 100, 2) AS proporcion_porcentual
FROM
    gender_counts gc
-- Usamos CROSS JOIN para aplicar el total a cada fila de género
CROSS JOIN
    total_counts tc
ORDER BY
    gc.numero_de_denunciantes DESC