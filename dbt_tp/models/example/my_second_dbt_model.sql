{{
    config(
        materialized='table'
    )
}}


select 
    *,

    CASE
        WHEN proporcion_porcentual >= 50.0 THEN 'Representación Mayoritaria'
        WHEN proporcion_porcentual <= 10.0 THEN 'Representación Minoritaria'
        ELSE 'Representación Estándar'
    END AS categoria_representacion
FROM
    {{ ref('my_first_dbt_model') }} -- Aquí referenciamos el primer modelo