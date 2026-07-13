#app\services\image_processing\operations\deskew.py
from pathlib import Path

import cv2
import numpy as np

from PIL import Image, ImageOps, UnidentifiedImageError

from app.services.image_processing.exceptions import ImageProcessingError


class DeskewOperation:
    """
    Corrige inclinación pequeña de documentos escaneados.
    """
    def __init__(self, max_angle: float = 5.0,):

        if max_angle <= 0:
            raise ValueError(
                "max_angle debe ser mayor a 0"
            )

        self.max_angle = max_angle

    def apply(
        self,
        image_path: str | Path,
    ) -> str:

        source = Path(
            image_path
        )

        self._validate_source(
            source
        )

        try:
            with Image.open(source) as image:

                corrected = self._deskew(
                    image
                )

                output = self._build_output_path(
                    source
                )

                corrected.save(
                    output,
                    format="PNG",
                )
                return str(output)

        except UnidentifiedImageError as exc:

            raise ImageProcessingError(
                f"Archivo de imagen inválido: {source}"
            ) from exc


        except Exception as exc:
            import traceback
            traceback.print_exc()

            raise ImageProcessingError(
                f"Error corrigiendo inclinación: {exc}"
            ) from exc

    def _deskew(
        self,
        image: Image.Image,
    ) -> Image.Image:

        gray = ImageOps.grayscale(
            image
        )

        angle = self._detect_angle(
            gray
        )

        if abs(angle) < 0.1:
            return image.copy()

        return image.rotate(
            angle,
            expand=True,
            fillcolor="white",
        )

    def _detect_angle(self, image: Image.Image) -> float:
        """
        Detecta inclinación usando líneas del contenido.
        Evita tomar el borde completo de la hoja.
        """
        img = np.array(
            image
        )

        # reducir tamaño para acelerar detección
        height, width = img.shape[:2]

        scale = 1.0

        if width > 1500:
            scale = 1500 / width

            img = cv2.resize(
                img,
                None,
                fx=scale,
                fy=scale,
            )

        # mejorar contraste
        blur = cv2.GaussianBlur(
            img,
            (5, 5),
            0,
        )

        edges = cv2.Canny(
            blur,
            50,
            150,
            apertureSize=3,
        )

        lines = cv2.HoughLinesP(
            edges,
            1,
            np.pi / 180,
            threshold=100,
            minLineLength=100,
            maxLineGap=10,
        )

        if lines is None:
             return 0.0

        angles = []

        for line in lines:
            x1=line[0]
            y1=line[1]
            x2=line[2]
            y2=line[3]

            angle = np.degrees(
                np.arctan2(
                    y2 - y1,
                    x2 - x1,
                )
            )

            # solo líneas horizontales
            if -45 < angle < 45:

                angles.append(
                    angle
                )

        median_angle = float(
            np.median(
                angles
            )
        )

        if abs(median_angle) > self.max_angle:
            return 0.0
        
        return median_angle


    def _build_output_path(
        self,
        source: Path,
    ) -> Path:

        return source.with_name(
            f"{source.stem}_deskew{source.suffix}"
        )

    def _validate_source(
        self,
        source: Path,
    ) -> None:

        if not source.exists():
            raise ImageProcessingError(
                f"No existe la imagen: {source}"
            )
        if not source.is_file():
            raise ImageProcessingError(
                f"La ruta no es un archivo: {source}"
            )