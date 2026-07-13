#app\services\image_processing\operations\cleanup.py
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError

from app.services.image_processing.exceptions import ImageProcessingError


class CleanupOperation:
    """
    Elimina bordes sombreados de documentos escaneados.
    Detecta sombras, gradientes y áreas uniformes cerca de los bordes.
    """

    def __init__(
        self,
        threshold: int = 220,
        border_margin: int = 50,
        gradient_threshold: int = 30,
    ):
        if not 0 <= threshold <= 255:
            raise ValueError("threshold debe estar entre 0 y 255")

        if border_margin < 0:
            raise ValueError("border_margin debe ser mayor o igual a 0")

        self.threshold = threshold
        self.border_margin = border_margin
        self.gradient_threshold = gradient_threshold

    def apply(self, image_path: str | Path) -> str:
        source = Path(image_path)
        self._validate_source(source)

        try:
            with Image.open(source) as image:
                cleaned = self._cleanup(image)
                output = self._build_output_path(source)

                cleaned.save(output, format="PNG")
                return str(output)

        except UnidentifiedImageError as exc:
            raise ImageProcessingError(
                f"Archivo de imagen inválido: {source}"
            ) from exc

        except Exception as exc:
            raise ImageProcessingError(
                f"Error limpiando bordes: {exc}"
            ) from exc

    def _cleanup(self, image: Image.Image) -> Image.Image:
        gray = ImageOps.grayscale(image)
        img_array = np.array(gray)

        shadow_mask = self._detect_border_shadows(img_array)

        result = np.array(image)
        result[shadow_mask] = 255

        return Image.fromarray(result)

    def _detect_border_shadows(self, img_array: np.ndarray) -> np.ndarray:
        height, width = img_array.shape

        # Máscara final combinando múltiples técnicas
        final_mask = np.zeros((height, width), dtype=bool)

        # Técnica 1: Detectar áreas oscuras conectadas a los bordes
        dark_mask = self._detect_dark_borders(img_array)
        final_mask |= dark_mask

        # Técnica 2: Detectar gradientes suaves desde los bordes
        gradient_mask = self._detect_gradients(img_array)
        final_mask |= gradient_mask

        # Técnica 3: Detectar áreas uniformes (baja varianza) cerca de bordes
        uniform_mask = self._detect_uniform_areas(img_array)
        final_mask |= uniform_mask

        return final_mask

    def _detect_dark_borders(self, img_array: np.ndarray) -> np.ndarray:
        """Detecta áreas oscuras conectadas a los bordes"""
        height, width = img_array.shape

        _, binary = cv2.threshold(
            img_array,
            self.threshold,
            255,
            cv2.THRESH_BINARY_INV,
        )

        contours, _ = cv2.findContours(
            binary,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        shadow_mask = np.zeros_like(binary, dtype=np.uint8)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            touches_border = (
                x <= 2 or 
                y <= 2 or 
                (x + w) >= (width - 2) or 
                (y + h) >= (height - 2)
            )

            if touches_border and cv2.contourArea(contour) > 100:
                cv2.drawContours(
                    shadow_mask, 
                    [contour], 
                    -1, 
                    255, 
                    thickness=cv2.FILLED
                )

        return shadow_mask == 255

    def _detect_gradients(self, img_array: np.ndarray) -> np.ndarray:
        """Detecta gradientes suaves desde los bordes hacia el centro"""
        height, width = img_array.shape
        
        # Calcular gradiente en dirección X e Y
        grad_x = cv2.Sobel(img_array, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(img_array, cv2.CV_64F, 0, 1, ksize=3)
        
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Normalizar
        magnitude = (magnitude / magnitude.max() * 255).astype(np.uint8)
        
        # Detectar áreas con bajo gradiente (uniformes) cerca de los bordes
        low_gradient = magnitude < self.gradient_threshold
        
        # Crear máscara de bordes
        border_mask = np.zeros((height, width), dtype=bool)
        border_mask[:self.border_margin, :] = True  # Arriba
        border_mask[-self.border_margin:, :] = True  # Abajo
        border_mask[:, :self.border_margin] = True  # Izquierda
        border_mask[:, -self.border_margin:] = True  # Derecha
        
        # Combinar: bajo gradiente Y cerca del borde
        gradient_border_mask = low_gradient & border_mask
        
        # Solo mantener si es más oscuro que el centro
        center_region = img_array[
            self.border_margin:-self.border_margin,
            self.border_margin:-self.border_margin
        ]
        center_mean = np.mean(center_region)
        
        # Si el borde es más oscuro que el centro, es sombra
        dark_border = img_array < (center_mean - 20)
        gradient_border_mask &= dark_border
        
        return gradient_border_mask

    def _detect_uniform_areas(self, img_array: np.ndarray) -> np.ndarray:
        """Detecta áreas uniformes (baja varianza) cerca de los bordes"""
        height, width = img_array.shape
        
        # Calcular varianza local usando filtro
        kernel_size = 15
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size**2)
        
        mean = cv2.filter2D(img_array.astype(np.float32), -1, kernel)
        mean_sq = cv2.filter2D(img_array.astype(np.float32)**2, -1, kernel)
        
        variance = mean_sq - mean**2
        
        # Áreas con muy baja varianza (uniformes)
        uniform = variance < 100
        
        # Solo cerca de los bordes
        border_mask = np.zeros((height, width), dtype=bool)
        border_mask[:self.border_margin, :] = True
        border_mask[-self.border_margin:, :] = True
        border_mask[:, :self.border_margin] = True
        border_mask[:, -self.border_margin:] = True
        
        uniform_border = uniform & border_mask
        
        # Solo si es más oscuro que el promedio
        overall_mean = np.mean(img_array)
        dark_uniform = img_array < (overall_mean - 15)
        uniform_border &= dark_uniform
        
        return uniform_border

    def _build_output_path(self, source: Path) -> Path:
        return source.with_name(f"{source.stem}_cleanup{source.suffix}")

    def _validate_source(self, source: Path) -> None:
        if not source.exists():
            raise ImageProcessingError(f"No existe la imagen: {source}")

        if not source.is_file():
            raise ImageProcessingError(f"La ruta no corresponde a un archivo: {source}")