#app\services\ocr\engine.py
from typing import Protocol


class OCREngine(Protocol):
    """Protocolo para motores OCR.

    El motor solo trabaja con imágenes en memoria (bytes PNG/JPEG).
    No conoce PDFs, rutas, ni el sistema de archivos.
    """

    def extract_text_from_images(self, images: list[bytes]) -> str:
        """Extrae texto de una lista de imágenes.

        Cada elemento es el contenido binario de una imagen (PNG/JPEG).
        Retorna el texto concatenado, separado por doble salto de línea entre páginas.
        """
        ...