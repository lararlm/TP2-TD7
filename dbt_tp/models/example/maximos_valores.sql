{{
    config(
        materialized='table'
    )
}}

WITH ranked_metrics AS (
    SELECT
        dimension,
        valor,
        total_denuncias,
        RANK() OVER (PARTITION BY dimension ORDER BY total_denuncias DESC) as ranking
    FROM
        {{ ref('procesamiento_categorico') }} 
)

SELECT
    dimension,
    valor AS categoria_top,
    total_denuncias
FROM
    ranked_metrics
WHERE
    ranking = 1