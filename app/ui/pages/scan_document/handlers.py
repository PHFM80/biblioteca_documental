import flet as ft

from app.services.scanner.apply_configuration import apply_configuration
from app.services.scanner.exceptions import ScannerError


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