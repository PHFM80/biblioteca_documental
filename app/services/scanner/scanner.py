#app\services\scanner\scanner.py
from pathlib import Path
from datetime import datetime

import pythoncom
import win32com.client

from app.core.config import SCANNER_TEMP_DIR
from app.services.scanner.session import scanner_session
from app.services.scanner.exceptions import (ScannerConnectionError, ScannerAcquisitionError, ScannerNotFoundError)


class ScannerService:
    """
    Servicio de comunicación con el escáner WIA.
    """
    def preview(self) -> str:
        """
        Realiza una captura rápida de previsualización.
        """
        return self._capture(prefix="preview")

    def scan(self) -> str:
        """
        Realiza un escaneo definitivo de una página.
        Devuelve la ruta del PNG temporal generado.
        """

        return self._capture(prefix="scan")

    def _apply_configuration(self, item):
        item.Properties["Horizontal Resolution"].Value = scanner_session.dpi
        item.Properties["Vertical Resolution"].Value = scanner_session.dpi

        if scanner_session.color_mode == "Blanco y negro":
            item.Properties["Current Intent"].Value = 4
        elif scanner_session.color_mode == "Escala de grises":
            item.Properties["Current Intent"].Value = 2
        elif scanner_session.color_mode == "Color":
            item.Properties["Current Intent"].Value = 1
        
    def _capture(self, prefix: str) -> str:
        """
        Ejecuta una captura WIA y guarda la imagen
        temporalmente.

        La diferencia entre preview y scan está
        únicamente en el propósito del archivo.
        """

        try:
            pythoncom.CoInitialize()

            device = self._get_device()

            item = device.Items(1)
            #self._debug_properties(item)
            self._apply_configuration(item)
            image = item.Transfer()

            SCANNER_TEMP_DIR.mkdir(
                parents=True,
                exist_ok=True,
            )

            filename = (
                f"{prefix}_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
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
                f"No se pudo realizar el escaneo.\n{exc}"
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

    def _debug_properties(self, item):
        print("\n===== PROPIEDADES WIA =====")

        for prop in item.Properties:
            try:
                print(
                    prop.PropertyID,
                    "|",
                    prop.Name,
                    "|",
                    prop.Value
                )
            except Exception:
                print(
                    prop.PropertyID,
                    "|",
                    prop.Name,
                    "| ERROR"
                )

        print("===========================\n")