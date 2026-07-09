import flet as ft

from PIL import Image


class PreviewView:

    MIN_ZOOM = 10
    MAX_ZOOM = 300
    STEP = 10

    def __init__(self):

        self.image_path = None
        self.original_width = 0
        self.original_height = 0

        self.zoom = self.MIN_ZOOM

        self.zoom_text = ft.Text(
            f"{self.zoom} %",
            width=60,
            text_align=ft.TextAlign.CENTER,
        )

        self.image = ft.Image(src="")

        self.btn_zoom_out = ft.IconButton(
            icon=ft.Icons.REMOVE,
            disabled=True,
            on_click=self.zoom_out,
        )

        self.btn_zoom_in = ft.IconButton(
            icon=ft.Icons.ADD,
            disabled=True,
            on_click=self.zoom_in,
        )

        self.viewer = ft.Container(
            expand=True,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_400,
            ),
            border_radius=8,
            alignment=ft.Alignment(0.5, 0.5),
            content=ft.Column(
                scroll=ft.ScrollMode.ALWAYS,
                controls=[
                    ft.Row(
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[
                            self.image,
                        ],
                    )
                ],
            ),
        )

        self.container = ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.btn_zoom_out,
                        self.zoom_text,
                        self.btn_zoom_in,
                    ],
                ),
                ft.Container(
                    height=350,
                    content=self.viewer,
                ),
            ],
        )

        self.image.visible = False
        self.btn_zoom_in.disabled = True
        self.btn_zoom_out.disabled = True

    def update_image(self, image_path: str):

        self.image_path = image_path

        with Image.open(image_path) as img:
            self.original_width = img.width
            self.original_height = img.height

        self.zoom = self.MIN_ZOOM

        self.btn_zoom_in.disabled = False
        self.btn_zoom_out.disabled = False

        self._refresh_image()

    def zoom_in(self, e=None):

        if self.zoom >= self.MAX_ZOOM:
            return

        self.zoom += self.STEP
        self._refresh_image()

    def zoom_out(self, e=None):

        if self.zoom <= self.MIN_ZOOM:
            return

        self.zoom -= self.STEP
        self._refresh_image()

    def _refresh_image(self):
        factor = self.zoom / 100

        if self.image_path is None:
            self.image.src = ""
            self.image.visible = False
        else:
            self.image.src = str(self.image_path)
            self.image.visible = True

        self.image.width = int(self.original_width * factor)
        self.image.height = int(self.original_height * factor)
        self.zoom_text.value = f"{self.zoom} %"

        if self.container.page:
            self.container.update()

    def clear(self):
        self.image.src = ""
        self.image.visible = False

        self.viewer.content = ft.Container(
            alignment=ft.Alignment(0.5, 0.5),
            content=ft.Text(
                "Vista previa del documento",
                color=ft.Colors.GREY_600,
            ),
        )

        self.btn_zoom_in.disabled = True
        self.btn_zoom_out.disabled = True

        self.zoom = self.MIN_ZOOM
        self.zoom_text.value = f"{self.zoom} %"

        if self.container.page:
            self.container.update()


def preview():
    return PreviewView()