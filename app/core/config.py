from pathlib import Path
import os
import sys
from dotenv import load_dotenv

# =========================
# CARGA .ENV
# =========================
load_dotenv()

# =========================
# DETECCIÓN DE BASE_DIR
# =========================
# Soporta:
# - desarrollo (VSCode)
# - ejecutable (.exe)

if getattr(sys, 'frozen', False):
    # Modo .exe (Flet / PyInstaller)
    BASE_DIR = Path(sys.executable).parent
else:
    # Modo desarrollo
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =========================
# RUTAS PRINCIPALES
# =========================
DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data")
LIBRARY_DIR = BASE_DIR / os.getenv("LIBRARY_DIR", "data/library")
OCR_DIR = BASE_DIR / os.getenv("OCR_DIR", "data/ocr")
INDEX_DIR = BASE_DIR / os.getenv("INDEX_DIR", "data/indexes")
DB_DIR = BASE_DIR / os.getenv("DB_DIR", "data/database")
SCANNER_TEMP_DIR = DATA_DIR / "temp" / "scanner"

TEXT_INDEX_DIR = INDEX_DIR / "text"
SEMANTIC_INDEX_DIR = INDEX_DIR / "semantic"

# =========================
# CONFIG GENERAL
# =========================
APP_NAME = os.getenv("APP_NAME", "Biblioteca Documental")

# =========================
# UTILIDAD
# =========================
def ensure_dirs():
    """
    Crea toda la estructura de carpetas si no existe.
    Esto es seguro tanto en dev como en .exe.
    """
    for path in [
        DATA_DIR,
        LIBRARY_DIR,
        OCR_DIR,
        TEXT_INDEX_DIR,
        SEMANTIC_INDEX_DIR,
        DB_DIR,
        SCANNER_TEMP_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)