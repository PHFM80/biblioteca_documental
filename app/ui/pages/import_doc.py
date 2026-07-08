import flet as ft

import app.ui.components.card


def view(router, render):

    
    def navigate(destination):
        router.navigate(destination)
        render()

    return ft.Container(
        expand=True,
        padding=40,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Incorporar documento",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Elegí cómo querés agregar un documento a la biblioteca.",
                    size=16,
                    color=ft.Colors.GREY_700,
                ),
                ft.Container(height=40),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=30,
                    controls=[
                        app.ui.components.card.AppCard(
                            icon="📄",
                            title="Cargar PDF",
                            subtitle="Seleccionar un PDF existente.",
                            on_click=lambda e: navigate("load_pdf"),
                        ),
                        app.ui.components.card.AppCard(
                            icon="🖨️",
                            title="Escanear documento",
                            subtitle="Crear un PDF desde un escáner.",
                            on_click=lambda e: navigate("scan_document"),
                        ),
                    ],
                ),
            ],
        ),
    )