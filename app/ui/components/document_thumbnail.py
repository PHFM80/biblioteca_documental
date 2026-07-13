#app\ui\components\document_thumbnail.py
import flet as ft

from app.services.scanner.document_page import DocumentPage


class DocumentThumbnail:
    """
    Componente visual para representar
    una página escaneada.
    """

    def __init__(
        self,
        page: DocumentPage,
        on_delete=None,
    ):

        self.page = page
        self.on_delete = on_delete

        self.page_label = ft.Text(
            self._get_title(),
            size=12,
            weight=ft.FontWeight.BOLD,
        )

        self.image = ft.Image(
            src=page.thumbnail_path,
            fit="contain",
            width=110,
            height=140,
        )

        self.delete_button = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_size=18,
            tooltip="Eliminar página",
            on_click=self._delete,
        )

        self.card = ft.Card(
            elevation=2,
            content=ft.Container(
                width=140,
                padding=5,

                content=ft.Column(
                    spacing=5,

                    controls=[

                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                self.page_label,
                                self.delete_button,
                            ],
                        ),

                        self.image,

                    ],
                ),
            ),
        )


    def _get_title(self):

        return f"Pág. {self.page.page_number}"


    def _delete(self, e):

        if self.on_delete:

            self.on_delete(
                self.page.page_number
            )


    def set_page_number(
        self,
        number: int,
    ):
        """
        Actualiza la numeración visible.
        """

        self.page.page_number = number

        self.page_label.value = (
            f"Pág. {number}"
        )

        self.update()


    def update_thumbnail(
        self,
        path: str,
    ):
        """
        Actualiza la imagen mostrada.
        """

        self.page.thumbnail_path = path

        self.image.src = path

        self.update()


    def update(self):

        if self.card.page:
            self.card.update()