import os
from pathlib import Path

import bcchapi
from dotenv import load_dotenv


# Ruta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno
load_dotenv(BASE_DIR / ".env")


# Código oficial de la serie diaria del dólar observado
DOLLAR_SERIES_ID = "F073.TCO.PRE.Z.D"


def get_client():
    """
    Crea el cliente para conectarse a la API BDE
    del Banco Central de Chile.
    """

    user = os.getenv("BCCH_USER")
    password = os.getenv("BCCH_PASSWORD")

    if not user or not password:
        raise RuntimeError(
            "No se encontraron las credenciales del Banco Central."
        )

    return bcchapi.Siete(user, password)


def extract_dollar_data(client):
    """
    Extrae los datos históricos del dólar observado
    desde el año 2020.
    """

    print("Extrayendo datos del dólar observado...")

    data = client.cuadro(
        series=[DOLLAR_SERIES_ID],
        desde="2020-01-01",
        nombres=["dolar_observado"]
    )

    return data


def save_raw_data(data):
    """
    Guarda los datos extraídos sin transformar.
    """

    raw_directory = BASE_DIR / "data" / "raw"

    raw_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = raw_directory / "dolar_observado.csv"

    data.to_csv(
        output_file,
        index=True,
        index_label="fecha"
    )

    print(f"Datos guardados en: {output_file}")


def main():
    print("Conectando con la API BDE...")

    client = get_client()

    print("Conexión configurada correctamente.")

    dollar_data = extract_dollar_data(client)

    print("\nPrimeras observaciones:")
    print(dollar_data.head())

    print("\nÚltimas observaciones:")
    print(dollar_data.tail())

    print(f"\nTotal de registros: {len(dollar_data)}")

    save_raw_data(dollar_data)


if __name__ == "__main__":
    main()