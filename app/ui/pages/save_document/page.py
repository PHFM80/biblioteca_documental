#app\ui\pages\save_document\page.py
import flet as ft

from app.ui.pages.save_document.preview import preview
from app.ui.pages.save_document.form import form
from app.ui.pages.save_document.actions import actions
from app.ui.pages.save_document.handlers import save_document


def section(title, content):
    return ft.Container(
        padding=15,
        border_radius=10,
        bgcolor=ft.Colors.GREY_100,
        content=ft.Column(
            controls=[
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                content],
        )
    )


def view(page, router, render):

    preview_view = preview()
    form_view = form()
    actions_view = actions()
    actions_view.set_save_handler(lambda e: save_document(form_view, page, router, render))

    return ft.Container(
        expand=True,
        padding=30,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=15,
            controls=[
                ft.Text("Guardar documento", size=30, weight=ft.FontWeight.BOLD),
                section("Vista previa", preview_view),
                section("Información del documento", form_view.container),
                section("Acciones", actions_view.container)],
        )
    )
