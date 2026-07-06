import flet as ft
from app.core.init import initialize_app


def main(page: ft.Page):
    # Inicialización del sistema
    initialize_app()

    # Configuración básica de la UI
    page.title = "Biblioteca Documental"
    page.window_width = 1000
    page.window_height = 700

    page.add(ft.Text("Sistema iniciado correctamente"))


if __name__ == "__main__":
    ft.app(target=main)