#app\ui\pages\scan_document\handlers.py
import flet as ft
import time

from app.services.scanner.apply_configuration import apply_configuration
from app.services.scanner.exceptions import ScannerError
from app.services.scanner.document_session import document_session
from app.services.scanner.document_session import document_session
from app.services.scanner.thumbnail_service import thumbnail_service
from app.services.scanner.document_session import document_session
from app.services.scanner.scan_coordinator import scan_coordinator


def apply_scanner_configuration(
    e,
    scanner_dropdown,
    dpi_dropdown,
    color_dropdown,
    size_dropdown,
    page,
):
    """
    Aplica la configuración seleccionada por el usuario.
    """

    try:
        dpi = int(
            dpi_dropdown.value.replace(" DPI", "")
        )

        apply_configuration(
            scanner_name=scanner_dropdown.value,
            dpi=dpi,
            color_mode=color_dropdown.value,
            page_size=size_dropdown.value,
        )

        page.update()

    except ScannerError as error:
        show_error(
            page,
            str(error),
        )

def show_error(page: ft.Page, message: str):
    """
    Muestra mensajes de error al usuario.
    """

    snack = ft.SnackBar(
        content=ft.Text(message),
    )

    page.overlay.append(snack)
    snack.open = True
    page.update()

def preview_scan(
    e,
    page,
    preview_view,
):
    """
    Ejecuta una previsualización del escaneo.
    """

    try:
        from app.services.scanner.scanner import ScannerService

        scanner = ScannerService()

        image_path = scanner.preview()

        preview_view.update_image(
            image_path
        )

        page.update()

    except ScannerError as error:
        show_error(
            page,
            str(error),
        )

async def scan_page(e, page, preview_view, pages_view, actions_view):
    """
    Ejecuta un escaneo definitivo.

    Flujo:

    Scanner
        ↓
    Imagen original
        ↓
    Thumbnail
        ↓
    DocumentSession
        ↓
    UI
    """
    if not scan_coordinator.acquire():
        return

    try:
        actions_view.set_scanning(True)
        page.update()

        from app.services.scanner.scanner import ScannerService

        scanner = ScannerService()

        image_path = scanner.scan()

        thumbnail_path = thumbnail_service.create(image_path)

        document_page = document_session.add_page(
            image_path=image_path,
            thumbnail_path=thumbnail_path,
        )

        pages_view.add_page(document_page)

        preview_view.update_image(image_path)

        page.update()

    except ScannerError as error:
        show_error(page, str(error))

    finally:
        scan_coordinator.release()
        actions_view.set_scanning(False)

        if page:
            page.update()

def remove_page(e, page, preview_view, pages_view, page_number: int):
    """
    Elimina una página del documento.
    El handler coordina la actualización de la
    sesión y de la interfaz.
    """
    removed_page = document_session.remove_page(page_number)

    if removed_page is None:
        return
    pages_view.remove_page(page_number)

    last_page = document_session.get_last_page()

    if last_page is None:
        preview_view.clear()
    else:
        preview_view.update_image(
            last_page.image_path
        )

    page.update()

def remove_scanned_page(
    page_number,
    page,
    preview_view,
    pages_view,
):
    """
    Elimina una página del documento actual.
    """

    removed_page = document_session.remove_page(
        page_number
    )

    if removed_page is None:
        return


    pages_view.remove_page(
        page_number
    )


    last_page = document_session.get_last_page()


    if last_page:

        preview_view.update_image(
            last_page.image_path
        )

    else:

        preview_view.clear()


    page.update()


