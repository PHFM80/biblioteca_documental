#app\ui\pages\save_document\form.py
import flet as ft


class SaveDocumentForm:
    """
    Formulario de información del documento.

    Únicamente administra los controles de la interfaz.
    No realiza validaciones ni guarda información.
    """

    def __init__(self):
        self.name = ft.TextField(
            label="Nombre del documento",
            autofocus=True,
            expand=True,
        )

        self.observations = ft.TextField(
            label="Observaciones",
            multiline=True,
            min_lines=3,
            max_lines=5,
            expand=True,
        )

        self.execute_ocr = ft.Checkbox(
            label="Ejecutar OCR",
            value=False,
        )

        self.execute_index = ft.Checkbox(
            label="Indexar documento",
            value=True,
        )

        self.generate_docx = ft.Checkbox(
            label="Generar DOCX",
            value=False,
        )

        self.container = ft.Column(
            spacing=15,
            controls=[
                self.name,
                self.observations,
                ft.Divider(),
                self.execute_ocr,
                self.execute_index,
                self.generate_docx,
            ],
        )

    def values(self) -> dict:
        """
        Devuelve los valores actuales del formulario.
        """

        return {
            "name": self.name.value.strip(),
            "observations": self.observations.value.strip(),
            "execute_ocr": self.execute_ocr.value,
            "execute_index": self.execute_index.value,
            "generate_docx": self.generate_docx.value,
        }


def form():
    return SaveDocumentForm()