#app\ui\pages\save_document\form.py
import flet as ft
from datetime import datetime

from app.services.document.dto.save_document_data import SaveDocumentData


class SaveDocumentForm:
    """
    Formulario de información del documento.

    Administra únicamente los controles de la interfaz
    y prepara los datos de entrada.
    """

    def __init__(self):
        self.name = ft.TextField(label="Nombre del documento", autofocus=True, expand=True)
        self.chinese_name = ft.TextField(label="Nombre en chino", expand=True)
        self.reception_date = ft.TextField(label="Fecha de recepción", hint_text="AAAA-MM-DD", expand=True)
        self.observations = ft.TextField(label="Observaciones", multiline=True, min_lines=3, max_lines=5, expand=True)
        self.execute_ocr = ft.Checkbox(label="Ejecutar OCR", value=False)
        self.execute_index = ft.Checkbox(label="Indexar documento", value=True)
        self.generate_docx = ft.Checkbox(label="Generar DOCX", value=False)

        self.container = ft.Column(
            spacing=15,
            controls=[
                self.name,
                self.chinese_name,
                self.reception_date,
                self.observations,
                ft.Divider(),
                self.execute_ocr,
                self.execute_index,
                self.generate_docx,
            ],
        )

    def _get_reception_date(self):
        value = self.reception_date.value.strip()

        if not value:
            return None

        return datetime.strptime(value, "%Y-%m-%d").date()

    def values(self) -> SaveDocumentData:
        return SaveDocumentData(
            name=self.name.value.strip(),
            chinese_name=self.chinese_name.value.strip() or None,
            reception_date=self._get_reception_date(),
            observations=self.observations.value.strip() or None,
            execute_ocr=bool(self.execute_ocr.value),
            execute_index=bool(self.execute_index.value),
            generate_docx=bool(self.generate_docx.value),
        )


def form():
    return SaveDocumentForm()