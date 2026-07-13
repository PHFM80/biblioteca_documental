from pathlib import Path

from app.core.config import SCANNER_TEMP_DIR

from app.services.scanner.scanner_cleanup import scanner_cleanup
from app.services.scanner.document_session import document_session
from app.services.scanner.session import scanner_session


def create_dummy_files():

    SCANNER_TEMP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for index in range(3):

        file = SCANNER_TEMP_DIR / f"dummy_{index}.png"

        file.write_text("test")


def print_status(title):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    print()

    print("Scanner Session")
    print(scanner_session.summary())

    print()

    print("Document Session")
    print(f"Páginas: {document_session.page_count}")

    for page in document_session.get_pages():

        print(
            page.page_number,
            page.image_path,
        )

    print()

    files = list(
        SCANNER_TEMP_DIR.glob("*")
    )

    print(
        f"Archivos temporales: {len(files)}"
    )

    for file in files:
        print(file.name)

    print()


def populate_sessions():

    scanner_session.update(
        scanner_id="123",
        scanner_name="Scanner Test",
        dpi=600,
        color_mode="Color",
        page_size="A4",
    )

    document_session.add_page(
        image_path="page1.png",
        thumbnail_path="thumb1.png",
    )

    document_session.add_page(
        image_path="page2.png",
        thumbnail_path="thumb2.png",
    )

    create_dummy_files()


def main():

    populate_sessions()

    print_status(
        "ANTES DE CLEANUP"
    )

    result = scanner_cleanup.cleanup()

    print_status(
        "DESPUÉS DE CLEANUP"
    )

    print(result.message)

    print()

    print(
        "SUCCESS:",
        result.success,
    )


if __name__ == "__main__":
    main()