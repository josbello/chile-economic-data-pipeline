import os

import psycopg


def get_connection():
    """
    Crea una conexión a PostgreSQL usando
    las variables de entorno del proyecto.
    """

    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def start_run():
    """
    Registra el inicio de una ejecución ETL.
    Devuelve el ID generado.
    """

    query = """
        INSERT INTO etl_runs (
            status
        )
        VALUES ('RUNNING')
        RETURNING run_id;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            run_id = cursor.fetchone()[0]

        connection.commit()

    return run_id


def finish_run(
    run_id,
    records_extracted,
    records_transformed,
    records_loaded,
    duration_seconds,
):
    """
    Marca una ejecución como completada correctamente.
    """

    query = """
        UPDATE etl_runs
        SET
            finished_at = CURRENT_TIMESTAMP,
            status = 'SUCCESS',
            records_extracted = %s,
            records_transformed = %s,
            records_loaded = %s,
            duration_seconds = %s
        WHERE run_id = %s;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    records_extracted,
                    records_transformed,
                    records_loaded,
                    duration_seconds,
                    run_id,
                ),
            )

        connection.commit()


def fail_run(run_id, duration_seconds, error_message):
    """
    Registra una ejecución fallida.
    """

    query = """
        UPDATE etl_runs
        SET
            finished_at = CURRENT_TIMESTAMP,
            status = 'FAILED',
            duration_seconds = %s,
            error_message = %s
        WHERE run_id = %s;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    duration_seconds,
                    str(error_message),
                    run_id,
                ),
            )

        connection.commit()