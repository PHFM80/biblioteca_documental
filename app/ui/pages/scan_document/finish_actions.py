#app\ui\pages\scan_document\finish_actions.py
import flet as ft


def finish_actions(router, render):

    def continue_document(e):
        router.navigate("save_document")
        render()
    def cancel_document(e):
        router.navigate("dashboard")
        render()

    return ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.ElevatedButton("Guardar documento", icon=ft.Icons.SAVE, on_click=continue_document),
            ft.ElevatedButton("Cancelar", icon=ft.Icons.CANCEL, on_click=cancel_document),
        ])