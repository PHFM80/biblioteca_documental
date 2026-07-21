#app\ui\components\notification.py
import flet as ft


def show_message(page: ft.Page, message: str, error: bool = False):
    snackbar = ft.SnackBar(
        content=ft.Text(message),
        duration=5000
    )

    page.overlay.append(snackbar)
    snackbar.open = True
    page.update()