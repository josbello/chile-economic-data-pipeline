from pathlib import Path

import pandas as pd

from config import INDICATORS


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


REQUIRED_COLUMNS = [
    "series_id",
    "indicator_name",
    "frequency",
    "fecha",
    "valor",
    "anio",
    "mes",
    "dia",
    "trimestre",
]


def validate_dataframe(data, indicator_key, indicator_config):
    """
    Valida la calidad del dataset procesado de un indicador.
    """

    if data.empty:
        raise ValueError(
            f"{indicator_key}: el dataset procesado está vacío."
        )

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{indicator_key}: faltan columnas: {missing_columns}"
        )

    df = data.copy()

    df["fecha"] = pd.to_datetime(
        df["fecha"],
        errors="coerce"
    )

    df["valor"] = pd.to_numeric(
        df["valor"],
        errors="coerce"
    )

    errors = []

    # --------------------------------------------------------
    # Fechas inválidas
    # --------------------------------------------------------

    invalid_dates = df["fecha"].isna().sum()

    if invalid_dates > 0:
        errors.append(
            f"{invalid_dates} fechas inválidas"
        )

    # --------------------------------------------------------
    # Valores nulos o no numéricos
    # --------------------------------------------------------

    null_values = df["valor"].isna().sum()

    if null_values > 0:
        errors.append(
            f"{null_values} valores nulos o inválidos"
        )

    # --------------------------------------------------------
    # Fechas duplicadas
    # --------------------------------------------------------

    duplicate_dates = df.duplicated(
        subset=["fecha"]
    ).sum()

    if duplicate_dates > 0:
        errors.append(
            f"{duplicate_dates} fechas duplicadas"
        )

    # --------------------------------------------------------
    # Fechas futuras
    # --------------------------------------------------------

    today = pd.Timestamp.today().normalize()

    future_dates = (
        df["fecha"] > today
    ).sum()

    if future_dates > 0:
        errors.append(
            f"{future_dates} fechas futuras"
        )

    # --------------------------------------------------------
    # Series ID
    # --------------------------------------------------------

    expected_series_id = indicator_config["series_id"]

    invalid_series = (
        df["series_id"] != expected_series_id
    ).sum()

    if invalid_series > 0:
        errors.append(
            f"{invalid_series} registros con series_id incorrecto"
        )

    # --------------------------------------------------------
    # Frecuencia
    # --------------------------------------------------------

    expected_frequency = indicator_config["frequency"]

    invalid_frequency = (
        df["frequency"] != expected_frequency
    ).sum()

    if invalid_frequency > 0:
        errors.append(
            f"{invalid_frequency} registros con frecuencia incorrecta"
        )

    # --------------------------------------------------------
    # Valor mínimo
    # --------------------------------------------------------

    min_value = indicator_config.get("min_value")

    if min_value is not None:

        invalid_values = (
            df["valor"] < min_value
        ).sum()

        if invalid_values > 0:
            errors.append(
                f"{invalid_values} valores menores a {min_value}"
            )

    # --------------------------------------------------------
    # Resultado
    # --------------------------------------------------------

    if errors:
        raise ValueError(
            f"{indicator_config['name']}: "
            + " | ".join(errors)
        )

    return len(df)


def validate_processed_file(
    indicator_key,
    indicator_config
):
    """
    Carga y valida un archivo procesado.
    """

    processed_file = (
        PROCESSED_DIR
        / f"{indicator_key}.csv"
    )

    if not processed_file.exists():
        raise FileNotFoundError(
            f"No se encontró: {processed_file}"
        )

    data = pd.read_csv(
        processed_file
    )

    records_validated = validate_dataframe(
        data,
        indicator_key,
        indicator_config
    )

    print(
        f"{indicator_config['name']}: "
        f"{records_validated} registros OK"
    )

    return records_validated


def main():

    print(
        "=== VALIDACIÓN DE CALIDAD DE DATOS ==="
    )

    total_validated = 0

    for indicator_key, indicator_config in INDICATORS.items():

        total_validated += validate_processed_file(
            indicator_key,
            indicator_config
        )

    print(
        f"\nTotal validado: {total_validated}"
    )

    print(
        "=== VALIDACIÓN COMPLETADA ==="
    )

    return total_validated


if __name__ == "__main__":
    main()