import flet as ft

def Sidebar(router, on_change):

    def go(view):
        if view == "back":
            router.back()
        else:
            router.navigate(view)

        on_change()

    return ft.Container(
        width=220,
        bgcolor=ft.Colors.BLUE_GREY_900,
        padding=10,
        content=ft.Column(
            controls=[
                ft.Text("Biblioteca", color=ft.Colors.WHITE, size=20),
                ft.TextButton("← Volver", on_click=lambda e: go("back")),

                ft.Divider(),

                ft.TextButton("Dashboard", on_click=lambda e: go("dashboard")),
                ft.TextButton("Biblioteca", on_click=lambda e: go("library")),
                ft.TextButton("Importar", on_click=lambda e: go("import")),
                ft.TextButton("Búsqueda", on_click=lambda e: go("search")),
            ],
        ),
    )