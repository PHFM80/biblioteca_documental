#app\db\repositories\documento_pdf_repository.py
from typing import Optional

from app.db.database import get_connection
from app.models import DocumentoPDF


class DocumentoPDFRepository:
    """
    Maneja la persistencia de la información específica
    de documentos PDF.
    """

    def create(self, documento_pdf: DocumentoPDF) -> DocumentoPDF:
        """
        Crea la información asociada a un documento PDF.
        """

        query = """
            INSERT INTO documento_pdf (
                documento_id,
                cantidad_paginas,
                tiene_ocr,
                tiene_indexacion,
                texto_ocr_ruta,
                pdf_editable_ruta
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """

        try:
            with get_connection() as connection:
                connection.execute(
                    query,
                    (
                        documento_pdf.documento_id,
                        documento_pdf.cantidad_paginas,
                        int(documento_pdf.tiene_ocr),
                        int(documento_pdf.tiene_indexacion),
                        documento_pdf.texto_ocr_ruta,
                        documento_pdf.pdf_editable_ruta,
                    )
                )

            return documento_pdf

        except Exception as error:
            raise RuntimeError(
                f"Error creando información PDF: {error}"
            ) from error


    def get_by_document_id(
        self,
        documento_id: int
    ) -> Optional[DocumentoPDF]:
        """
        Obtiene la información PDF de un documento.
        """

        query = """
            SELECT *
            FROM documento_pdf
            WHERE documento_id = ?
        """

        try:
            with get_connection() as connection:
                row = connection.execute(
                    query,
                    (documento_id,)
                ).fetchone()

            if row is None:
                return None

            return self._row_to_model(row)

        except Exception as error:
            raise RuntimeError(
                f"Error obteniendo información PDF: {error}"
            ) from error


    def update(self, documento_pdf: DocumentoPDF) -> DocumentoPDF:
        """
        Actualiza información PDF existente.
        """

        query = """
            UPDATE documento_pdf
            SET
                cantidad_paginas = ?,
                tiene_ocr = ?,
                tiene_indexacion = ?,
                texto_ocr_ruta = ?,
                pdf_editable_ruta = ?
            WHERE documento_id = ?
        """

        try:
            with get_connection() as connection:
                connection.execute(
                    query,
                    (
                        documento_pdf.cantidad_paginas,
                        int(documento_pdf.tiene_ocr),
                        int(documento_pdf.tiene_indexacion),
                        documento_pdf.texto_ocr_ruta,
                        documento_pdf.pdf_editable_ruta,
                        documento_pdf.documento_id,
                    )
                )

            return documento_pdf

        except Exception as error:
            raise RuntimeError(
                f"Error actualizando información PDF: {error}"
            ) from error


    def delete(self, documento_id: int) -> bool:
        """
        Elimina la información PDF asociada.
        """

        query = """
            DELETE FROM documento_pdf
            WHERE documento_id = ?
        """

        try:
            with get_connection() as connection:
                cursor = connection.execute(
                    query,
                    (documento_id,)
                )

            return cursor.rowcount > 0

        except Exception as error:
            raise RuntimeError(
                f"Error eliminando información PDF: {error}"
            ) from error


    def set_ocr(
        self,
        documento_id: int,
        texto_ocr_ruta: str
    ) -> bool:
        """
        Marca el documento como procesado por OCR.
        """

        query = """
            UPDATE documento_pdf
            SET
                tiene_ocr = 1,
                texto_ocr_ruta = ?
            WHERE documento_id = ?
        """

        try:
            with get_connection() as connection:
                cursor = connection.execute(
                    query,
                    (
                        texto_ocr_ruta,
                        documento_id,
                    )
                )

            return cursor.rowcount > 0

        except Exception as error:
            raise RuntimeError(
                f"Error actualizando OCR: {error}"
            ) from error


    def set_indexacion(
        self,
        documento_id: int
    ) -> bool:
        """
        Marca el documento como indexado.
        """

        query = """
            UPDATE documento_pdf
            SET tiene_indexacion = 1
            WHERE documento_id = ?
        """

        try:
            with get_connection() as connection:
                cursor = connection.execute(
                    query,
                    (documento_id,)
                )

            return cursor.rowcount > 0

        except Exception as error:
            raise RuntimeError(
                f"Error actualizando indexación: {error}"
            ) from error


    @staticmethod
    def _row_to_model(row) -> DocumentoPDF:
        """
        Convierte una fila SQLite en un modelo DocumentoPDF.
        """

        return DocumentoPDF(
            documento_id=row["documento_id"],
            cantidad_paginas=row["cantidad_paginas"],
            tiene_ocr=bool(row["tiene_ocr"]),
            tiene_indexacion=bool(row["tiene_indexacion"]),
            texto_ocr_ruta=row["texto_ocr_ruta"],
            pdf_editable_ruta=row["pdf_editable_ruta"],
        )