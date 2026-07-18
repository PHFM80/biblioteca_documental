#app\db\schema.py
from app.db.database import execute_query


def create_tipo_documento_table() -> None:
    execute_query("""
        CREATE TABLE IF NOT EXISTS tipo_documento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL UNIQUE
        );
    """)


def create_documento_table() -> None:
    execute_query("""
        CREATE TABLE IF NOT EXISTS documento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo_id INTEGER NOT NULL,
            ruta TEXT NOT NULL,
            tamaño_bytes INTEGER NOT NULL DEFAULT 0,
            fecha_creacion TEXT NOT NULL,
            fecha_modificacion TEXT NOT NULL,
            observaciones TEXT,
            hash_archivo TEXT UNIQUE,
            FOREIGN KEY (tipo_id)
                REFERENCES tipo_documento(id)
                ON DELETE RESTRICT
        );
    """)


def create_documento_pdf_table() -> None:
    execute_query("""
        CREATE TABLE IF NOT EXISTS documento_pdf (
            documento_id INTEGER PRIMARY KEY,
            cantidad_paginas INTEGER NOT NULL DEFAULT 0,
            tiene_ocr INTEGER NOT NULL DEFAULT 0,
            tiene_indexacion INTEGER NOT NULL DEFAULT 0,
            texto_ocr_ruta TEXT,
            pdf_editable_ruta TEXT,
            FOREIGN KEY (documento_id)
                REFERENCES documento(id)
                ON DELETE CASCADE
        );
    """)


def insert_default_data() -> None:
    execute_query("""
        INSERT OR IGNORE INTO tipo_documento(id, tipo)
        VALUES
            (1, 'PDF'),
            (2, 'MP3');
    """)


def init_database() -> None:
    """
    Inicializa completamente el esquema SQLite.
    Puede ejecutarse todas las veces que sea necesario.
    """

    create_tipo_documento_table()
    create_documento_table()
    create_documento_pdf_table()
    insert_default_data()