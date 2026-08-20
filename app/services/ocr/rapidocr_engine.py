#app\services\ocr\rapidocr_engine.py
from rapidocr_onnxruntime import RapidOCR


class RapidOCREngine:
    """Implementación de OCR usando RapidOCR (ONNX Runtime).

    - Instalable vía pip sin binarios externos.
    - Soporta español y chino.
    - Acepta bytes de imagen directamente.
    """

    def __init__(self):
        self._engine: RapidOCR | None = None

    @property
    def engine(self) -> RapidOCR:
        if self._engine is None:
            self._engine = RapidOCR()
        return self._engine

    def extract_text_from_images(self, images: list[bytes]) -> str:
        text_parts: list[str] = []

        for img_bytes in images:
            result, _ = self.engine(img_bytes)
            if result:
                page_text = "\n".join(line[1] for line in result)
                if page_text.strip():
                    text_parts.append(page_text)

        return "\n\n".join(text_parts)