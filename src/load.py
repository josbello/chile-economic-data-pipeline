import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

from config import INDICATORS


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

load_dotenv(BASE_DIR / ".env")


def get_connection():
    """
    Crea una conexión con PostgreSQL utilizando
    las variables almacenadas en .env.
    """

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


def load_processed_file(indicator_key):
    """
    Carga el CSV procesado correspondiente
    a un indicador.
    """

    processed_file = (
        PROCESSED_DIR
        / f"{indicator_key}.csv"
    )

    if not processed_file.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo procesado: {processed_file}"
        )

    return pd.read_csv(
        processed_file,
        parse_dates=["fecha"]
    )


def insert_data(connection, data):
    """
    Inserta o actualiza observaciones económicas
    dentro de PostgreSQL.
    """

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
                row["series_id"],
                row["indicator_name"],
                row["frequency"],
                row["fecha"].date(),
                float(row["valor"]),
                int(row["anio"]),
                int(row["mes"]),
                int(row["dia"]),
                int(row["trimestre"]),
            )
        )

    with connection.cursor() as cursor:
        cursor.executemany(
            query,
            records
        )

    connection.commit()

    return len(records)


def main():

    print(
        "=== CARGA DE INDICADORES A POSTGRESQL ==="
    )

    connection = get_connection()

    total_loaded = 0

    try:

        print(
            "Conexión con PostgreSQL establecida correctamente."
        )

        for indicator_key, indicator_config in INDICATORS.items():

            print(
                f"\nCargando: {indicator_config['name']}"
            )

            data = load_processed_file(
                indicator_key
            )

            records_loaded = insert_data(
                connection,
                data
            )

            total_loaded += records_loaded

            print(
                f"Registros procesados para carga: "
                f"{records_loaded}"
            )

        print(
            "\n=== CARGA COMPLETADA ==="
        )
        return total_loaded

    finally:

        connection.close()

        print(
            "Conexión con PostgreSQL cerrada."
        )

    print(
        "\n=== CARGA COMPLETADA ==="
    )


if __name__ == "__main__":
    main()