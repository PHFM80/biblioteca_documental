from pathlib import Path
import os
import sys
from dotenv import load_dotenv

# =========================
# CARGA .ENV
# =========================
load_dotenv()

# =========================
# CONFIG GENERAL
# =========================
APP_NAME = os.getenv("APP_NAME", "BibliotecaDocumental")

# =========================
# RUTA DE LA APLICACIÓN
# =========================
# Solo se utiliza para localizar recursos de la aplicación
# (assets, iconos, .env, etc.)

if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).parent
else:
    APP_DIR = Path(__file__).resolve().parent.parent.parent

# =========================
# RUTA DE DATOS DEL USUARIO
# =========================
# Todos los datos del usuario se almacenan en:
# C:\Users\<usuario>\AppData\Local\BibliotecaDocumental

LOCAL_APPDATA = Path(os.getenv("LOCALAPPDATA"))
DATA_DIR = LOCAL_APPDATA / APP_NAME

# =========================
# ESTRUCTURA DE DATOS
# =========================
DB_PATH = DATA_DIR / "biblioteca.db"

LIBRARY_DIR = DATA_DIR / "library"

OCR_DIR = DATA_DIR / "ocr"

INDEX_DIR = DATA_DIR / "indexes"
TEXT_INDEX_DIR = INDEX_DIR / "text"
SEMANTIC_INDEX_DIR = INDEX_DIR / "semantic"

THUMBNAILS_DIR = DATA_DIR / "thumbnails"

TEMP_DIR = DATA_DIR / "temp"
SCANNER_TEMP_DIR = TEMP_DIR / "scanner"
IMPORT_TEMP_DIR = TEMP_DIR / "import"
PROCESSING_TEMP_DIR = TEMP_DIR / "processing"

LOGS_DIR = DATA_DIR / "logs"

CONFIG_DIR = DATA_DIR / "config"

# =========================
# UTILIDAD
# =========================
def ensure_dirs():
    """
    Crea toda la estructura de directorios de la aplicación.
    Puede ejecutarse en cada inicio sin inconvenientes.
    """

    directories = [
        DATA_DIR,
        LIBRARY_DIR,
        OCR_DIR,
        INDEX_DIR,
        TEXT_INDEX_DIR,
        SEMANTIC_INDEX_DIR,
        THUMBNAILS_DIR,
        TEMP_DIR,
        SCANNER_TEMP_DIR,
        IMPORT_TEMP_DIR,
        PROCESSING_TEMP_DIR,
        LOGS_DIR,
        CONFIG_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)