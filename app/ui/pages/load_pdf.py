import flet as ft

def view():
    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0.5, 0.5),
        content=ft.Text(
            "Cargar PDF",
            size=30,
            weight=ft.FontWeight.BOLD,
        ),
    )