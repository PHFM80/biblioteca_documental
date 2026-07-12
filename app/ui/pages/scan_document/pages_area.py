#app\ui\pages\scan_document\pages_area.py
import flet as ft

from app.services.scanner.document_page import DocumentPage


class PagesArea:
    """
    Componente visual encargado de mostrar
    las páginas escaneadas.

    No conoce el escáner ni la sesión.
    Solo representa páginas.
    """

    def __init__(self):

        self.container = ft.Row(
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
        )


    def add_page(
        self,
        page: DocumentPage,
    ):
        """
        Agrega una miniatura visual.
        """

        thumbnail = ft.Container(
            width=120,
            height=150,
            border_radius=8,
            bgcolor=ft.Colors.GREY_200,
            padding=5,

            content=ft.Image(
                src=page.thumbnail_path,
                fit="contain",
            ),
        )

        self.container.controls.append(
            thumbnail
        )

        self.update()


    def remove_last_page(self):
        """
        Elimina la última miniatura.
        """

        if not self.container.controls:
            return

        self.container.controls.pop()

        self.update()


    def clear(self):
        """
        Limpia todas las miniaturas.
        """

        self.container.controls.clear()

        self.update()


    def update(self):

        if self.container.page:
            self.container.update()



def pages_area():

    return PagesArea()