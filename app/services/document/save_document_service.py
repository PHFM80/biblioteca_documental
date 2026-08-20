#app\services\document\save_document_service.py
import uuid
from datetime import datetime
from pathlib import Path

import blake3

from app.core.config import LIBRARY_DIR
from app.db.repositories.documento_repository import DocumentoRepository
from app.db.repositories.documento_pdf_repository import DocumentoPDFRepository
from app.models import Documento, DocumentoPDF
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

        # 1. Generar ruta definitiva
        pdf_filename = f"{uuid.uuid4().hex}.pdf"
        pdf_path = LIBRARY_DIR / pdf_filename

        # 2. Generar el PDF en la ruta definitiva
        self.pdf_generator.generate(pages, pdf_path)

        # 3. Calcular tamaño
        file_size = pdf_path.stat().st_size

        # 4. Calcular hash BLAKE3
        file_hash = self._calculate_hash(pdf_path)

        # 5. Verificar duplicados por hash
        if self.document_repository.exists_by_hash(file_hash):
            pdf_path.unlink()
            raise ValueError("El documento ya existe en la biblioteca.")

        # 6. Crear Documento
        documento = Documento(
            id=None,
            nombre=data.name,
            tipo_id=1,
            ruta=str(pdf_path),
            tamaño_bytes=file_size,
            fecha_creacion=datetime.now(),
            fecha_modificacion=datetime.now(),
            observaciones=data.observations,
            hash_archivo=file_hash,
        )

        # 7. Persistir Documento
        documento = self.document_repository.create(documento)

        # 8. Crear DocumentoPDF
        documento_pdf = DocumentoPDF(
            documento_id=documento.id,
            cantidad_paginas=len(pages),
            tiene_ocr=data.execute_ocr,
            nombre_chino=data.chinese_name,
            fecha_recepcion=data.reception_date,
            tiene_indexacion=data.execute_index,
        )

        # 9. Persistir DocumentoPDF
        self.document_pdf_repository.create(documento_pdf)

        # 10. Ejecutar OCR si corresponde
        source_images = [Path(page.image_path) for page in pages]
        if data.execute_ocr:
            self.ocr_service.process(documento.id, source_images=source_images)

        # 11. Ejecutar Indexación si corresponde
        if data.execute_index:
            self.index_service.index(documento.id)

        # 12. Limpiar sesión
        scanner_cleanup.cleanup()

        return pdf_path

    @staticmethod
    def _calculate_hash(file_path: Path) -> str:
        """Calcula el hash BLAKE3 de un archivo."""
        hasher = blake3.blake3()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()