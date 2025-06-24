{{
    config(
        materialized='table'
    )
}}

WITH gender_counts AS (
    SELECT
        genero,
        COUNT(dni) AS numero_de_denunciantes
    FROM
        {{ source('raw_data', 'solicitante') }}
    GROUP BY
        genero
),

total_counts AS (
    SELECT
        COUNT(dni) AS total_denunciantes
    FROM
        {{ source('raw_data', 'solicitante') }}
)

SELECT
    gc.genero,
    gc.numero_de_denunciantes,
    tc.total_denunciantes,
    ROUND((gc.numero_de_denunciantes::numeric / tc.total_denunciantes) * 100, 2) AS proporcion_porcentual
FROM
    gender_counts gc
CROSS JOIN
    total_counts tc
ORDER BY
    gc.numero_de_denunciantes DESC