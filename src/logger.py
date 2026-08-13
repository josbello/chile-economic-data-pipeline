import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = LOG_DIR / "pipeline.log"


def get_logger():

    logger = logging.getLogger(
        "chile_economic_pipeline"
    )

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Consola
    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )

    # Archivo
    file_handler = logging.FileHandler(
        LOG_FILE
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )

    logger.addHandler(
        file_handler
    )

    return logger