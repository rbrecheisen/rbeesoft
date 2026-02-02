import os
from PySide6.QtCore import Qt, QByteArray
from PySide6.QtWidgets import QMainWindow, QStyle, QFileDialog
from PySide6.QtGui import QGuiApplication, QAction
from rbeesoft.app.ui.settings import Settings
from rbeesoft.app.ui.widgets import CentralDockWidget
from rbeesoft.app.ui.widgets import LogDockWidget
from rbeesoft.common import LicenseManager
from rbeesoft.common.exceptions import LicenseException
from rbeesoft.common import LogManager

LOG = LogManager()

PUBLIC_KEY_B64 = 'C7yBmGtvBkvnvGtWiey4PKXZWo7Lza61+FwV2UyAu34='


class RbeesoftMainWindow(QMainWindow):
    def __init__(self, bundle_identifier, app_name, app_title, app_width=1024, app_height=1024, app_icon=None):
        super(RbeesoftMainWindow, self).__init__()
        self._settings = Settings(bundle_identifier, app_name)
        self._settings.set('public_key', PUBLIC_KEY_B64)
        self._app_title = app_title
        self._app_width = app_width
        self._app_height = app_height
        self._app_icon = app_icon
        self._central_dockwidget = None
        self._log_dockwidget = None
        self._license_manager = None
        self._license = None
        self.init()

    # INITIALIZATION

    def init(self):
        self.setWindowTitle(self.app_title())
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.central_dockwidget())
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.log_dockwidget())
        LOG.info(f'Settings path: {self.settings().fileName()}')
        if self.app_icon():
            self.setWindowIcon(self.app_icon())
        self.load_geometry_and_state()
        self.init_default_menus()
        self.check_license()
        self.statusBar().showMessage('Ready')

    def init_default_menus(self):
        # Application menu
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
        exit_action = QAction(icon, 'E&xit', self)
        exit_action.triggered.connect(self.close)
        application_menu = self.menuBar().addMenu('Application')
        application_menu.addAction(exit_action)
        # Settings menu
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_VistaShield)
        open_license_file_action = QAction(icon, 'Open license file...', self)
        open_license_file_action.triggered.connect(self.handle_open_license_file_action)
        settings_menu = self.menuBar().addMenu('Settings')
        settings_menu.addAction(open_license_file_action)

    # GETTERS

    def settings(self):
        return self._settings
    
    def app_title(self):
        return self._app_title
    
    def app_width(self):
        return self._app_width
    
    def app_height(self):
        return self._app_height
    
    def app_icon(self):
        return self._app_icon
    
    def central_dockwidget(self):
        if not self._central_dockwidget:
            self._central_dockwidget = CentralDockWidget(self, self.settings())
        return self._central_dockwidget
    
    def log_dockwidget(self):
        if not self._log_dockwidget:
            self._log_dockwidget = LogDockWidget(self)
            LOG.add_listener(self._log_dockwidget)
        return self._log_dockwidget
    
    def license_manager(self):
        if not self._license_manager:
            self._license_manager = LicenseManager(self.settings().get('public_key', None))
        return self._license_manager
    
    def license(self):
        return self._license
    
    # EVENT HANDLERS

    def closeEvent(self, event):
        self.save_geometry_and_state()
        return super().closeEvent(event)

    def handle_open_license_file_action(self):
        last_directory = self.settings().get('mainwindow/last_directory', None)
        file_path, _ = QFileDialog.getOpenFileName(dir=last_directory)
        if file_path:
            self.settings().set('mainwindow/last_directory', os.path.split(file_path)[0])
            self.settings().set('mainwindow/license_file', file_path)
            self.check_license()

    # HELPERS

    def add_page(self, page, home_page=False):
        self.central_dockwidget().add_page(page, home_page)

    def check_license(self):
        file_path = self.settings().get('mainwindow/license_file', None)
        if file_path:
            try:
                self._license = self.license_manager().verify(file_path)
                LOG.info(f'License found at {file_path}')
                LOG.info('License OK')
                return True
            except LicenseException as e:
                LOG.info(e)
                return False
        LOG.info('No license found')
        return False

    def load_geometry_and_state(self):
        geometry = self.settings().get('mainwindow/geometry')
        state = self.settings().get('mainwindow/state')
        if isinstance(geometry, QByteArray) and self.restoreGeometry(geometry):
            if isinstance(state, QByteArray):
                self.restoreState(state)
            return
        self.resize(self.app_width(), self.app_height())
        self.center_window()        

    def save_geometry_and_state(self):
        self.settings().set('mainwindow/geometry', self.saveGeometry())
        self.settings().set('mainwindow/state', self.saveState())

    def center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))