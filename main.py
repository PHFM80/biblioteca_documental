import flet as ft

from app.core.init import initialize_app
from app.ui.router import Router
from app.ui.layout.sidebar import Sidebar

from app.ui.pages import dashboard, library, import_doc, search


def main(page: ft.Page):
    initialize_app()

    router = Router()

    content_area = ft.Container(expand=True)

    def render():

        if router.current_view == "dashboard":
            content_area.content = dashboard.view()

        elif router.current_view == "library":
            content_area.content = library.view()

        elif router.current_view == "import":
            content_area.content = import_doc.view()

        elif router.current_view == "search":
            content_area.content = search.view()

        page.update()

    sidebar = Sidebar(router, render)

    page.add(
        ft.Row(
            controls=[
                sidebar,
                content_area,
            ],
            expand=True
        )
    )

    render()


if __name__ == "__main__":
    ft.app(target=main)