#main.py
import flet as ft

from app.core.init import initialize_app
from app.ui.router import Router
from app.ui.layout.sidebar import Sidebar
from app.db import initialize_database
from app.ui.pages import dashboard, library, import_doc, search, load_pdf, scan_document, save_document
from app.core.window import configure_window

async def main(page: ft.Page):
    await configure_window(page)
    initialize_app()
    initialize_database()

    router = Router()

    content_area = ft.Container(expand=True)

    def render():
        
        if router.current_view == "dashboard":
            content_area.content = dashboard.view()
        elif router.current_view == "library":
            content_area.content = library.view()
        elif router.current_view == "import":
            content_area.content = import_doc.view(router, render)
        elif router.current_view == "search":
            content_area.content = search.view()
        elif router.current_view == "load_pdf":
            content_area.content = load_pdf.view()
        elif router.current_view == "scan_document":
            content_area.content = scan_document.view(page, router, render)
        elif router.current_view == "save_document":
            content_area.content = save_document.view(page, router, render)
        else:
            content_area.content = dashboard.view()

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
    ft.run(main)