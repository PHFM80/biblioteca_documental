import flet as ft


def scan_actions(
    on_preview=None,
    on_scan=None,
):

    return ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        controls=[

            ft.ElevatedButton(
                "Vista previa",
                icon=ft.Icons.PREVIEW,
                on_click=on_preview,
            ),

            ft.ElevatedButton(
                "Escanear página",
                icon=ft.Icons.SCANNER,
                on_click=on_scan,
            ),

        ],
    )