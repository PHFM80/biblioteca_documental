#app\models\documento_pdf.py
from dataclasses import dataclass
from datetime import date

@dataclass
class DocumentoPDF:
    documento_id: int
    cantidad_paginas: int
    tiene_ocr: bool = False
    nombre_chino: str | None = None
    fecha_recepcion: date | None = None
    tiene_indexacion: bool = False
    texto_ocr_ruta: str | None = None
    pdf_editable_ruta: str | None = None