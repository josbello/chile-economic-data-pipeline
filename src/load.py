import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "dolar_observado_clean.csv"
)

load_dotenv(BASE_DIR / ".env")


SERIES_ID = "F073.TCO.PRE.Z.D"
INDICATOR_NAME = "Dólar observado"
FREQUENCY = "DAILY"


def get_connection():
    required_variables = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing_variables = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing_variables:
        raise RuntimeError(
            f"Faltan variables de entorno: {missing_variables}"
        )

    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def load_processed_data():
    if not PROCESSED_FILE.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo procesado: {PROCESSED_FILE}"
        )

    return pd.read_csv(
        PROCESSED_FILE,
        parse_dates=["fecha"]
    )


def insert_data(connection, data):
    query = """
        INSERT INTO economic_indicators (
            series_id,
            indicator_name,
            frequency,
            observation_date,
            value,
            year,
            month,
            day,
            quarter
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
        ON CONFLICT (series_id, observation_date)
        DO UPDATE SET
            indicator_name = EXCLUDED.indicator_name,
            frequency = EXCLUDED.frequency,
            value = EXCLUDED.value,
            year = EXCLUDED.year,
            month = EXCLUDED.month,
            day = EXCLUDED.day,
            quarter = EXCLUDED.quarter;
    """

    records = []

    for _, row in data.iterrows():
        records.append(
            (
                SERIES_ID,
                INDICATOR_NAME,
                FREQUENCY,
                row["fecha"].date(),
                float(row["dolar_observado"]),
                int(row["anio"]),
                int(row["mes"]),
                int(row["dia"]),
                int(row["trimestre"]),
            )
        )

    with connection.cursor() as cursor:
        cursor.executemany(query, records)

    connection.commit()

    print(f"{len(records)} registros cargados correctamente.")


def main():
    print("=== CARGA DE DATOS A POSTGRESQL ===\n")

    data = load_processed_data()

    print(f"Registros a cargar: {len(data)}")

    connection = get_connection()

    try:
        print("Conexión con PostgreSQL establecida.")

        insert_data(connection, data)

    finally:
        connection.close()
        print("Conexión con PostgreSQL cerrada.")


if __name__ == "__main__":
    main()