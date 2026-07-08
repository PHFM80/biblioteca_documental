import flet as ft

from app.ui.pages.scan_document.scanner_config import scanner_config
from app.ui.pages.scan_document.scan_actions import scan_actions
from app.ui.pages.scan_document.preview import preview
from app.ui.pages.scan_document.pages_area import pages_area
from app.ui.pages.scan_document.finish_actions import finish_actions
from app.services.scanner.scanner_detector import ScannerDetector
from app.services.scanner.exceptions import ScannerNotFoundError, ScannerDetectionError
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
                scanner_name=result.default_scanner.name
            )
        return result.scanners

    except ScannerNotFoundError:
        print("No hay escáneres disponibles.")
        return []

    except ScannerDetectionError as e:
        print(f"Error detectando escáneres: {e}")
        return []

def view():
    """
    Vista principal de escaneo.

    Esta función solamente compone la interfaz.
    La lógica se encuentra en:
    
    services/scanner/
        - detector
        - session
        - apply_configuration
        - scanner

    ui/pages/scan_document/
        - handlers
        - componentes visuales
    """
    scanners = _get_available_scanners()

    return ft.Container(
        expand=True,
        padding=30,

        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=15,

            controls=[

                # -------------------------------------------------
                # Título de la sección
                # -------------------------------------------------

                ft.Text(
                    "Escanear documento",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),


                # -------------------------------------------------
                # Configuración del escáner
                #
                # Actualmente:
                # - muestra configuración de sesión.
                # - muestra dropdowns.
                #
                # Pendiente:
                # - conectar detección automática.
                # - aplicar configuración desde botón.
                # -------------------------------------------------

                section(
                    "Configuración del escáner",
                    scanner_config(scanner_options=scanners),
                ),



                # -------------------------------------------------
                # Acciones principales
                #
                # Botones:
                # - Vista previa.
                # - Escanear página.
                #
                # Pendiente:
                # - conectar eventos.
                # -------------------------------------------------

                scan_actions(),



                # -------------------------------------------------
                # Área grande de vista previa
                #
                # Actualmente:
                # muestra placeholder.
                #
                # Futuro:
                # - imagen escaneada.
                # - zoom.
                # - rotación.
                # - ajustes.
                # -------------------------------------------------

                section(
                    "Vista previa",
                    preview(),
                ),



                # -------------------------------------------------
                # Miniaturas de páginas escaneadas
                #
                # Actualmente:
                # muestra "Próxima página aquí".
                #
                # Futuro:
                # - lista dinámica de páginas.
                # - mover páginas.
                # - eliminar páginas.
                # -------------------------------------------------

                section(
                    "Páginas escaneadas",
                    pages_area(),
                ),



                # -------------------------------------------------
                # Acciones finales
                #
                # Botones:
                # - Guardar documento.
                # - Cancelar.
                #
                # Futuro:
                # Guardar:
                #   -> unir imágenes
                #   -> generar PDF
                #   -> OCR
                #   -> indexar
                #
                # Cancelar:
                #   -> limpiar sesión
                #   -> descartar páginas temporales
                # -------------------------------------------------

                finish_actions(),

            ],
        ),
    )


