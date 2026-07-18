#app\db\repositories\documento_repository.py
from typing import Optional

from app.db.database import get_connection
from app.models import Documento


class DocumentoRepository:
    """
    Maneja la persistencia de documentos generales.
    """

    def create(self, documento: Documento) -> Documento:
        """
        Crea un nuevo documento.
        """

        query = """
            INSERT INTO documento (
                nombre,
                tipo_id,
                ruta,
                tamaño_bytes,
                fecha_creacion,
                fecha_modificacion,
                observaciones,
                hash_archivo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            with get_connection() as connection:
                cursor = connection.execute(
                    query,
                    (
                        documento.nombre,
                        documento.tipo_id,
                        documento.ruta,
                        documento.tamaño_bytes,
                        documento.fecha_creacion.isoformat(),
                        documento.fecha_modificacion.isoformat(),
                        documento.observaciones,
                        documento.hash_archivo,
                    )
                )

                documento.id = cursor.lastrowid

            return documento

        except Exception as error:
            raise RuntimeError(
                f"Error creando documento: {error}"
            ) from error


    def get_by_id(self, documento_id: int) -> Optional[Documento]:
        """
        Obtiene un documento por ID.
        """

        query = """
            SELECT *
            FROM documento
            WHERE id = ?
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
                f"Error obteniendo documento: {error}"
            ) from error


    def get_all(self) -> list[Documento]:
        """
        Lista todos los documentos.
        """

        query = """
            SELECT *
            FROM documento
            ORDER BY fecha_creacion DESC
        """

        try:
            with get_connection() as connection:
                rows = connection.execute(query).fetchall()

            return [
                self._row_to_model(row)
                for row in rows
            ]

        except Exception as error:
            raise RuntimeError(
                f"Error listando documentos: {error}"
            ) from error


    def update(self, documento: Documento) -> Documento:
        """
        Actualiza un documento existente.
        """

        if documento.id is None:
            raise ValueError(
                "No se puede actualizar un documento sin ID"
            )

        query = """
            UPDATE documento
            SET
                nombre = ?,
                tipo_id = ?,
                ruta = ?,
                tamaño_bytes = ?,
                fecha_modificacion = ?,
                observaciones = ?,
                hash_archivo = ?
            WHERE id = ?
        """

        try:
            with get_connection() as connection:
                connection.execute(
                    query,
                    (
                        documento.nombre,
                        documento.tipo_id,
                        documento.ruta,
                        documento.tamaño_bytes,
                        documento.fecha_modificacion.isoformat(),
                        documento.observaciones,
                        documento.hash_archivo,
                        documento.id,
                    )
                )

            return documento

        except Exception as error:
            raise RuntimeError(
                f"Error actualizando documento: {error}"
            ) from error


    def delete(self, documento_id: int) -> bool:
        """
        Elimina un documento.
        """

        query = """
            DELETE FROM documento
            WHERE id = ?
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
                f"Error eliminando documento: {error}"
            ) from error


    def exists_by_hash(self, hash_archivo: str) -> bool:
        """
        Permite detectar documentos duplicados.
        """

        query = """
            SELECT 1
            FROM documento
            WHERE hash_archivo = ?
            LIMIT 1
        """

        try:
            with get_connection() as connection:
                result = connection.execute(
                    query,
                    (hash_archivo,)
                ).fetchone()

            return result is not None

        except Exception as error:
            raise RuntimeError(
                f"Error verificando hash del documento: {error}"
            ) from error


    @staticmethod
    def _row_to_model(row) -> Documento:
        """
        Convierte una fila SQLite en un modelo Documento.
        """

        from datetime import datetime

        return Documento(
            id=row["id"],
            nombre=row["nombre"],
            tipo_id=row["tipo_id"],
            ruta=row["ruta"],
            tamaño_bytes=row["tamaño_bytes"],
            fecha_creacion=datetime.fromisoformat(
                row["fecha_creacion"]
            ),
            fecha_modificacion=datetime.fromisoformat(
                row["fecha_modificacion"]
            ),
            observaciones=row["observaciones"],
            hash_archivo=row["hash_archivo"],
        )