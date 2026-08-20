#app\ui\pages\save_document\handlers.py
import asyncio
import flet as ft

from app.core.logging_config import get_logger
from app.services.document.save_document_service import SaveDocumentService
from app.services.document.pdf_generator import PDFGenerator
from app.services.ocr import OCRService, RapidOCREngine
from app.services.ocr.tesseract_engine import TesseractEngine
from app.services.document.index_service import IndexService
from app.ui.components.notification import show_message

logger = get_logger(__name__)

def save_document(form, page, router, render):
    page.run_task(_save_task, form, page, router, render)


async def _save_task(form, page, router, render):
    try:
        data = form.values()
        logger.info(f"Iniciando guardado de documento: {data.name}")

        # Crear servicio con el engine de OCR
        ocr_service = OCRService(engine=TesseractEngine())
        index_service = IndexService()

        service = SaveDocumentService(
            pdf_generator=PDFGenerator(),
            ocr_service=ocr_service,
            index_service=index_service,
        )

        try:
            # Ejecutar la operación bloqueante en un hilo del pool
            # sin bloquear el event loop de Flet
            result = await asyncio.to_thread(service.save, data)

            logger.info(f"Documento guardado exitosamente: {data.name} -> {result}")
            show_message(page, "Documento guardado correctamente.")
            router.navigate("dashboard")
            render()

        except ValueError as error:
            logger.warning(f"Error de validación al guardar {data.name}: {error}")
            show_message(page, str(error), error=True)

        except Exception as error:
            logger.error(f"Error inesperado al guardar {data.name}: {error}", exc_info=True)
            show_message(page, f"Error guardando documento: {error}", error=True)

    except ValueError as error:
        logger.warning(f"Error de validación en formulario: {error}")
        show_message(page, str(error), error=True)

    except Exception as error:
        logger.error(f"Error inesperado en handler: {error}", exc_info=True)
        show_message(page, f"Error guardando documento: {error}", error=True)