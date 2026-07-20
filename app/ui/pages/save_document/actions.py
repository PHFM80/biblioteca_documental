#app\ui\pages\save_document\actions.py
import flet as ft


class SaveDocumentActions:
    """
    Expone las acciones disponibles en la vista.

    No contiene lógica de negocio.
    Solo asigna eventos definidos por la vista.
    """

    def __init__(self):
        self.save_button = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE)
        self.cancel_button = ft.ElevatedButton("Cancelar", icon=ft.Icons.CANCEL)

        self.container = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                self.save_button,
                self.cancel_button,
            ],
        )

    def set_save_handler(self, handler):
        self.save_button.on_click = handler

    def set_cancel_handler(self, handler):
        self.cancel_button.on_click = handler


def actions():
    return SaveDocumentActions()