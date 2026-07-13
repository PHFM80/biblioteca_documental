#app\ui\pages\scan_document\pages_area.py
import flet as ft

from app.services.scanner.document_page import DocumentPage
from app.ui.components.document_thumbnail import DocumentThumbnail


class PagesArea:
    """
    Área visual donde se muestran las páginas
    escaneadas del documento.
    """

    def __init__(
        self,
        on_delete=None,
    ):

        self._pages: list[DocumentThumbnail] = []

        self.on_delete = on_delete

        self.container = ft.Row(
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
        )


    def add_page(self, page: DocumentPage):
        """
        Agrega una nueva página visual.
        """

        thumbnail = DocumentThumbnail(
            page=page,
            on_delete=self.on_delete,
        )

        self._pages.append(
            thumbnail
        )

        self.container.controls.append(
            thumbnail.card
        )

        self.update()

    def remove_page(
        self,
        page_number: int,
    ):
        """
        Elimina una página específica
        de la vista.
        """

        index = page_number - 1

        if index < 0:
            return

        if index >= len(self._pages):
            return


        self._pages.pop(index)

        self.container.controls.pop(index)

        self._renumber()

        self.update()

    def _renumber(self):
        """
        Actualiza la numeración visible
        luego de una eliminación.
        """

        for index, thumbnail in enumerate(
            self._pages,
            start=1,
        ):

            thumbnail.set_page_number(
                index
            )

    def clear(self):
        """
        Elimina todas las miniaturas.
        """

        self._pages.clear()

        self.container.controls.clear()

        self.update()

    def update(self):

        if self.container.page:
            self.container.update()

    def set_on_delete(self, callback):
        self.on_delete = callback

def pages_area(on_delete=None):

    return PagesArea(on_delete=on_delete)