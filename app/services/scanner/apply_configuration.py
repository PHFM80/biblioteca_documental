from app.services.scanner.exceptions import ScannerConfigurationError
from app.services.scanner.session import scanner_session


VALID_DPI = {150, 300, 600}

VALID_COLOR_MODES = {
    "Blanco y negro",
    "Escala de grises",
    "Color",
}

VALID_PAGE_SIZES = {
    "Automático",
    "A4",
    "Carta",
    "Oficio",
    "Sobre",
}


def apply_configuration(
    *,
    scanner_id: str | None,
    scanner_name: str,
    dpi: int,
    color_mode: str,
    page_size: str,
):
    """
    Valida y aplica la configuración de escaneo a la sesión actual.

    Parameters
    ----------
    scanner_name : str
        Nombre del escáner seleccionado.
    dpi : int
        Resolución en DPI.
    color_mode : str
        Modo de color.
    page_size : str
        Tamaño de página.
    """

    scanner_name = (scanner_name or "").strip()
    color_mode = (color_mode or "").strip()
    page_size = (page_size or "").strip()

    if not scanner_name:
        raise ScannerConfigurationError(
            "Debe seleccionarse un escáner."
        )

    if dpi not in VALID_DPI:
        raise ScannerConfigurationError(
            f"Resolución no soportada: {dpi} DPI."
        )

    if color_mode not in VALID_COLOR_MODES:
        raise ScannerConfigurationError(
            f"Modo de color no soportado: '{color_mode}'."
        )

    if page_size not in VALID_PAGE_SIZES:
        raise ScannerConfigurationError(
            f"Tamaño de página no soportado: '{page_size}'."
        )

    scanner_session.update(
        scanner_id=scanner_id,
        scanner_name=scanner_name,
        dpi=dpi,
        color_mode=color_mode,
        page_size=page_size,
    )

    return scanner_session