from dataclasses import dataclass

@dataclass
class DocumentoPDF:
    documento_id: int
    cantidad_paginas: int
    tiene_ocr: bool = False
    tiene_indexacion: bool = False
    texto_ocr_ruta: str | None = None
    pdf_editable_ruta: str | None = None