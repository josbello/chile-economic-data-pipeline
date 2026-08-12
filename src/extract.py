import os
from pathlib import Path

import bcchapi
from dotenv import load_dotenv

from config import INDICATORS


# Ruta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpeta donde se guardarán los datos RAW
RAW_DIR = BASE_DIR / "data" / "raw"

# Cargar variables de entorno
load_dotenv(BASE_DIR / ".env")


def get_client():
    """
    Crea un cliente para conectarse a la API BDE
    del Banco Central de Chile.
    """

    user = os.getenv("BCCH_USER")
    password = os.getenv("BCCH_PASSWORD")

    if not user or not password:
        raise RuntimeError(
            "No se encontraron las credenciales BCCH_USER y BCCH_PASSWORD."
        )

    return bcchapi.Siete(user, password)


def extract_indicator(client, indicator_key, indicator_config):
    """
    Extrae una serie económica desde la API BDE.
    """

    series_id = indicator_config["series_id"]
    start_date = indicator_config["start_date"]
    indicator_name = indicator_config["name"]

    print(f"\nExtrayendo: {indicator_name}")
    print(f"Serie: {series_id}")
    print(f"Desde: {start_date}")

    data = client.cuadro(
        series=[series_id],
        desde=start_date,
        nombres=[indicator_key]
    )

    if data.empty:
        raise RuntimeError(
            f"No se obtuvieron datos para {indicator_name}."
        )

    print(f"Registros obtenidos: {len(data)}")

    return data


def save_raw_data(data, indicator_key):
    """
    Guarda los datos obtenidos desde la API
    sin aplicar transformaciones.
    """

    RAW_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = RAW_DIR / f"{indicator_key}.csv"

    data.to_csv(
        output_file,
        index=True,
        index_label="fecha"
    )

    print(f"Archivo guardado en: {output_file}")


def main():
    print("=== EXTRACCIÓN DE INDICADORES ECONÓMICOS ===")

    client = get_client()

    print("Conexión con la API BDE configurada correctamente.")

    for indicator_key, indicator_config in INDICATORS.items():

        data = extract_indicator(
            client,
            indicator_key,
            indicator_config
        )

        save_raw_data(
            data,
            indicator_key
        )

    print("\n=== EXTRACCIÓN COMPLETADA ===")


if __name__ == "__main__":
    main()