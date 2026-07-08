import flet as ft


def pages_area():

    return ft.Row(
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
        controls=[
            ft.Container(
                width=120,
                height=150,
                bgcolor=ft.Colors.GREY_200,
                border_radius=8,
                alignment=ft.Alignment(0, 0),
                content=ft.Text(
                    "Próxima\npágina\n aquí",
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.GREY_700,
                ),
            )
        ],
    )