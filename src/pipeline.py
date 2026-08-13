import time

from audit import (
    fail_run,
    finish_run,
    start_run,
)
from extract import main as extract_main
from load import main as load_main
from logger import get_logger
from transform import main as transform_main
from validate import main as validate_main


logger = get_logger()


def main():

    logger.info(
        "============================================================"
    )

    logger.info(
        "CHILE ECONOMIC DATA PIPELINE"
    )

    logger.info(
        "============================================================"
    )

    start_time = time.time()

    run_id = None

    try:

        run_id = start_run()

        logger.info(
            f"ETL run iniciado. run_id={run_id}"
        )

        # ====================================================
        # EXTRACT
        # ====================================================

        logger.info(
            "[1/4] Iniciando EXTRACT"
        )

        records_extracted = extract_main()

        logger.info(
            f"EXTRACT completado: "
            f"{records_extracted} registros obtenidos"
        )

        # ====================================================
        # TRANSFORM
        # ====================================================

        logger.info(
            "[2/4] Iniciando TRANSFORM"
        )

        records_transformed = transform_main()

        logger.info(
            f"TRANSFORM completado: "
            f"{records_transformed} registros procesados"
        )

        # ====================================================
        # VALIDATE
        # ====================================================

        logger.info(
            "[3/4] Iniciando VALIDATE"
        )

        records_validated = validate_main()

        logger.info(
            f"VALIDATE completado: "
            f"{records_validated} registros validados"
        )

        # ====================================================
        # LOAD
        # ====================================================

        logger.info(
            "[4/4] Iniciando LOAD"
        )

        records_loaded = load_main()

        logger.info(
            f"LOAD completado: "
            f"{records_loaded} registros procesados"
        )

        # ====================================================
        # FINALIZACIÓN
        # ====================================================

        duration = round(
            time.time() - start_time,
            2
        )

        finish_run(
            run_id=run_id,
            records_extracted=records_extracted,
            records_transformed=records_transformed,
            records_loaded=records_loaded,
            duration_seconds=duration,
        )

        logger.info(
            f"PIPELINE COMPLETADO CORRECTAMENTE "
            f"en {duration} segundos"
        )

    except Exception as error:

        duration = round(
            time.time() - start_time,
            2
        )

        logger.exception(
            "PIPELINE FAILED"
        )

        if run_id is not None:

            fail_run(
                run_id=run_id,
                duration_seconds=duration,
                error_message=error,
            )

        raise


if __name__ == "__main__":
    main()