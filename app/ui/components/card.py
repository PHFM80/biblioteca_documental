#app\ui\components\card.py
import flet as ft


def AppCard(
    icon: str,
    title: str,
    subtitle: str,
    on_click=None,
    width: int = 320,
    height: int = 220,
):
    return ft.Card(
        elevation=3,
        content=ft.Container(
            width=width,
            height=height,
            padding=20,
            border_radius=12,
            ink=True,
            on_click=on_click,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                controls=[
                    ft.Text(icon, size=48),
                    ft.Text(
                        title,
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        subtitle,
                        size=14,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        ),
    )