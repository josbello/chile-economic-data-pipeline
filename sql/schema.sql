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