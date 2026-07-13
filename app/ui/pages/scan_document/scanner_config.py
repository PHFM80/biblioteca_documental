#app\ui\pages\scan_document\scanner_config.py
import flet as ft

from app.services.scanner.session import scanner_session
from app.services.scanner.apply_configuration import apply_configuration
from app.services.scanner.exceptions import ScannerConfigurationError


def scanner_config(scanner_options=None):
    scanner_options = scanner_options or []
    scanner_map = {scanner.id: scanner.name for scanner in scanner_options}

    scanner_text = ft.Text()
    dpi_text = ft.Text()
    color_text = ft.Text()
    size_text = ft.Text()

    scanner_dropdown = ft.Dropdown(
        label="Escáner",
        width=300,
        options=[
            ft.dropdown.Option(key=scanner.id, text=scanner.name)
            for scanner in scanner_options
        ],
        value=scanner_session.scanner_id,
    )

    dpi_dropdown = ft.Dropdown(
        label="Resolución",
        width=180,
        value=f"{scanner_session.dpi} DPI",
        options=[
            ft.dropdown.Option("150 DPI"),
            ft.dropdown.Option("300 DPI"),
            ft.dropdown.Option("600 DPI"),
        ],
    )

    color_dropdown = ft.Dropdown(
        label="Color",
        width=180,
        value=scanner_session.color_mode,
        options=[
            ft.dropdown.Option("Blanco y negro"),
            ft.dropdown.Option("Escala de grises"),
            ft.dropdown.Option("Color"),
        ],
    )

    size_dropdown = ft.Dropdown(
        label="Tamaño",
        width=180,
        value=scanner_session.page_size,
        options=[
            ft.dropdown.Option("Automático"),
            ft.dropdown.Option("A4"),
            ft.dropdown.Option("Carta"),
            ft.dropdown.Option("Oficio"),
            ft.dropdown.Option("Sobre"),
        ],
    )

    def update_summary():
        scanner_text.value = (
            f"Escáner: {scanner_session.scanner_name}"
        )
        dpi_text.value = (
            f"Resolución: {scanner_session.dpi} DPI"
        )
        color_text.value = (
            f"Color: {scanner_session.color_mode}"
        )
        size_text.value = (
            f"Tamaño: {scanner_session.page_size}"
        )

    def on_apply(e):
        try:
            scanner_id = scanner_dropdown.value

            apply_configuration(
                scanner_id=scanner_id,
                scanner_name=scanner_map.get(
                    scanner_id,
                    "Detectando automáticamente"
                ),
                dpi=int(
                    dpi_dropdown.value.replace(" DPI", "")
                ),
                color_mode=color_dropdown.value,
                page_size=size_dropdown.value,
            )

            update_summary()

            e.page.update()

            print("Configuración aplicada:")
            print(scanner_session.summary())

        except ScannerConfigurationError as ex:
            print(f"Error configuración: {ex}")

    update_summary()

    return ft.Column(
        controls=[
            ft.Container(
                padding=15,
                bgcolor=ft.Colors.WHITE,
                border_radius=8,
                content=ft.Column(
                    spacing=5,
                    controls=[
                        ft.Text(
                            "Configuración actual",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                        scanner_text,
                        dpi_text,
                        color_text,
                        size_text,
                    ],
                ),
            ),

            ft.ExpansionTile(
                title=ft.Text("Cambiar configuración"),
                leading=ft.Icon(ft.Icons.SETTINGS),
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            scanner_dropdown
                        ],
                    ),

                    ft.Container(height=20),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            dpi_dropdown,
                            color_dropdown,
                            size_dropdown,
                        ],
                    ),

                    ft.Container(height=15),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.ElevatedButton(
                                "Aplicar configuración",
                                icon=ft.Icons.CHECK,
                                on_click=on_apply,
                            )
                        ],
                    ),

                    ft.Container(height=20),
                ],
            ),
        ]
    )