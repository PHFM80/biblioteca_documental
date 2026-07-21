#app\ui\pages\save_document\handlers.py
from app.services.document.save_document_service import SaveDocumentService
from app.services.document.pdf_generator import PDFGenerator
from app.services.document.ocr_service import OCRService
from app.services.document.index_service import IndexService
from app.ui.components.notification import show_message


def save_document(form, page, router, render):
    """
    Ejecuta el flujo de guardado desde la interfaz.
    Obtiene los datos del formulario,
    crea las dependencias necesarias
    y ejecuta el servicio de guardado.
    """

    try:
        data = form.values()

        service = SaveDocumentService(
            pdf_generator=PDFGenerator(),
            ocr_service=OCRService(),
            index_service=IndexService(),
        )

        result = service.save(data)

        show_message(page, "Documento guardado correctamente.") 
        router.navigate("dashboard")
        render()

        return result

    except ValueError as error:
        show_message(page, str(error), error=True)

    except Exception as error:
        show_message(page, f"Error guardando documento: {error}", error=True)