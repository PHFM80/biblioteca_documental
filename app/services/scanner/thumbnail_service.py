#app\services\thumbnail_service.py
from pathlib import Path
from datetime import datetime

from PIL import Image

from app.core.config import SCANNER_TEMP_DIR


class ThumbnailService:
    """
    Servicio encargado de generar miniaturas
    de imágenes escaneadas.

    No conoce la UI.
    Solo transforma imágenes.
    """

    THUMBNAIL_SIZE = (180, 220)


    def create(
        self,
        image_path: str,
    ) -> str:
        """
        Genera una miniatura y devuelve
        la ruta creada.
        """

        source = Path(image_path)

        if not source.exists():
            raise FileNotFoundError(
                f"No existe la imagen: {source}"
            )


        thumbnail_dir = (
            SCANNER_TEMP_DIR /
            "thumbs"
        )

        thumbnail_dir.mkdir(
            parents=True,
            exist_ok=True,
        )


        filename = (
            f"thumb_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            ".png"
        )


        destination = (
            thumbnail_dir /
            filename
        )


        with Image.open(source) as image:

            image.thumbnail(
                self.THUMBNAIL_SIZE
            )

            image.save(
                destination,
                format="PNG",
            )


        return str(destination)


thumbnail_service = ThumbnailService()