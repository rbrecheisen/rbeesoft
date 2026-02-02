from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget


class Page(QWidget):
    page_changed = Signal(str)

    def __init__(self, name, title, settings, license=None):
        super(Page, self).__init__()
        self._name = name
        self._title = title
        self._settings = settings
        self._license = license

    def name(self):
        return self._name

    def title(self):
        return self._title
    
    def settings(self):
        return self._settings
    
    def license(self):
        return self._license
    
    def switch_to_page(self, name):
        self.page_changed.emit(name)