#app\services\scanner\document_session.py
from app.services.scanner.document_page import DocumentPage


class DocumentSession:
    """
    Administra las páginas escaneadas del documento
    durante la sesión actual.
    """

    def __init__(self):
        self.clear()

    @property
    def page_count(self) -> int:
        return len(self._pages)

    def has_pages(self) -> bool:
        return self.page_count > 0

    def add_page(
        self,
        image_path: str,
        thumbnail_path: str,
    ) -> DocumentPage:
        """
        Agrega una nueva página al final del documento.
        """

        page = DocumentPage(
            page_number=self.page_count + 1,
            image_path=image_path,
            thumbnail_path=thumbnail_path,
        )

        self._pages.append(page)

        return page

    def get_pages(self) -> tuple[DocumentPage, ...]:
        """
        Devuelve una colección de solo lectura.
        """

        return tuple(self._pages)

    def get_last_page(self) -> DocumentPage | None:

        if not self.has_pages():
            return None

        return self._pages[-1]

    def remove_page(
        self,
        page_number: int,
    ) -> DocumentPage | None:
        """
        Elimina una página del documento y
        renumera las páginas restantes.
        """

        if page_number < 1:
            return None

        if page_number > self.page_count:
            return None

        removed_page = self._pages.pop(
            page_number - 1
        )

        self._renumber_pages()

        return removed_page

    def remove_last_page(self) -> DocumentPage | None:
        """
        Elimina la última página del documento.
        """

        if not self.has_pages():
            return None

        return self.remove_page(
            self.page_count
        )

    def clear(self):
        """
        Reinicia completamente la sesión.
        """

        self._pages: list[DocumentPage] = []

    def _renumber_pages(self):
        """
        Actualiza la numeración de todas
        las páginas del documento.
        """

        for index, page in enumerate(
            self._pages,
            start=1,
        ):
            page.page_number = index


document_session = DocumentSession()