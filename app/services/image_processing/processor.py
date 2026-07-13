#app\services\imageprocessing\processor.py
from pathlib import Path

from app.services.image_processing import settings
from app.services.image_processing.exceptions import (ImageProcessingError, ImageProcessingExecutionError)
from app.services.image_processing.operations.cleanup import CleanupOperation
from app.services.image_processing.operations.deskew import DeskewOperation


class ImageProcessingService:

    def __init__(self):
        self.operations = self._load_operations()

    def process(
        self,
        image_path: str | Path,
    ) -> str:
        """
        Ejecuta todas las operaciones configuradas.
        Returns:
            Ruta de la imagen procesada.
        """

        current_path = Path(image_path)

        self._validate_image(current_path)

        try:
            for operation in self.operations:
                current_path = operation.apply(current_path)
            return str(current_path)

        except ImageProcessingError:
            raise

        except Exception as exc:
            raise ImageProcessingExecutionError(
                f"Error en pipeline de imagen: {exc}"
            ) from exc

    def _load_operations(self):
        """
        Construye el pipeline según configuración.
        """

        operations = []


        if settings.AUTO_DESKEW:
            operations.append(DeskewOperation())

        return operations

    def _validate_image(
        self,
        image_path: Path,
    ):
        """
        Valida imagen de entrada.
        """

        if not image_path.exists():
            raise ImageProcessingError(
                f"No existe la imagen: {image_path}"
            )

        if not image_path.is_file():
            raise ImageProcessingError(
                f"La ruta no corresponde a un archivo: {image_path}"
            )