#app\ui\pages\save_document\actions.py
import flet as ft


class SaveDocumentActions:
    """
    Acciones disponibles para el guardado del documento.

    No contiene lógica de negocio.
    Solamente expone los botones para que la vista
    asigne sus eventos.
    """

    def __init__(self):
        self.save_button = ft.ElevatedButton(
            "Guardar",
            icon=ft.Icons.SAVE,
        )

        self.cancel_button = ft.ElevatedButton(
            "Cancelar",
            icon=ft.Icons.CANCEL,
        )

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