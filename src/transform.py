from pathlib import Path

import pandas as pd


# Ruta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Archivos de entrada y salida
RAW_FILE = BASE_DIR / "data" / "raw" / "dolar_observado.csv"

PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_FILE = PROCESSED_DIR / "dolar_observado_clean.csv"


def load_raw_data():
    """
    Carga el archivo RAW generado en la fase de extracción.
    """

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo RAW: {RAW_FILE}"
        )

    return pd.read_csv(RAW_FILE)


def transform_data(data):
    """
    Limpia, valida y transforma los datos
    correspondientes al dólar observado.
    """

    # Trabajamos sobre una copia para no modificar
    # accidentalmente el DataFrame original
    df = data.copy()

    expected_columns = {"fecha", "dolar_observado"}

    if not expected_columns.issubset(df.columns):
        raise ValueError(
            f"El archivo debe contener las columnas: {expected_columns}"
        )

    print(f"Registros RAW: {len(df)}")

    # -------------------------------------------------
    # 1. CONVERSIÓN DE TIPOS
    # -------------------------------------------------

    df["fecha"] = pd.to_datetime(
        df["fecha"],
        errors="coerce"
    )

    df["dolar_observado"] = pd.to_numeric(
        df["dolar_observado"],
        errors="coerce"
    )

    # -------------------------------------------------
    # 2. CONTROL DE CALIDAD
    # -------------------------------------------------

    invalid_dates = df["fecha"].isna().sum()

    null_values = df["dolar_observado"].isna().sum()

    duplicates = df.duplicated(
        subset=["fecha"]
    ).sum()

    print(f"Fechas inválidas: {invalid_dates}")
    print(f"Valores nulos: {null_values}")
    print(f"Fechas duplicadas: {duplicates}")

    # -------------------------------------------------
    # 3. LIMPIEZA
    # -------------------------------------------------

    # Eliminar registros sin una fecha válida
    df = df.dropna(
        subset=["fecha"]
    )

    # Eliminar días sin valor observado
    df = df.dropna(
        subset=["dolar_observado"]
    )

    # Eliminar posibles fechas duplicadas
    df = df.drop_duplicates(
        subset=["fecha"],
        keep="last"
    )

    # El dólar observado debe ser un valor positivo
    df = df[
        df["dolar_observado"] > 0
    ]

    # -------------------------------------------------
    # 4. ORDENAMIENTO
    # -------------------------------------------------

    df = df.sort_values(
        by="fecha"
    )
    
    # Reiniciar índice después de la limpieza
    df = df.reset_index(drop=True)

    # -------------------------------------------------
    # 5. NUEVAS VARIABLES PARA ANÁLISIS
    # -------------------------------------------------

    df["anio"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    df["dia"] = df["fecha"].dt.day
    df["trimestre"] = df["fecha"].dt.quarter

    return df


def save_processed_data(data):
    """
    Guarda el DataFrame limpio en la carpeta processed.
    """

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    data.to_csv(
        PROCESSED_FILE,
        index=False
    )

    print(
        f"\nDatos procesados guardados en:\n{PROCESSED_FILE}"
    )


def main():
    print("=== TRANSFORMACIÓN DE DATOS ===\n")

    raw_data = load_raw_data()

    clean_data = transform_data(raw_data)

    print(f"\nRegistros procesados: {len(clean_data)}")

    print("\nPrimeros registros:")
    print(clean_data.head())

    print("\nÚltimos registros:")
    print(clean_data.tail())

    save_processed_data(clean_data)


if __name__ == "__main__":
    main()