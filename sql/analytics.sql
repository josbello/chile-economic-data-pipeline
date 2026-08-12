-- ============================================================
-- Chile Economic Data Pipeline
-- Consultas analíticas
-- ============================================================


-- ============================================================
-- 1. RESUMEN GENERAL DEL DÓLAR OBSERVADO
-- ============================================================

SELECT
    COUNT(*) AS total_observaciones,
    MIN(observation_date) AS fecha_inicial,
    MAX(observation_date) AS fecha_final,
    MIN(value) AS valor_minimo,
    MAX(value) AS valor_maximo,
    ROUND(AVG(value), 2) AS valor_promedio
FROM economic_indicators
WHERE series_id = 'F073.TCO.PRE.Z.D';


-- ============================================================
-- 2. PROMEDIO DEL DÓLAR POR AÑO
-- ============================================================

SELECT
    year,
    COUNT(*) AS observaciones,
    ROUND(AVG(value), 2) AS promedio_anual,
    MIN(value) AS minimo_anual,
    MAX(value) AS maximo_anual
FROM economic_indicators
WHERE series_id = 'F073.TCO.PRE.Z.D'
GROUP BY year
ORDER BY year;


-- ============================================================
-- 3. PROMEDIO MENSUAL DEL DÓLAR
-- ============================================================

SELECT
    year,
    month,
    COUNT(*) AS observaciones,
    ROUND(AVG(value), 2) AS promedio_mensual,
    MIN(value) AS minimo_mensual,
    MAX(value) AS maximo_mensual
FROM economic_indicators
WHERE series_id = 'F073.TCO.PRE.Z.D'
GROUP BY year, month
ORDER BY year, month;


-- ============================================================
-- 4. DÍA CON EL VALOR MÁS ALTO DEL PERÍODO
-- ============================================================

SELECT
    observation_date,
    value
FROM economic_indicators
WHERE series_id = 'F073.TCO.PRE.Z.D'
ORDER BY value DESC
LIMIT 1;


-- ============================================================
-- 5. DÍA CON EL VALOR MÁS BAJO DEL PERÍODO
-- ============================================================

SELECT
    observation_date,
    value
FROM economic_indicators
WHERE series_id = 'F073.TCO.PRE.Z.D'
ORDER BY value ASC
LIMIT 1;


-- ============================================================
-- 6. VARIACIÓN DIARIA DEL DÓLAR
-- ============================================================

SELECT
    observation_date,
    value,
    LAG(value) OVER (
        ORDER BY observation_date
    ) AS valor_anterior,

    ROUND(
        value - LAG(value) OVER (
            ORDER BY observation_date
        ),
        2
    ) AS variacion_diaria

FROM economic_indicators
WHERE series_id = 'F073.TCO.PRE.Z.D'
ORDER BY observation_date;


-- ============================================================
-- 7. VARIACIÓN PORCENTUAL DIARIA
-- ============================================================

WITH variaciones AS (
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
        (
            (value - valor_anterior)
            / valor_anterior
        ) * 100,
        2
    ) AS variacion_porcentual

FROM variaciones
WHERE valor_anterior IS NOT NULL
ORDER BY observation_date;


-- ============================================================
-- 8. MAYORES ALZAS DIARIAS
-- ============================================================

WITH variaciones AS (
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
        (
            (value - valor_anterior)
            / valor_anterior
        ) * 100,
        2
    ) AS variacion_porcentual

FROM variaciones
WHERE valor_anterior IS NOT NULL
ORDER BY variacion DESC
LIMIT 10;


-- ============================================================
-- 9. MAYORES CAÍDAS DIARIAS
-- ============================================================

WITH variaciones AS (
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
        (
            (value - valor_anterior)
            / valor_anterior
        ) * 100,
        2
    ) AS variacion_porcentual

FROM variaciones
WHERE valor_anterior IS NOT NULL
ORDER BY variacion ASC
LIMIT 10;