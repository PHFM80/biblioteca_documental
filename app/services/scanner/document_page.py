#app\services\scanner\document_page.py
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DocumentPage:
    """
    Representa una página escaneada durante
    la sesión temporal del documento.

    image_path:
        Imagen original para procesamiento,
        OCR y guardado definitivo.

    thumbnail_path:
        Imagen reducida utilizada exclusivamente
        por la interfaz.
    """

    page_number: int
    image_path: str
    thumbnail_path: str
