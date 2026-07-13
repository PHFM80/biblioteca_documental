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

        print("SCAN COORDINATOR -> acquire()")

        acquired = self._lock.acquire(blocking=False)

        if acquired:
            print("SCAN COORDINATOR -> LOCK ADQUIRIDO")
        else:
            print("SCAN COORDINATOR -> LOCK OCUPADO")

        return acquired


    def release(self) -> None:
        
        print("SCAN COORDINATOR -> release()")

        if self._lock.locked():
            self._lock.release()
            print("SCAN COORDINATOR -> LOCK LIBERADO")

    @property
    def busy(self) -> bool:
        return self._lock.locked()


scan_coordinator = ScanCoordinator()