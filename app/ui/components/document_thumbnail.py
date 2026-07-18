#app\ui\components\document_thumbnail.py
import flet as ft

from app.services.scanner.document_page import DocumentPage


class DocumentThumbnail:
    """
    Componente visual para representar
    una página escaneada.
    """

    def __init__(self, page: DocumentPage, on_delete=None, show_actions=True):
        self.page = page
        self.on_delete = on_delete
        self.show_actions = show_actions

        self.page_label = ft.Text(self._get_title(), size=12, weight=ft.FontWeight.BOLD)

        self.image = ft.Image(src=page.thumbnail_path, fit="contain", width=110, height=140)

        self.card = self._build_card()

    def _build_card(self):
        header_controls = [self.page_label]

        if self.show_actions:
            header_controls.append(self._delete_button())

        return ft.Card(
            elevation=2,
            content=ft.Container(
                width=140,
                padding=5,
                content=ft.Column(
                    spacing=5,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=header_controls,
                        ),
                        self.image,
                    ],
                ),
            ),
        )

    def _delete_button(self):
        return ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_size=18,
            tooltip="Eliminar página",
            on_click=self._delete,
        )

    def _get_title(self):
        return f"Pág. {self.page.page_number}"

    def _delete(self, e):
        if self.on_delete:
            self.on_delete(self.page.page_number)

    def set_page_number(self, number: int):
        self.page.page_number = number
        self.page_label.value = f"Pág. {number}"
        self.update()

    def update_thumbnail(self, path: str):
        self.page.thumbnail_path = path
        self.image.src = path
        self.update()

    def update(self):
        if self.card.page:
            self.card.update()