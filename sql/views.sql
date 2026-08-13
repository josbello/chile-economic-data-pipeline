CREATE OR REPLACE VIEW vw_monthly_economic_summary AS
WITH mensual AS (
    SELECT
        DATE_TRUNC('month', observation_date)::date AS mes,

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

    GROUP BY DATE_TRUNC('month', observation_date)
)

SELECT *
FROM mensual;

CREATE OR REPLACE VIEW vw_latest_indicators AS
SELECT DISTINCT ON (series_id)
    series_id,
    indicator_name,
    frequency,
    observation_date,
    value
FROM economic_indicators
ORDER BY
    series_id,
    observation_date DESC;