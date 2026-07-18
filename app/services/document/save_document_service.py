#app\services\document\save_document_service.py
from app.db.repositories.documento_repository import DocumentoRepository
from app.db.repositories.documento_pdf_repository import DocumentoPDFRepository
from app.services.scanner.scanner_cleanup import scanner_cleanup
from app.services.scanner.document_session import document_session


class SaveDocumentService:
    """
    Orquesta el flujo completo de guardado
    de un documento escaneado.
    No contiene lógica específica de generación,
    OCR o indexación.
    Solo coordina servicios independientes.
    """

    def __init__(self, pdf_generator, ocr_service, index_service):
        self.pdf_generator = pdf_generator
        self.ocr_service = ocr_service
        self.index_service = index_service

        self.document_repository = DocumentoRepository()
        self.document_pdf_repository = DocumentoPDFRepository()

    def save(self, name: str, execute_ocr: bool, execute_index: bool):
        """
        Ejecuta el pipeline completo de guardado.
        """
        pages = document_session.get_pages()

        # 1. Generar PDF definitivo
        pdf_path = self.pdf_generator.generate(pages, name)

        # 2. Registrar documento
        # pendiente implementar creación del modelo Documento

        # 3. Registrar información PDF
        # pendiente implementar creación DocumentoPDF

        # 4. OCR opcional
        if execute_ocr:
            self.ocr_service.process()
        # 5. Indexación opcional
        if execute_index:
            self.index_service.index()
        # 6. Limpieza temporales
        scanner_cleanup.cleanup()

        return pdf_path