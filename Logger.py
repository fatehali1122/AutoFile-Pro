import logging
from pathlib import Path
from datetime import datetime
import re


_LOGGER_CREATED = False 


def creating_name(name: str):
    name = name.strip()
    name = re.sub(r"[^\w\-]", "_", name)
    return name


def setup_logger(target_path: Path, module_name: str):

    global _LOGGER_CREATED

    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    folder_name = creating_name(target_path.name)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    log_file = logs_dir / f"{folder_name}_{timestamp}.log"

    logger = logging.getLogger("AutoFilePro")
    logger.setLevel(logging.DEBUG)

    if not _LOGGER_CREATED:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s:%(module)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        logger.addHandler(file_handler)
        logger.propagate = False

        _LOGGER_CREATED = True

    return logging.getLogger(f"AutoFilePro.{module_name}")
