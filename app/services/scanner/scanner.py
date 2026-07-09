from pathlib import Path
from datetime import datetime

import pythoncom
import win32com.client

from app.core.config import SCANNER_TEMP_DIR
from app.services.scanner.session import scanner_session
from app.services.scanner.exceptions import (
    ScannerConnectionError,
    ScannerAcquisitionError,
    ScannerNotFoundError,
)


class ScannerService:
    """
    Servicio de comunicación con el escáner WIA.
    """

    def preview(self) -> str:
        """
        Realiza una captura de previsualización
        y devuelve la ruta de la imagen generada.
        """

        try:
            pythoncom.CoInitialize()

            device = self._get_device()

            image = device.Items(1).Transfer()

            SCANNER_TEMP_DIR.mkdir(
                parents=True,
                exist_ok=True,
            )

            filename = (
                f"preview_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                ".png"
            )

            filepath = SCANNER_TEMP_DIR / filename

            image.SaveFile(
                str(filepath)
            )

            return str(filepath)

        except ScannerNotFoundError:
            raise

        except pythoncom.com_error as exc:
            raise ScannerConnectionError(
                f"Error comunicando con el escáner.\n{exc}"
            ) from exc

        except Exception as exc:
            raise ScannerAcquisitionError(
                f"No se pudo realizar la previsualización.\n{exc}"
            ) from exc

        finally:
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass


    def _get_device(self):
        """
        Obtiene el dispositivo WIA seleccionado.
        """

        if not scanner_session.scanner_id:
            raise ScannerNotFoundError(
                "No hay escáner seleccionado."
            )

        manager = win32com.client.Dispatch(
            "WIA.DeviceManager"
        )

        for device_info in manager.DeviceInfos:

            if device_info.Type != 1:
                continue

            if str(device_info.DeviceID) == scanner_session.scanner_id:
                return device_info.Connect()

        raise ScannerNotFoundError(
            "El escáner seleccionado no está disponible."
        )