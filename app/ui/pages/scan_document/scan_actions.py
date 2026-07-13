#app\ui\pages\scan_document\scan_actions.py
import flet as ft


class ScanActions:
    """
    Contenedor de acciones del módulo de escaneo.
    """

    def __init__(self):

        self.scanning = False

        self.scan_button = ft.ElevatedButton(
            "Escanear página",
            icon=ft.Icons.SCANNER,
            on_click=self._scan_click,
        )

        self.preview_button = ft.ElevatedButton(
            "Vista previa",
            icon=ft.Icons.PREVIEW,
        )

        self.container = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                self.preview_button,
                self.scan_button,
            ],
        )

        self._on_scan = None


    def set_scan_handler(self, callback):

        self._on_scan = callback


    def _scan_click(self, e):

        if self.scanning:
            return

        self.set_scanning(True)

        if self._on_scan:
            self._on_scan(e)


    def set_scanning(self, value: bool):

        self.scanning = value

        self.scan_button.disabled = value

        if self.container.page:
            self.container.update()

def scan_actions():
    return ScanActions()