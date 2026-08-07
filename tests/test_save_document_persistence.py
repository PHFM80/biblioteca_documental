import blake3
from datetime import date
from unittest.mock import MagicMock

import pytest

import app.db.database
import app.services.document.save_document_service as svc_module
from app.db.schema import init_database
from app.models import Documento, DocumentoPDF
from app.services.document.dto.save_document_data import SaveDocumentData
from app.services.document.save_document_service import SaveDocumentService

PDF_CONTENT = b"%PDF-1.4 fake pdf content"
EXPECTED_HASH = blake3.blake3(PDF_CONTENT).hexdigest()


def make_data(**overrides) -> SaveDocumentData:
    defaults = dict(
        name="Contrato de prueba",
        chinese_name="测试合同",
        reception_date=date(2026, 8, 7),
        observations="Observaciones de prueba",
        execute_ocr=False,
        execute_index=False,
        generate_docx=False,
    )
    defaults.update(overrides)
    return SaveDocumentData(**defaults)


def fake_generate(pages, output_path):
    output_path.write_bytes(PDF_CONTENT)
    return output_path


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test_biblioteca.db"
    monkeypatch.setattr(app.db.database, "DB_PATH", db_file)
    init_database()
    return db_file


@pytest.fixture
def temp_library(tmp_path, monkeypatch):
    library = tmp_path / "library"
    library.mkdir()
    monkeypatch.setattr(svc_module, "LIBRARY_DIR", library)
    return library


@pytest.fixture
def fake_session(monkeypatch):
    session = MagicMock()
    session.get_pages.return_value = [object(), object(), object()]
    monkeypatch.setattr(svc_module, "document_session", session)
    return session


@pytest.fixture
def fake_cleanup(monkeypatch):
    cleanup = MagicMock()
    monkeypatch.setattr(svc_module, "scanner_cleanup", cleanup)
    return cleanup


@pytest.fixture
def save_service(temp_db, temp_library, fake_session, fake_cleanup):
    pdf_generator = MagicMock()
    pdf_generator.generate.side_effect = fake_generate
    ocr_service = MagicMock()
    index_service = MagicMock()
    return SaveDocumentService(pdf_generator, ocr_service, index_service)


def test_pdf_se_guarda_en_library(save_service, temp_library):
    pdf_path = save_service.save(make_data())
    assert pdf_path.exists()
    assert pdf_path.parent == temp_library
    assert pdf_path.read_bytes() == PDF_CONTENT


def test_documento_se_persiste(save_service, temp_db, temp_library):
    save_service.save(make_data())
    from app.db.repositories.documento_repository import DocumentoRepository
    repo = DocumentoRepository()
    docs = repo.get_all()
    assert len(docs) == 1
    doc = docs[0]
    assert doc.nombre == "Contrato de prueba"
    assert doc.tamaño_bytes == len(PDF_CONTENT)
    assert doc.hash_archivo == EXPECTED_HASH
    assert doc.ruta == str(list(temp_library.glob("*.pdf"))[0])


def test_documento_pdf_se_persiste(save_service, temp_db, temp_library):
    save_service.save(make_data())
    from app.db.repositories.documento_repository import DocumentoRepository
    from app.db.repositories.documento_pdf_repository import DocumentoPDFRepository
    doc_repo = DocumentoRepository()
    pdf_repo = DocumentoPDFRepository()
    doc = doc_repo.get_all()[0]
    doc_pdf = pdf_repo.get_by_document_id(doc.id)
    assert doc_pdf is not None
    assert doc_pdf.cantidad_paginas == 3
    assert doc_pdf.nombre_chino == "测试合同"
    assert doc_pdf.tiene_ocr is False
    assert doc_pdf.tiene_indexacion is False


def test_duplicado_lanza_error(save_service, temp_library):
    save_service.save(make_data())
    with pytest.raises(ValueError, match="ya existe"):
        save_service.save(make_data())
    pdfs = list(temp_library.glob("*.pdf"))
    assert len(pdfs) == 1


def test_ocr_e_index_se_llaman(save_service, temp_db, temp_library):
    data = make_data(execute_ocr=True, execute_index=True)
    save_service.save(data)
    from app.db.repositories.documento_repository import DocumentoRepository
    doc = DocumentoRepository().get_all()[0]
    save_service.ocr_service.process.assert_called_once_with(doc.id)
    save_service.index_service.index.assert_called_once_with(doc.id)


def test_cleanup_se_llama(save_service, fake_cleanup):
    save_service.save(make_data())
    fake_cleanup.cleanup.assert_called_once()