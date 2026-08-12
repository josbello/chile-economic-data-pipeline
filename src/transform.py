from pathlib import Path

import pandas as pd

from config import INDICATORS


# ============================================================
# RUTAS DEL PROYECTO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def load_raw_data(indicator_key):
    """
    Carga el archivo RAW correspondiente a un indicador.
    """

    raw_file = RAW_DIR / f"{indicator_key}.csv"

    if not raw_file.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo RAW: {raw_file}"
        )

    return pd.read_csv(raw_file)


def transform_indicator(data, indicator_key, indicator_config):
    """
    Limpia, valida y normaliza un indicador económico.
    """

    df = data.copy()

    expected_columns = {
        "fecha",
        indicator_key,
    }

    if not expected_columns.issubset(df.columns):
        raise ValueError(
            f"El archivo de {indicator_key} debe contener "
            f"las columnas: {expected_columns}"
        )

    print(f"\nTransformando: {indicator_config['name']}")
    print("-" * 60)

    print(f"Registros RAW: {len(df)}")

    # ========================================================
    # 1. CONVERSIÓN DE TIPOS
    # ========================================================

    df["fecha"] = pd.to_datetime(
        df["fecha"],
        errors="coerce"
    )

    df[indicator_key] = pd.to_numeric(
        df[indicator_key],
        errors="coerce"
    )

    # ========================================================
    # 2. CONTROL DE CALIDAD
    # ========================================================

    invalid_dates = df["fecha"].isna().sum()

    null_values = df[indicator_key].isna().sum()

    duplicates = df.duplicated(
        subset=["fecha"]
    ).sum()

    today = pd.Timestamp.today().normalize()

    future_dates = (
        df["fecha"] > today
    ).sum()

    print(f"Fechas inválidas: {invalid_dates}")
    print(f"Valores nulos: {null_values}")
    print(f"Fechas duplicadas: {duplicates}")
    print(f"Registros con fecha futura: {future_dates}")

    # ========================================================
    # 3. LIMPIEZA
    # ========================================================

    # Eliminar fechas inválidas
    df = df.dropna(
        subset=["fecha"]
    )

    # Eliminar registros sin valor
    df = df.dropna(
        subset=[indicator_key]
    )

    # Eliminar duplicados
    df = df.drop_duplicates(
        subset=["fecha"],
        keep="last"
    )

    # Los archivos RAW conservan posibles datos futuros,
    # pero el dataset procesado solo considera datos hasta hoy.
    df = df[
        df["fecha"] <= today
    ]

    # ========================================================
    # 4. VALIDACIÓN DEL VALOR
    # ========================================================

    min_value = indicator_config.get("min_value")

    if min_value is not None:

        invalid_values = (
            df[indicator_key] < min_value
        ).sum()

        print(
            f"Valores menores a {min_value}: "
            f"{invalid_values}"
        )

        df = df[
            df[indicator_key] >= min_value
        ]

    # ========================================================
    # 5. NORMALIZACIÓN
    # ========================================================

    # Todos los indicadores utilizarán la misma columna
    # para representar su valor.
    df = df.rename(
        columns={
            indicator_key: "valor"
        }
    )

    # Agregar metadatos
    df["series_id"] = indicator_config["series_id"]
    df["indicator_name"] = indicator_config["name"]
    df["frequency"] = indicator_config["frequency"]

    # ========================================================
    # 6. VARIABLES TEMPORALES
    # ========================================================

    df["anio"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    df["dia"] = df["fecha"].dt.day
    df["trimestre"] = df["fecha"].dt.quarter

    # Orden cronológico
    df = df.sort_values(
        by="fecha"
    )

    # Reiniciar índice
    df = df.reset_index(
        drop=True
    )

    # ========================================================
    # 7. ORDEN DE COLUMNAS
    # ========================================================

    df = df[
        [
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
    ]

    return df


def save_processed_data(data, indicator_key):
    """
    Guarda un indicador transformado.
    """

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        PROCESSED_DIR
        / f"{indicator_key}.csv"
    )

    data.to_csv(
        output_file,
        index=False
    )

    print(
        f"Registros procesados: {len(data)}"
    )

    print(
        f"Archivo procesado guardado en: "
        f"{output_file}"
    )


def main():

    print(
        "=== TRANSFORMACIÓN DE INDICADORES ECONÓMICOS ==="
    )

    for indicator_key, indicator_config in INDICATORS.items():

        raw_data = load_raw_data(
            indicator_key
        )

        clean_data = transform_indicator(
            raw_data,
            indicator_key,
            indicator_config
        )

        save_processed_data(
            clean_data,
            indicator_key
        )

    print(
        "\n=== TRANSFORMACIÓN COMPLETADA ==="
    )


if __name__ == "__main__":
    main()