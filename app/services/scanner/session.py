from dataclasses import dataclass, field


DEFAULT_SCANNER = "Detectando automáticamente"
DEFAULT_DPI = 300
DEFAULT_COLOR_MODE = "Escala de grises"
DEFAULT_PAGE_SIZE = "Automático"


@dataclass
class ScannerSessionConfig:
    scanner_name: str = DEFAULT_SCANNER
    dpi: int = DEFAULT_DPI
    color_mode: str = DEFAULT_COLOR_MODE
    page_size: str = DEFAULT_PAGE_SIZE

    def update(
        self,
        scanner_name=None,
        dpi=None,
        color_mode=None,
        page_size=None,
    ):
        if scanner_name is not None:
            self.scanner_name = scanner_name

        if dpi is not None and dpi in [150, 300, 600]:
            self.dpi = dpi

        if color_mode is not None:
            self.color_mode = color_mode

        if page_size is not None:
            self.page_size = page_size

    def reset(self):
        self.scanner_name = DEFAULT_SCANNER
        self.dpi = DEFAULT_DPI
        self.color_mode = DEFAULT_COLOR_MODE
        self.page_size = DEFAULT_PAGE_SIZE

    def summary(self):
        return {
            "scanner": self.scanner_name,
            "dpi": self.dpi,
            "color": self.color_mode,
            "page_size": self.page_size,
        }


# Sesión activa mientras la aplicación está abierta
scanner_session = ScannerSessionConfig()