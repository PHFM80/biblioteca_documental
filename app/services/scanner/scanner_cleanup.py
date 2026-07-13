#app\services\scanner\scanner_cleanup.py
from dataclasses import dataclass, field
from pathlib import Path

from app.core.config import SCANNER_TEMP_DIR

from app.services.scanner.document_session import document_session
from app.services.scanner.session import scanner_session


@dataclass(slots=True)
class CleanupResult:
    """
    Resultado de una limpieza de sesión.
    """

    removed_files: int = 0
    failed_files: list[Path] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.failed_files) == 0

    @property
    def message(self) -> str:

        if self.success:
            return (
                f"Limpieza finalizada. "
                f"Archivos eliminados: {self.removed_files}."
            )

        return (
            f"Limpieza finalizada con errores. "
            f"Eliminados: {self.removed_files}. "
            f"No eliminados: {len(self.failed_files)}."
        )


class ScannerCleanupService:
    """
    Servicio encargado de destruir completamente
    una sesión temporal de escaneo.

    Responsabilidades:

    - eliminar archivos temporales
    - limpiar la sesión del documento
    - reiniciar la configuración temporal
      del escáner

    No conoce la interfaz gráfica.
    """

    def cleanup(self) -> CleanupResult:
        """
        Ejecuta la limpieza completa.
        """

        result = CleanupResult()

        for directory in self._temporary_directories():

            self._remove_directory_files(
                directory,
                result,
            )

        self._clear_document_session()

        self._reset_scanner_session()

        return result

    @staticmethod
    def _temporary_directories() -> tuple[Path, ...]:
        """
        Devuelve las carpetas temporales
        administradas por el servicio.
        """

        return (
            SCANNER_TEMP_DIR,
        )

    @staticmethod
    def _remove_directory_files(directory: Path, result: CleanupResult) -> None:
        """
        Elimina archivos y carpetas temporales
        de forma recursiva.
        """

        if not directory.exists():
            return

        for item in directory.iterdir():
            try:
                if item.is_file():
                    item.unlink()
                    result.removed_files += 1
                elif item.is_dir():
                    ScannerCleanupService._remove_directory_files(item, result)
                    item.rmdir()

            except Exception:
                result.failed_files.append(item)
 

    @staticmethod
    def _clear_document_session() -> None:
        """
        Vacía la sesión del documento.
        """

        document_session.clear()

    @staticmethod
    def _reset_scanner_session() -> None:
        """
        Restablece la configuración temporal
        del escáner.
        """

        scanner_session.reset()


scanner_cleanup = ScannerCleanupService()