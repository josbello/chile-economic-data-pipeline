-- ============================================================
-- CHILE ECONOMIC DATA PIPELINE
-- SQL ANALYTICS
--
-- Indicadores:
-- 1. Dólar observado
-- 2. Unidad de Fomento
-- 3. Tasa de Política Monetaria
-- 4. IPC - Variación mensual
-- ============================================================


-- ============================================================
-- 1. RESUMEN GENERAL DE LA BASE DE DATOS
-- ============================================================

SELECT
    indicator_name,
    frequency,
    COUNT(*) AS total_registros,
    MIN(observation_date) AS fecha_inicial,
    MAX(observation_date) AS fecha_final,
    ROUND(MIN(value), 2) AS valor_minimo,
    ROUND(MAX(value), 2) AS valor_maximo,
    ROUND(AVG(value), 2) AS valor_promedio
FROM economic_indicators
GROUP BY
    indicator_name,
    frequency
ORDER BY indicator_name;



-- ============================================================
-- 2. ÚLTIMA OBSERVACIÓN DISPONIBLE POR INDICADOR
-- ============================================================

SELECT DISTINCT ON (series_id)
    indicator_name,
    frequency,
    observation_date,
    value
FROM economic_indicators
ORDER BY
    series_id,
    observation_date DESC;



-- ============================================================
-- 3. CANTIDAD DE REGISTROS POR INDICADOR Y AÑO
-- ============================================================

SELECT
    indicator_name,
    year,
    COUNT(*) AS total_registros
FROM economic_indicators
GROUP BY
    indicator_name,
    year
ORDER BY
    indicator_name,
    year;



-- ============================================================
-- 4. RESUMEN ANUAL POR INDICADOR
-- ============================================================

SELECT
    indicator_name,
    year,
    COUNT(*) AS observaciones,
    ROUND(AVG(value), 2) AS promedio_anual,
    ROUND(MIN(value), 2) AS minimo_anual,
    ROUND(MAX(value), 2) AS maximo_anual
FROM economic_indicators
GROUP BY
    indicator_name,
    year
ORDER BY
    indicator_name,
    year;



-- ============================================================
-- 5. RESUMEN MENSUAL POR INDICADOR
-- ============================================================

SELECT
    indicator_name,
    year,
    month,
    COUNT(*) AS observaciones,
    ROUND(AVG(value), 2) AS promedio_mensual,
    ROUND(MIN(value), 2) AS minimo_mensual,
    ROUND(MAX(value), 2) AS maximo_mensual
FROM economic_indicators
GROUP BY
    indicator_name,
    year,
    month
ORDER BY
    indicator_name,
    year,
    month;



-- ============================================================
-- 6. EVOLUCIÓN DEL DÓLAR OBSERVADO
-- ============================================================

SELECT
    observation_date,
    value
FROM economic_indicators
WHERE series_id = 'F073.TCO.PRE.Z.D'
ORDER BY observation_date;



-- ============================================================
-- 7. VARIACIÓN DIARIA DEL DÓLAR
-- ============================================================

WITH dolar_variaciones AS (
    SELECT
        observation_date,
        value,
        LAG(value) OVER (
            ORDER BY observation_date
        ) AS valor_anterior
    FROM economic_indicators
    WHERE series_id = 'F073.TCO.PRE.Z.D'
)

SELECT
    observation_date,
    value,
    valor_anterior,

    ROUND(
        value - valor_anterior,
        2
    ) AS variacion,

    ROUND(
        ((value - valor_anterior) / valor_anterior) * 100,
        2
    ) AS variacion_porcentual

FROM dolar_variaciones
WHERE valor_anterior IS NOT NULL
ORDER BY observation_date;



-- ============================================================
-- 8. MAYORES ALZAS DIARIAS DEL DÓLAR
-- ============================================================

WITH dolar_variaciones AS (
    SELECT
        observation_date,
        value,
        LAG(value) OVER (
            ORDER BY observation_date
        ) AS valor_anterior
    FROM economic_indicators
    WHERE series_id = 'F073.TCO.PRE.Z.D'
)

SELECT
    observation_date,
    valor_anterior,
    value AS valor_actual,

    ROUND(
        value - valor_anterior,
        2
    ) AS variacion,

    ROUND(
        ((value - valor_anterior) / valor_anterior) * 100,
        2
    ) AS variacion_porcentual

FROM dolar_variaciones
WHERE valor_anterior IS NOT NULL
ORDER BY variacion_porcentual DESC
LIMIT 10;



-- ============================================================
-- 9. MAYORES CAÍDAS DIARIAS DEL DÓLAR
-- ============================================================

WITH dolar_variaciones AS (
    SELECT
        observation_date,
        value,
        LAG(value) OVER (
            ORDER BY observation_date
        ) AS valor_anterior
    FROM economic_indicators
    WHERE series_id = 'F073.TCO.PRE.Z.D'
)

SELECT
    observation_date,
    valor_anterior,
    value AS valor_actual,

    ROUND(
        value - valor_anterior,
        2
    ) AS variacion,

    ROUND(
        ((value - valor_anterior) / valor_anterior) * 100,
        2
    ) AS variacion_porcentual

FROM dolar_variaciones
WHERE valor_anterior IS NOT NULL
ORDER BY variacion_porcentual ASC
LIMIT 10;



-- ============================================================
-- 10. EVOLUCIÓN DE LA UF
-- ============================================================

SELECT
    observation_date,
    value AS valor_uf
FROM economic_indicators
WHERE series_id = 'F073.UFF.PRE.Z.D'
ORDER BY observation_date;



-- ============================================================
-- 11. EVOLUCIÓN DE LA TPM
-- ============================================================

SELECT
    observation_date,
    value AS tpm
FROM economic_indicators
WHERE series_id = 'F022.TPM.TIN.D001.NO.Z.D'
ORDER BY observation_date;



-- ============================================================
-- 12. EVOLUCIÓN DEL IPC MENSUAL
-- ============================================================

SELECT
    observation_date,
    value AS ipc_variacion_mensual
FROM economic_indicators
WHERE series_id = 'F074.IPC.VAR.Z.Z.C.M'
ORDER BY observation_date;



-- ============================================================
-- 13. MESES CON MAYOR INFLACIÓN
-- ============================================================

SELECT
    observation_date,
    value AS variacion_ipc
FROM economic_indicators
WHERE series_id = 'F074.IPC.VAR.Z.Z.C.M'
ORDER BY value DESC
LIMIT 10;



-- ============================================================
-- 14. MESES CON MENOR VARIACIÓN DEL IPC
-- Incluye meses con inflación negativa si existen.
-- ============================================================

SELECT
    observation_date,
    value AS variacion_ipc
FROM economic_indicators
WHERE series_id = 'F074.IPC.VAR.Z.Z.C.M'
ORDER BY value ASC
LIMIT 10;



-- ============================================================
-- 15. DÓLAR, UF Y TPM EN FECHAS COMUNES
-- ============================================================

SELECT
    observation_date,

    MAX(value) FILTER (
        WHERE series_id = 'F073.TCO.PRE.Z.D'
    ) AS dolar_observado,

    MAX(value) FILTER (
        WHERE series_id = 'F073.UFF.PRE.Z.D'
    ) AS uf,

    MAX(value) FILTER (
        WHERE series_id = 'F022.TPM.TIN.D001.NO.Z.D'
    ) AS tpm

FROM economic_indicators

WHERE series_id IN (
    'F073.TCO.PRE.Z.D',
    'F073.UFF.PRE.Z.D',
    'F022.TPM.TIN.D001.NO.Z.D'
)

GROUP BY observation_date

HAVING
    MAX(value) FILTER (
        WHERE series_id = 'F073.TCO.PRE.Z.D'
    ) IS NOT NULL

    AND

    MAX(value) FILTER (
        WHERE series_id = 'F073.UFF.PRE.Z.D'
    ) IS NOT NULL

    AND

    MAX(value) FILTER (
        WHERE series_id = 'F022.TPM.TIN.D001.NO.Z.D'
    ) IS NOT NULL

ORDER BY observation_date;



-- ============================================================
-- 16. DATASET MENSUAL CONSOLIDADO
--
-- Esta consulta será especialmente útil para Power BI.
-- Convierte los indicadores diarios en promedios mensuales
-- y los combina con el IPC mensual.
-- ============================================================

WITH mensual AS (

    SELECT
        DATE_TRUNC(
            'month',
            observation_date
        )::date AS mes,

        ROUND(
            AVG(value) FILTER (
                WHERE series_id = 'F073.TCO.PRE.Z.D'
            ),
            2
        ) AS dolar_promedio,

        ROUND(
            AVG(value) FILTER (
                WHERE series_id = 'F073.UFF.PRE.Z.D'
            ),
            2
        ) AS uf_promedio,

        ROUND(
            AVG(value) FILTER (
                WHERE series_id = 'F022.TPM.TIN.D001.NO.Z.D'
            ),
            2
        ) AS tpm_promedio,

        MAX(value) FILTER (
            WHERE series_id = 'F074.IPC.VAR.Z.Z.C.M'
        ) AS ipc_variacion_mensual

    FROM economic_indicators

    GROUP BY
        DATE_TRUNC(
            'month',
            observation_date
        )
)

SELECT *
FROM mensual
ORDER BY mes;



-- ============================================================
-- 17. VARIACIÓN MENSUAL DEL PROMEDIO DEL DÓLAR
-- ============================================================

WITH dolar_mensual AS (

    SELECT
        DATE_TRUNC(
            'month',
            observation_date
        )::date AS mes,

        AVG(value) AS dolar_promedio

    FROM economic_indicators

    WHERE series_id = 'F073.TCO.PRE.Z.D'

    GROUP BY
        DATE_TRUNC(
            'month',
            observation_date
        )
),

variaciones AS (

    SELECT
        mes,
        dolar_promedio,

        LAG(dolar_promedio) OVER (
            ORDER BY mes
        ) AS promedio_mes_anterior

    FROM dolar_mensual
)

SELECT
    mes,

    ROUND(
        dolar_promedio,
        2
    ) AS dolar_promedio,

    ROUND(
        promedio_mes_anterior,
        2
    ) AS promedio_mes_anterior,

    ROUND(
        (
            (
                dolar_promedio
                - promedio_mes_anterior
            )
            / promedio_mes_anterior
        ) * 100,
        2
    ) AS variacion_mensual_porcentual

FROM variaciones

WHERE promedio_mes_anterior IS NOT NULL

ORDER BY mes;



-- ============================================================
-- 18. CAMBIOS EN LA TPM
--
-- Devuelve solo fechas donde la TPM cambió respecto
-- de la observación anterior.
-- ============================================================

WITH cambios_tpm AS (

    SELECT
        observation_date,
        value,

        LAG(value) OVER (
            ORDER BY observation_date
        ) AS tpm_anterior

    FROM economic_indicators

    WHERE series_id = 'F022.TPM.TIN.D001.NO.Z.D'
)

SELECT
    observation_date,
    tpm_anterior,
    value AS nueva_tpm,

    ROUND(
        value - tpm_anterior,
        2
    ) AS cambio

FROM cambios_tpm

WHERE
    tpm_anterior IS NOT NULL
    AND value <> tpm_anterior

ORDER BY observation_date;



-- ============================================================
-- 19. CRECIMIENTO ANUAL PROMEDIO DE LA UF
-- ============================================================

WITH uf_anual AS (

    SELECT
        year,
        AVG(value) AS promedio_uf

    FROM economic_indicators

    WHERE series_id = 'F073.UFF.PRE.Z.D'

    GROUP BY year
),

crecimiento AS (

    SELECT
        year,
        promedio_uf,

        LAG(promedio_uf) OVER (
            ORDER BY year
        ) AS promedio_anterior

    FROM uf_anual
)

SELECT
    year,

    ROUND(
        promedio_uf,
        2
    ) AS promedio_uf,

    ROUND(
        (
            (
                promedio_uf
                - promedio_anterior
            )
            / promedio_anterior
        ) * 100,
        2
    ) AS crecimiento_porcentual

FROM crecimiento

WHERE promedio_anterior IS NOT NULL

ORDER BY year;



-- ============================================================
-- 20. CONTROL DE DUPLICADOS
-- Debe devolver cero filas.
-- ============================================================

SELECT
    series_id,
    observation_date,
    COUNT(*) AS repeticiones

FROM economic_indicators

GROUP BY
    series_id,
    observation_date

HAVING COUNT(*) > 1;



-- ============================================================
-- 21. CONTROL DE VALORES NULOS
-- Debe devolver cero filas.
-- ============================================================

SELECT *
FROM economic_indicators
WHERE
    series_id IS NULL
    OR indicator_name IS NULL
    OR observation_date IS NULL
    OR value IS NULL;