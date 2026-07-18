#app/models\documento.py
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Documento:
    id: int | None
    nombre: str
    tipo_id: int
    ruta: str
    tamaño_bytes: int
    fecha_creacion: datetime
    fecha_modificacion: datetime
    observaciones: str | None = None
    hash_archivo: str | None = None
