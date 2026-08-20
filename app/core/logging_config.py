#app\core\logging_config.py
"""
Sistema de logging centralizado.

Uso en cualquier módulo:

    from app.core.logging_config import get_logger

    logger = get_logger(__name__)
    logger.info("Documento guardado correctamente")
    logger.error("Error guardando documento", exc_info=True)
"""

import logging
import logging.handlers
import threading
from pathlib import Path

from app.core.config import APP_NAME, IS_DEVELOPMENT, LOGS_DIR

_lock = threading.Lock()
_configured = False


def setup_logging(level: int = logging.INFO) -> None:
    """Configura el logging global. Idempotente y thread-safe."""
    global _configured

    with _lock:
        if _configured:
            return
        _configured = True

    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-40s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Archivo con rotación (5 MB x 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / f"{APP_NAME}.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    # Consola solo en desarrollo
    if IS_DEVELOPMENT:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        root.addHandler(console)


def get_logger(name: str) -> logging.Logger:
    """Obtiene un logger para el módulo indicado."""
    if not _configured:
        setup_logging()
    return logging.getLogger(name)