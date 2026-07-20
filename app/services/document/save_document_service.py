#app\services\document\save_document_service.py
from app.db.repositories.documento_repository import DocumentoRepository
from app.db.repositories.documento_pdf_repository import DocumentoPDFRepository
from app.services.document.dto.save_document_data import SaveDocumentData
from app.services.document.validators.save_document_validator import SaveDocumentValidator
from app.services.scanner.document_session import document_session
from app.services.scanner.scanner_cleanup import scanner_cleanup


class SaveDocumentService:
    """
    Orquesta el flujo completo de guardado de un documento.

    Coordina servicios independientes.
    No contiene lógica propia de PDF, OCR o indexación.
    """

    def __init__(self, pdf_generator, ocr_service, index_service):
        self.pdf_generator = pdf_generator
        self.ocr_service = ocr_service
        self.index_service = index_service

        self.validator = SaveDocumentValidator()
        self.document_repository = DocumentoRepository()
        self.document_pdf_repository = DocumentoPDFRepository()

    def save(self, data: SaveDocumentData):
        """
        Ejecuta el pipeline completo de guardado.
        """

        errors = self.validator.validate(data)

        if errors:
            raise ValueError(errors)

        pages = document_session.get_pages()

        if not pages:
            raise ValueError("No existen páginas para guardar.")

        pdf_path = self.pdf_generator.generate(pages, data.name)

        # Crear y persistir Documento

        # Crear y persistir DocumentoPDF

        if data.execute_ocr:
            self.ocr_service.process()

        if data.execute_index:
            self.index_service.index()

        scanner_cleanup.cleanup()

        return pdf_path