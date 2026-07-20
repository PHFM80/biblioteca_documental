#app\services\document\DTO\save_document_data.py
from dataclasses import dataclass
from datetime import date


@dataclass
class SaveDocumentData:
    """
    Datos necesarios para ejecutar el proceso
    de guardado de un documento.
    """

    name: str
    chinese_name: str | None
    reception_date: date | None
    observations: str | None
    execute_ocr: bool
    execute_index: bool
    generate_docx: bool