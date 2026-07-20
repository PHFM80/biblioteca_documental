#tests\test_save_document_flow.py
from datetime import date

from app.services.document.dto.save_document_data import SaveDocumentData
from app.services.document.validators.save_document_validator import SaveDocumentValidator


def test_save_document_data_creation():
    data = SaveDocumentData(
        name="Contrato ejemplo",
        chinese_name="示例合同",
        reception_date=date.today(),
        observations="Documento de prueba",
        execute_ocr=True,
        execute_index=True,
        generate_docx=False,
    )

    assert data.name == "Contrato ejemplo"
    assert data.chinese_name == "示例合同"
    assert data.execute_ocr is True


def test_save_document_validator_valid_data():
    data = SaveDocumentData(
        name="Documento válido",
        chinese_name=None,
        reception_date=date.today(),
        observations=None,
        execute_ocr=False,
        execute_index=True,
        generate_docx=False,
    )

    validator = SaveDocumentValidator()

    errors = validator.validate(data)

    assert errors == []


def test_save_document_validator_invalid_name():
    data = SaveDocumentData(
        name="",
        chinese_name=None,
        reception_date=None,
        observations=None,
        execute_ocr=False,
        execute_index=False,
        generate_docx=False,
    )

    validator = SaveDocumentValidator()

    errors = validator.validate(data)

    assert "El nombre del documento es obligatorio." in errors