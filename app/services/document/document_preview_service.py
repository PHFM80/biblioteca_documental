#app\services\document\document_preview_service.py
from pathlib import Path

from app.core.config import PROCESSING_TEMP_DIR
from app.services.document.pdf_generator import PDFGenerator
from app.services.scanner.document_session import document_session


class DocumentPreviewService:
    """
    Genera el PDF temporal utilizado como vista previa
    antes del guardado definitivo.
    """

    def __init__(self, pdf_generator: PDFGenerator):
        self.pdf_generator = pdf_generator

    def generate(self) -> Path:
        """
        Genera el archivo PDF temporal de preview.
        """
        if not document_session.has_pages():
            raise ValueError("No existen páginas escaneadas para generar preview.")
        output_path = PROCESSING_TEMP_DIR / "preview.pdf"

        return self.pdf_generator.generate(document_session.get_pages(), output_path)