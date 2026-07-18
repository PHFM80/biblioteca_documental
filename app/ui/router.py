#app\ui\router.py

class Router:
    VALID_VIEWS = {"dashboard", "library", "import", "search", "load_pdf", "scan_document", "save_document"}

    def __init__(self):
        self._stack = ["dashboard"]

    @property
    def current_view(self):
        return self._stack[-1]

    def navigate(self, view: str):
        if view not in self.VALID_VIEWS:
            raise ValueError(f"Vista no válida: {view}")
        self._stack.append(view)

    def back(self):
        if len(self._stack) > 1:
            self._stack.pop()