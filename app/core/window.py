import flet as ft


async def configure_window(page: ft.Page):

    # Información de la aplicación
    page.title = "Biblioteca Documental Inteligente"

    # Tema
    page.theme_mode = ft.ThemeMode.LIGHT

    # Layout
    page.padding = 0
    page.spacing = 0

    # Ventana
    page.window.width = 1400
    page.window.height = 900

    page.window.min_width = 1100
    page.window.min_height = 700

    await page.window.center()

    # Comportamiento
    page.window.maximizable = True
    page.window.minimizable = True
    page.window.resizable = True

    # Opcional
    page.window.prevent_close = False