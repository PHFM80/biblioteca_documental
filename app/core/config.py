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
if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).parent
else:
    APP_DIR = Path(__file__).resolve().parent.parent.parent

# =========================
# ENTORNO
# =========================
ENVIRONMENT = os.getenv("ENVIRONMENT", "production").strip().lower()
IS_DEVELOPMENT = ENVIRONMENT == "development"

# =========================
# RESOLUCIÓN DE RUTAS
# =========================
def _resolve_data_dir() -> Path:
    override = os.getenv("DATA_DIR", "").strip()
    if override:
        path = Path(override)
        return path if path.is_absolute() else APP_DIR / path
    if IS_DEVELOPMENT:
        return APP_DIR / "data"
    return Path(os.getenv("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))) / APP_NAME.replace(" ", "")

def _resolve_library_dir(data_dir: Path) -> Path:
    override = os.getenv("LIBRARY_DIR", "").strip()
    if override:
        path = Path(override)
        return path if path.is_absolute() else APP_DIR / path
    if IS_DEVELOPMENT:
        return data_dir / "library"
    return Path.home() / "Documents" / APP_NAME.replace(" ", "")

DATA_DIR = _resolve_data_dir()
LIBRARY_DIR = _resolve_library_dir(DATA_DIR)

# =========================
# ESTRUCTURA DE DATOS
# =========================
DATABASE_DIR = DATA_DIR / "database"
DB_PATH = DATABASE_DIR / "biblioteca.db"
OCR_DIR = DATA_DIR / "ocr"
INDEX_DIR = DATA_DIR / "indexes"
TEXT_INDEX_DIR = INDEX_DIR / "text"
SEMANTIC_INDEX_DIR = INDEX_DIR / "semantic"
THUMBNAILS_DIR = DATA_DIR / "thumbnails"
TEMP_DIR = DATA_DIR / "temp"
SCANNER_TEMP_DIR = TEMP_DIR / "scanner"
LOGS_DIR = DATA_DIR / "logs"

# =========================
# UTILIDAD
# =========================
def ensure_dirs():
    directories = [
        DATA_DIR,
        DATABASE_DIR,
        LIBRARY_DIR,
        OCR_DIR,
        INDEX_DIR,
        TEXT_INDEX_DIR,
        SEMANTIC_INDEX_DIR,
        THUMBNAILS_DIR,
        TEMP_DIR,
        SCANNER_TEMP_DIR,
        LOGS_DIR,
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)