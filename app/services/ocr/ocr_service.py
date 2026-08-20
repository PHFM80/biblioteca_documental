#app\services\ocr\ocr_service.py
from pathlib import Path

import fitz

from app.core.config import OCR_DIR
from app.db.repositories.documento_pdf_repository import DocumentoPDFRepository
from app.db.repositories.documento_repository import DocumentoRepository
from app.services.ocr.engine import OCREngine


class OCRService:
    """Extrae texto de documentos y actualiza la base de datos.

    Estrategia de origen:
    - Si se proporcionan source_images (sesión de escaneo), las usa directamente.
    - Si no, renderiza el PDF del documento a imágenes en memoria.
    """

    def __init__(self, engine: OCREngine):
        self._engine = engine
        self._doc_repo = DocumentoRepository()
        self._doc_pdf_repo = DocumentoPDFRepository()

    def process(self, document_id: int, source_images: list[Path] | None = None) -> Path:
        documento = self._doc_repo.get_by_id(document_id)
        if documento is None:
            raise ValueError(f"Documento {document_id} no encontrado")

        images = self._resolve_images(documento, source_images)
        text = self._engine.extract_text_from_images(images)

        OCR_DIR.mkdir(parents=True, exist_ok=True)
        ocr_text_path = OCR_DIR / f"{document_id}.txt"
        ocr_text_path.write_text(text, encoding="utf-8")

        self._doc_pdf_repo.set_ocr(document_id, str(ocr_text_path))
        return ocr_text_path

    def _resolve_images(self, documento, source_images: list[Path] | None) -> list[bytes]:
        if source_images:
            return [p.read_bytes() for p in source_images]

        pdf_path = Path(documento.ruta)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF no encontrado: {pdf_path}")
        return self._render_pdf(pdf_path)

    def _render_pdf(self, pdf_path: Path) -> list[bytes]:
        """Renderiza un PDF a imágenes PNG en memoria (sin archivos temporales)."""
        images: list[bytes] = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                pix = page.get_pixmap(dpi=300)
                images.append(pix.tobytes("png"))
        return images