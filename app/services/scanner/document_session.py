#app\services\scanner\document_session.py
from app.services.scanner.document_page import DocumentPage


class DocumentSession:

    def __init__(self):
        self.clear()


    @property
    def page_count(self):
        return len(self._pages)


    def has_pages(self):
        return self.page_count > 0


    def add_page(
        self,
        image_path: str,
        thumbnail_path: str,
    ) -> DocumentPage:

        page = DocumentPage(
            page_number=self.page_count + 1,
            image_path=image_path,
            thumbnail_path=thumbnail_path,
        )

        self._pages.append(page)

        return page


    def get_pages(self):
        return tuple(self._pages)


    def get_last_page(self):
        if not self.has_pages():
            return None

        return self._pages[-1]


    def remove_last_page(self):

        if not self.has_pages():
            return None

        return self._pages.pop()


    def clear(self):
        self._pages = []


document_session = DocumentSession()