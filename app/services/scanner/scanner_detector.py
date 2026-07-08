from dataclasses import dataclass, field

import pythoncom
import win32com.client

from app.services.scanner.exceptions import (
    ScannerConnectionError,
    ScannerDetectionError,
    ScannerInternalError,
    ScannerNotFoundError,
)


@dataclass(slots=True)
class ScannerInfo:
    """Información básica de un escáner."""

    id: str
    name: str


@dataclass(slots=True)
class ScannerDetectionResult:
    """Resultado de la detección de escáneres."""

    success: bool
    scanners: list[ScannerInfo] = field(default_factory=list)
    default_scanner: ScannerInfo | None = None
    message: str = ""


class ScannerDetector:
    """
    Detecta los escáneres WIA disponibles en Windows.
    """

    def detect(self) -> ScannerDetectionResult:

        try:
            pythoncom.CoInitialize()

            device_manager = win32com.client.Dispatch(
                "WIA.DeviceManager"
            )

            scanners: list[ScannerInfo] = []

            for device in device_manager.DeviceInfos:

                # 1 = Scanner (WIA)
                if device.Type != 1:
                    continue

                scanners.append(
                    ScannerInfo(
                        id=str(device.DeviceID),
                        name=str(device.Properties["Name"].Value),
                    )
                )
                device= None

            if not scanners:
                raise ScannerNotFoundError()
            device_manager = None
            return ScannerDetectionResult(
                success=True,
                scanners=scanners,
                default_scanner=scanners[0],
                message=f"{len(scanners)} escáner(es) detectado(s).",
            )

        except ScannerNotFoundError:
            raise

        except pythoncom.com_error as exc:
            raise ScannerConnectionError(
                f"No fue posible acceder al servicio WIA.\n{exc}"
            ) from exc

        except Exception as exc:
            raise ScannerDetectionError(
                f"Error detectando escáneres.\n{exc}"
            ) from exc

        finally:
            try:
                device_manager = None
                pythoncom.CoUninitialize()
            except Exception:
                pass