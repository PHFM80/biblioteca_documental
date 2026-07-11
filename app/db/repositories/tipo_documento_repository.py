from typing import Optional

from app.db.database import get_connection
from app.models import TipoDocumento


class TipoDocumentoRepository:
    """
    Maneja la persistencia de tipos de documento.
    """

    def create(self, tipo: TipoDocumento) -> TipoDocumento:
        """
        Inserta un nuevo tipo de documento.
        """

        query = """
            INSERT INTO tipo_documento (tipo)
            VALUES (?)
        """

        try:
            with get_connection() as connection:
                cursor = connection.execute(
                    query,
                    (tipo.tipo,)
                )

                tipo.id = cursor.lastrowid

            return tipo

        except Exception as error:
            raise RuntimeError(
                f"Error creando tipo de documento: {error}"
            ) from error


    def get_by_id(self, tipo_id: int) -> Optional[TipoDocumento]:
        """
        Busca un tipo por su ID.
        """

        query = """
            SELECT id, tipo
            FROM tipo_documento
            WHERE id = ?
        """

        try:
            with get_connection() as connection:
                row = connection.execute(
                    query,
                    (tipo_id,)
                ).fetchone()

            if row is None:
                return None

            return TipoDocumento(
                id=row["id"],
                tipo=row["tipo"]
            )

        except Exception as error:
            raise RuntimeError(
                f"Error buscando tipo de documento: {error}"
            ) from error


    def get_by_name(self, nombre: str) -> Optional[TipoDocumento]:
        """
        Busca un tipo por nombre.
        """

        query = """
            SELECT id, tipo
            FROM tipo_documento
            WHERE tipo = ?
        """

        try:
            with get_connection() as connection:
                row = connection.execute(
                    query,
                    (nombre,)
                ).fetchone()

            if row is None:
                return None

            return TipoDocumento(
                id=row["id"],
                tipo=row["tipo"]
            )

        except Exception as error:
            raise RuntimeError(
                f"Error buscando tipo por nombre: {error}"
            ) from error


    def get_all(self) -> list[TipoDocumento]:
        """
        Devuelve todos los tipos registrados.
        """

        query = """
            SELECT id, tipo
            FROM tipo_documento
            ORDER BY tipo
        """

        try:
            with get_connection() as connection:
                rows = connection.execute(query).fetchall()

            return [
                TipoDocumento(
                    id=row["id"],
                    tipo=row["tipo"]
                )
                for row in rows
            ]

        except Exception as error:
            raise RuntimeError(
                f"Error listando tipos de documento: {error}"
            ) from error