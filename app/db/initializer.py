from app.db.database import check_connection
from app.db.schema import init_database



def initialize_database() -> None:
    """
    Inicializa completamente la base de datos.

    Responsabilidades:
        - Crear la base de datos si no existe.
        - Crear todas las tablas.
        - Insertar datos iniciales.
        - Ejecutar futuras migraciones.

    Este método puede ejecutarse múltiples veces sin afectar
    la información existente.
    """

    init_database()


def initialize_database() -> None:
    """
    Inicializa completamente la base de datos.
    """

    check_connection()
    init_database()