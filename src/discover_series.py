from extract import get_client


def search_series(client, term, title_filter=None, frequency=None):
    print(f"\n{'=' * 80}")
    print(f"BUSCANDO: {term}")
    print("=" * 80)

    results = client.buscar(term)

    if results.empty:
        print("No se encontraron resultados.")
        return

    # Filtrar por frecuencia
    if frequency:
        results = results[
            results["frequencyCode"] == frequency
        ]

    # Filtrar por palabras contenidas en el título
    if title_filter:
        results = results[
            results["spanishTitle"].str.contains(
                title_filter,
                case=False,
                na=False
            )
        ]

    columns = [
        "seriesId",
        "frequencyCode",
        "spanishTitle",
        "firstObservation",
        "lastObservation",
    ]

    if results.empty:
        print("No quedaron resultados después de aplicar los filtros.")
        return

    print(
        results[columns]
        .head(30)
        .to_string(index=False)
    )


def main():
    client = get_client()

    # UF
    search_series(
        client,
        term="Unidad de Fomento",
        title_filter="Unidad de Fomento",
        frequency="DAILY"
    )

    # TPM
    search_series(
        client,
        term="Tasa de Política Monetaria",
        title_filter="Política Monetaria",
        frequency="DAILY"
    )

    # IPC Chile
    search_series(
        client,
        term="IPC General",
        title_filter="IPC",
        frequency="MONTHLY"
    )


if __name__ == "__main__":
    main()