{{
    config(
        materialized='table'
    )
}}

SELECT
    'Género del Solicitante' AS dimension,
    s.genero AS valor,
    COUNT(d.id_denuncia) AS total_denuncias
FROM
    {{ source('raw_data', 'denuncia') }} d
LEFT JOIN
    {{ source('raw_data', 'solicitante') }} s ON d.dni_solicitante = s.dni
WHERE
    s.genero IS NOT NULL
GROUP BY
    s.genero

UNION ALL

SELECT
    'Nivel Educativo del Solicitante' AS dimension,
    ne.nivel AS valor,
    COUNT(d.id_denuncia) AS total_denuncias
FROM
    {{ source('raw_data', 'denuncia') }} d
LEFT JOIN
    {{ source('raw_data', 'solicitante') }} s ON d.dni_solicitante = s.dni
LEFT JOIN
    {{ source('raw_data', 'nivel_educativo') }} ne ON s.maximo_nivel_educativo = ne.id
WHERE
    ne.nivel IS NOT NULL
GROUP BY
    ne.nivel

UNION ALL

SELECT
    'Vínculo del Denunciado' AS dimension,
    vu.nombre_vinculo AS valor,
    COUNT(d.id_denuncia) AS total_denuncias
FROM
    {{ source('raw_data', 'denuncia') }} d
LEFT JOIN
    {{ source('raw_data', 'denunciado') }} den ON d.dni_denunciado = den.dni
LEFT JOIN
    {{ source('raw_data', 'vinculo_universidad') }} vu ON den.vinculo_universidad_id = vu.id
WHERE
    vu.nombre_vinculo IS NOT NULL
GROUP BY
    vu.nombre_vinculo


UNION ALL

SELECT
    'Condición Laboral del Solicitante' as dimension,
    cl.condicion as valor,
    COUNT(d.id_denuncia) AS total_denuncias
FROM
    {{ source('raw_data', 'denuncia') }} d
LEFT JOIN
    {{ source('raw_data', 'solicitante') }} s ON d.dni_solicitante = s.dni
LEFT JOIN
    {{ source('raw_data', 'condicion_laboral') }} cl ON s.condicion_laboral = cl.id
WHERE
    cl.condicion IS NOT NULL
GROUP BY
    cl.condicion

UNION ALL

SELECT
    'Tipo de Vivienda del Solicitante' as dimension,
    tv.vivienda as valor,
    COUNT(d.id_denuncia) AS total_denuncias
FROM
    {{ source('raw_data', 'denuncia') }} d
LEFT JOIN
    {{ source('raw_data', 'solicitante') }} s ON d.dni_solicitante = s.dni
LEFT JOIN
    {{ source('raw_data', 'tipo_vivienda') }} tv ON s.tipo_vivienda = tv.id
WHERE
    tv.vivienda IS NOT NULL
GROUP BY
    tv.vivienda