from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QDockWidget,
    QStackedWidget,
)
from rbeesoft.common.logmanager import LogManager

LOG = LogManager()


class CentralDockWidget(QDockWidget):
    def __init__(self, parent, settings):
        super(CentralDockWidget, self).__init__(parent)
        self._settings = settings
        self._stacked_widget = None
        self._pages = None
        self.init()

    # INITIALIZATION

    def init(self):
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget())
        container = QWidget()
        container.setLayout(layout)
        self.setObjectName('centraldockwidget') # Needed for saving geometry/state
        self.setWidget(container)

    # GETTERS/SETTERS

    def settings(self):
        return self._settings
    
    def stacked_widget(self):
        if not self._stacked_widget:
            self._stacked_widget = QStackedWidget()
        return self._stacked_widget
    
    def pages(self):
        if not self._pages:
            self._pages = {}
        return self._pages
    
    # HELPERS

    def add_page(self, page, name):
        self.pages()[name] = page
        self.stacked_widget().addWidget(page)

    def select_panel(self, name):
        page = self.pages().get(name, None)
        if page:
            self.stacked_widget().setCurrentWidget(page)