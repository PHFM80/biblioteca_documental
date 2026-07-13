#app\services\scanner\scan_coordinator.py
from threading import Lock


class ScanCoordinator:
    """
    Coordina el ciclo completo de un escaneo.
    Garantiza que solamente exista
    un proceso de escaneo activo.
    """

    def __init__(self):
        self._lock = Lock()

    def acquire(self) -> bool:
        return self._lock.acquire(blocking=False)
        
    def release(self) -> None:
        if self._lock.locked():
            self._lock.release()

    @property
    def busy(self) -> bool:
        return self._lock.locked()


scan_coordinator = ScanCoordinator()