#app\services\document\pdf_generator.py
from pathlib import Path

from PIL import Image

from app.services.scanner.document_page import DocumentPage


class PDFGenerator:
    """
    Genera archivos PDF a partir de páginas escaneadas.
    No conoce rutas de negocio ni flujo de guardado.
    Solo transforma imágenes en un archivo PDF.
    """

    def generate(self, pages: tuple[DocumentPage, ...], output_path: Path) -> Path:
        """
        Genera un PDF usando las imágenes de las páginas recibidas.
        """
        if not pages:
            raise ValueError("No hay páginas disponibles para generar el PDF.")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        images = []
        try:
            for page in pages:
                image_path = Path(page.image_path)
                if not image_path.exists():
                    raise FileNotFoundError(f"No existe la imagen: {image_path}")
                with Image.open(image_path) as image:
                    images.append(image.convert("RGB"))

            images[0].save(output_path, save_all=True, append_images=images[1:])
            return output_path

        except Exception as error:
            raise RuntimeError(f"Error generando PDF: {error}") from error
        finally:
            for image in images:
                image.close()