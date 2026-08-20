#app\core\init.py
from app.core.config import ensure_dirs
from app.core.logging_config import setup_logging

def initialize_app():
    """
    Inicializa toda la infraestructura base de la aplicación.
    """
    ensure_dirs()
    setup_logging()