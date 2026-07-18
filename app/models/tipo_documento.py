#app\models\tipo_documento.py
from dataclasses import dataclass

@dataclass
class TipoDocumento:
    id: int | None
    tipo: str
