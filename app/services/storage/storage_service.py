# app/services/storage/storage_service.py
from pathlib import Path
from datetime import date
from dataclasses import dataclass
import shutil
from blake3 import blake3

@dataclass(frozen=True)
class StoredFileMetadata:
    path: Path
    size_bytes: int
    hash_blake3: str

class StorageService:
    def __init__(self, library_path: Path):
        self.library_path = library_path
        self.library_path.mkdir(parents=True, exist_ok=True)

    def _get_document_folder(self, reception_date: date, document_id: str) -> Path:
        """
        Define la estructura de carpetas:
        data/library/{YYYY}/{MM}/{document_id}/
        """
        folder = self.library_path / str(reception_date.year) / f"{reception_date.month:02d}" / document_id
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def _calculate_file_hash(self, file_path: Path) -> str:
        hasher = blake3()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def store_document_pdf(self, temp_pdf_path: Path, reception_date: date, document_id: str) -> StoredFileMetadata:
        """
        Mueve el PDF temporal a la ubicación definitiva y calcula sus metadatos físicos.
        """
        doc_folder = self._get_document_folder(reception_date, document_id)
        final_path = doc_folder / "documento.pdf"
        
        shutil.move(str(temp_pdf_path), str(final_path))
        
        return StoredFileMetadata(
            path=final_path,
            size_bytes=final_path.stat().st_size,
            hash_blake3=self._calculate_file_hash(final_path)
        )