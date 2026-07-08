import flet as ft


def finish_actions():

    return ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.ElevatedButton(
                "Guardar documento",
                icon=ft.Icons.SAVE,
            ),

            ft.ElevatedButton(
                "Cancelar",
                icon=ft.Icons.CANCEL,
            ),
        ],
    )