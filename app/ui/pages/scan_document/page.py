#app\ui\pages\scan_document\page.py
import flet as ft

from app.ui.pages.scan_document.scanner_config import scanner_config
from app.ui.pages.scan_document.scan_actions import scan_actions
from app.ui.pages.scan_document.preview import preview
from app.ui.pages.scan_document.pages_area import pages_area
from app.ui.pages.scan_document.finish_actions import finish_actions
from app.ui.pages.scan_document.handlers import (preview_scan, scan_page, remove_scanned_page)

from app.services.scanner.scanner_detector import ScannerDetector
from app.services.scanner.exceptions import (
    ScannerNotFoundError,
    ScannerDetectionError,
)
from app.services.scanner.session import scanner_session


def section(title, content):
    """
    Contenedor visual común para separar
    las diferentes áreas de la pantalla.
    """

    return ft.Container(
        padding=15,
        border_radius=10,
        bgcolor=ft.Colors.GREY_100,
        content=ft.Column(
            controls=[
                ft.Text(
                    title,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Divider(),
                content,
            ]
        ),
    )


def _get_available_scanners():
    detector = ScannerDetector()

    try:
        result = detector.detect()

        print(result.message)

        if result.default_scanner:
            scanner_session.update(
                scanner_id=result.default_scanner.id,
                scanner_name=result.default_scanner.name,
            )

        return result.scanners

    except ScannerNotFoundError:
        print("No hay escáneres disponibles.")
        return []

    except ScannerDetectionError as e:
        print(f"Error detectando escáneres: {e}")
        return []

def view(page):
    """
    Vista principal de escaneo.
    """

    scanners = _get_available_scanners()

    preview_view = preview()

    pages_view = pages_area()

    pages_view.set_on_delete(
        lambda page_number: remove_scanned_page(page_number, page, preview_view, pages_view)
    )

    actions_view = scan_actions()
    actions_view.preview_button.on_click = lambda e: preview_scan(e, page, preview_view)
    actions_view.set_scan_handler(lambda e: scan_page(e, page, preview_view, pages_view, actions_view))

    return ft.Container(
        expand=True,
        padding=30,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=15,
            controls=[
                ft.Text(
                    "Escanear documento",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),

                section(
                    "Configuración del escáner",
                    scanner_config(
                        scanner_options=scanners
                    ),
                ),

                actions_view.container,

                section(
                    "Vista previa",
                    preview_view.container,
                ),

                section(
                    "Páginas escaneadas",
                    pages_view.container,
                ),

                finish_actions(),
            ],
        ),
    )