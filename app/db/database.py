from pathlib import Path
import sqlite3

from app.core.config import DB_PATH


def get_connection() -> sqlite3.Connection:
    """
    Crea y devuelve una conexión SQLite.

    La conexión se configura para:
    - usar la base definida en config.py
    - activar claves foráneas
    - devolver filas como objetos tipo diccionario
    """

    try:
        # Seguridad extra por si se llama antes del arranque principal
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        connection = sqlite3.connect(
            DB_PATH,
            timeout=10
        )

        # Permite acceder por nombre de columna
        connection.row_factory = sqlite3.Row

        # Activa relaciones FK en SQLite
        connection.execute(
            "PRAGMA foreign_keys = ON;"
        )

        return connection

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Error al conectar con la base de datos: {error}"
        ) from error


def execute_query(query: str, params: tuple = ()) -> None:
    """
    Ejecuta una consulta simple de escritura.
    """

    try:
        with get_connection() as connection:
            connection.execute(query, params)
            connection.commit()

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Error ejecutando consulta: {error}"
        ) from error


def execute_script(script: str) -> None:
    """
    Ejecuta un script SQL completo.
    Utilizado principalmente para creación de esquema.
    """

    try:
        with get_connection() as connection:
            connection.executescript(script)
            connection.commit()

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Error ejecutando script SQL: {error}"
        ) from error

def check_connection() -> bool:
    """
    Verifica que la conexión con la base de datos sea válida.

    Returns:
        True si la conexión es correcta.

    Raises:
        RuntimeError si ocurre algún error.
    """

    try:
        with get_connection() as connection:
            connection.execute("SELECT 1;")

        return True

    except Exception as error:
        raise RuntimeError(
            f"No fue posible establecer conexión con la base de datos: {error}"
        ) from error