import flet as ft


def scan_actions():

    return ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.ElevatedButton(
                "Vista previa",
                icon=ft.Icons.PREVIEW,
            ),

            ft.ElevatedButton(
                "Escanear página",
                icon=ft.Icons.SCANNER,
            ),
        ],
    )