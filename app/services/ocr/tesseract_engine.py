#app\services\ocr\tesseract_engine.py
from pathlib import Path

import pytesseract
from PIL import Image
import io

from app.services.ocr.engine import OCREngine

# Ruta al ejecutable de Tesseract en Windows
# Ajustar si se instaló en otra ubicación
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class TesseractEngine:
    """Implementación de OCR usando Tesseract.

    - Mejor calidad para español (modelo spa nativo).
    - Correcta segmentación de palabras.
    - Soporte de ñ, tildes y caracteres especiales.
    - Requiere binario externo instalado.
    """

    def __init__(
        self,
        languages: str = "spa+chi_sim+chi_tra+eng",
        tesseract_cmd: str = TESSERACT_CMD,
        dpi: int = 300,
    ):
        self._languages = languages
        self._dpi = dpi
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        self._config = f"--oem 3 --psm 6 -c preserve_interword_spaces=1"

    def extract_text_from_images(self, images: list[bytes]) -> str:
        text_parts: list[str] = []

        for img_bytes in images:
            image = Image.open(io.BytesIO(img_bytes))
            page_text = pytesseract.image_to_string(
                image,
                lang=self._languages,
                config=self._config,
            )
            if page_text.strip():
                text_parts.append(page_text.strip())

        return "\n\n".join(text_parts)
    