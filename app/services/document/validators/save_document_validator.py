#app\services\validators\save_document_validator.py
from datetime import datetime, date

from app.services.document.dto.save_document_data import SaveDocumentData


class SaveDocumentValidator:
    """
    Valida los datos recibidos antes del proceso de guardado.
    No modifica datos ni interactúa con persistencia.
    """

    def validate(self, data: SaveDocumentData) -> list[str]:
        errors = []

        self._validate_name(data.name, errors)
        self._validate_chinese_name(data.chinese_name, errors)
        self._validate_reception_date(data.reception_date, errors)

        return errors

    def _validate_name(self, value: str, errors: list[str]) -> None:
        if not isinstance(value, str) or not value.strip():
            errors.append("El nombre del documento es obligatorio.")

    def _validate_chinese_name(self, value: str | None, errors: list[str]) -> None:
        if value is not None and (not isinstance(value, str) or not value.strip()):
            errors.append("El nombre en chino debe contener texto válido.")

    def _validate_reception_date(self, value, errors: list[str]) -> None:
        if value is None:
            return

        if not isinstance(value, date):
            errors.append("La fecha de recepción tiene un formato inválido.")
