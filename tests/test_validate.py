import pandas as pd
import pytest

from validate import validate_dataframe


CONFIG = {
    "series_id": "TEST.SERIES",
    "name": "Indicador de prueba",
    "frequency": "DAILY",
    "min_value": 0,
}


def valid_dataframe():
    return pd.DataFrame(
        {
            "series_id": [
                "TEST.SERIES",
                "TEST.SERIES",
            ],
            "indicator_name": [
                "Indicador de prueba",
                "Indicador de prueba",
            ],
            "frequency": [
                "DAILY",
                "DAILY",
            ],
            "fecha": [
                "2025-01-01",
                "2025-01-02",
            ],
            "valor": [
                100.0,
                101.0,
            ],
            "anio": [
                2025,
                2025,
            ],
            "mes": [
                1,
                1,
            ],
            "dia": [
                1,
                2,
            ],
            "trimestre": [
                1,
                1,
            ],
        }
    )


def test_valid_dataframe():
    df = valid_dataframe()

    result = validate_dataframe(
        df,
        "test",
        CONFIG,
    )

    assert result == 2


def test_duplicate_dates_fail():
    df = valid_dataframe()

    df.loc[1, "fecha"] = df.loc[0, "fecha"]

    with pytest.raises(
        ValueError,
        match="fechas duplicadas",
    ):
        validate_dataframe(
            df,
            "test",
            CONFIG,
        )


def test_null_value_fail():
    df = valid_dataframe()

    df.loc[0, "valor"] = None

    with pytest.raises(
        ValueError,
        match="valores nulos",
    ):
        validate_dataframe(
            df,
            "test",
            CONFIG,
        )


def test_wrong_series_id_fail():
    df = valid_dataframe()

    df.loc[0, "series_id"] = "SERIE.INCORRECTA"

    with pytest.raises(
        ValueError,
        match="series_id incorrecto",
    ):
        validate_dataframe(
            df,
            "test",
            CONFIG,
        )


def test_negative_value_fail():
    df = valid_dataframe()

    df.loc[0, "valor"] = -10

    with pytest.raises(
        ValueError,
        match="valores menores",
    ):
        validate_dataframe(
            df,
            "test",
            CONFIG,
        )