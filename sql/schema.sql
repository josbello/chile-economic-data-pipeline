CREATE TABLE IF NOT EXISTS economic_indicators (
    series_id VARCHAR(100) NOT NULL,
    indicator_name VARCHAR(150) NOT NULL,
    frequency VARCHAR(20) NOT NULL,
    observation_date DATE NOT NULL,
    value NUMERIC(12, 4) NOT NULL,
    year SMALLINT NOT NULL,
    month SMALLINT NOT NULL,
    day SMALLINT NOT NULL,
    quarter SMALLINT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (series_id, observation_date)
);

-- ============================================================
-- AUDITORÍA DE EJECUCIONES ETL
-- ============================================================

CREATE TABLE IF NOT EXISTS etl_runs (
    run_id BIGSERIAL PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL,
    records_extracted INTEGER DEFAULT 0,
    records_transformed INTEGER DEFAULT 0,
    records_loaded INTEGER DEFAULT 0,
    duration_seconds NUMERIC(12, 2),
    error_message TEXT
);