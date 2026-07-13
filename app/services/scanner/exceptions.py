"""
Excepciones del subsistema de escaneo.
"""


class ScannerError(Exception):
    """Excepción base del módulo de escaneo."""

    default_message = "Error del sistema de escaneo."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class ScannerNotFoundError(ScannerError):
    default_message = "No se detectó ningún escáner."


class ScannerDetectionError(ScannerError):
    default_message = "No fue posible detectar los escáneres del sistema."


class ScannerConnectionError(ScannerError):
    default_message = "No fue posible establecer comunicación con el escáner."


class ScannerBusyError(ScannerError):
    default_message = "El escáner se encuentra ocupado por otra aplicación."


class ScannerConfigurationError(ScannerError):
    default_message = "La configuración del escáner no es válida."


class ScannerCapabilityError(ScannerError):
    default_message = "El escáner no soporta la configuración solicitada."


class ScannerAcquisitionError(ScannerError):
    default_message = "No fue posible adquirir la imagen desde el escáner."


class ScannerPaperError(ScannerError):
    default_message = "Se produjo un problema con el papel del escáner."


class ScannerCancelledError(ScannerError):
    default_message = "La operación fue cancelada por el usuario."


class ScannerFileError(ScannerError):
    default_message = "No fue posible guardar el archivo generado."


class ScannerInternalError(ScannerError):
    default_message = "Se produjo un error interno durante el proceso de escaneo."

class ScannerBusyError(ScannerError):
    """
    Se intenta iniciar un escaneo mientras
    otro continúa en ejecución.
    """

