import flet as ft


def preview():

    return ft.Container(
        height=350,
        alignment=ft.Alignment(0, 0),
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(
            1,
            ft.Colors.GREY_400,
        ),
        border_radius=8,
        content=ft.Text(
            "Vista previa del documento",
            color=ft.Colors.GREY_600,
        ),
    )