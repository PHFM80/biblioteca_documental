#app\ui\pages\save_document\preview.py
import flet as ft

from app.services.scanner.document_session import document_session
from app.ui.components.document_thumbnail import DocumentThumbnail


class DocumentPreview:

    def __init__(self):
        self.row = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=10)
        self.container = ft.Container(content=self.row)
        self.refresh()

    def refresh(self):
        self.row.controls.clear()

        pages = document_session.get_pages()

        if not pages:
            self.row.controls.append(ft.Text("No hay páginas escaneadas.", italic=True))
            return

        for page in pages:
            thumbnail = DocumentThumbnail(page, show_actions=False)
            self.row.controls.append(thumbnail.card)

def preview():
    return DocumentPreview().container