import os
from PySide6.QtCore import Qt, QByteArray, Signal
from PySide6.QtWidgets import QMainWindow, QStyle, QFileDialog
from PySide6.QtGui import QGuiApplication, QAction
from rbeesoft.app.ui.settings import Settings
from rbeesoft.app.ui.widgets.centraldockwidget import CentralDockWidget
from rbeesoft.app.ui.widgets.logdockwidget import LogDockWidget
from rbeesoft.common.licensemanager import LicenseManager
from rbeesoft.common.exceptions.licenseexception import LicenseException
from rbeesoft.common.logmanager import LogManager

LOG = LogManager()

PUBLIC_KEY_B64 = 'C7yBmGtvBkvnvGtWiey4PKXZWo7Lza61+FwV2UyAu34='


class RbeesoftMainWindow(QMainWindow):
    license_changed = Signal(str)

    def __init__(self, bundle_identifier, app_name, app_title, app_major_version, app_width, app_height, app_icon, requires_license=False):
        super(RbeesoftMainWindow, self).__init__()
        self._settings = Settings(bundle_identifier, app_name)
        self._settings.set('public_key', PUBLIC_KEY_B64)
        self._settings.set('major_version', app_major_version)
        self._app_title = app_title
        self._app_major_version = app_major_version
        self._app_width = app_width
        self._app_height = app_height
        self._app_icon = app_icon
        self._requires_license = requires_license
        self._application_menu = None
        self._settings_menu = None
        self._views_menu = None
        self._central_dockwidget = None
        self._log_dockwidget = None
        self._license_manager = None
        self._license = None
        self._init()

    # INITIALIZATION

    def _init(self):
        self.setWindowTitle(self.app_title() + f' ({self.app_major_version()})')
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.central_dockwidget())
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.log_dockwidget())
        LOG.info(f'Settings path: {self.settings().fileName()}')
        if self.app_icon():
            self.setWindowIcon(self.app_icon())
        self._load_geometry_and_state()
        self._init_default_menus()
        if self._requires_license:
            self._check_license()
        self.statusBar().showMessage('Ready')

    def _init_default_menus(self):
        # Application menu
        self._application_menu = self.menuBar().addMenu('Application')
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
        exit_action = QAction(icon, 'E&xit', self)
        exit_action.triggered.connect(self.close)
        self._application_menu.addAction(exit_action)
        # Settings menu
        self._settings_menu = self.menuBar().addMenu('Settings')
        if self._requires_license:
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_VistaShield)
            open_license_file_action = QAction(icon, 'Open license file...', self)
            open_license_file_action.triggered.connect(self.handle_open_license_file_action)
            self._settings_menu.addAction(open_license_file_action)
        # Views
        self._views_menu = self.menuBar().addMenu('Views')
        view_log_action = self.log_dockwidget().toggleViewAction()
        view_log_action.setText('Log')
        self._views_menu.addAction(view_log_action)
    
    # GETTERS

    def settings(self):
        return self._settings
    
    def app_title(self):
        return self._app_title
    
    def app_major_version(self):
        return self._app_major_version
    
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
    
    def application_menu(self):
        return self._application_menu
    
    def settings_menu(self):
        return self._settings_menu
    
    def views_menu(self):
        return self._views_menu
    
    def license_manager(self):
        if not self._license_manager:
            self._license_manager = LicenseManager(self.settings())
        return self._license_manager
    
    def license(self):
        return self._license
    
    # EVENT HANDLERS

    def closeEvent(self, event):
        self._save_geometry_and_state()
        return super().closeEvent(event)

    def handle_open_license_file_action(self):
        last_directory = self.settings().get('mainwindow/last_directory', None)
        file_path, _ = QFileDialog.getOpenFileName(dir=last_directory)
        if file_path:
            self.settings().set('mainwindow/last_directory', os.path.split(file_path)[0])
            self.settings().set('mainwindow/license_file', file_path)
            self._check_license()

    # HELPERS

    def add_page(self, page, home_page=False):
        self.central_dockwidget().add_page(page, home_page)

    def switch_to_page(self, name):
        self.central_dockwidget().switch_to_page(name)

    def _check_license(self):
        file_path = self.settings().get('mainwindow/license_file', None)
        if file_path:
            try:
                self._license = self.license_manager().check_license(file_path)
                LOG.info(f'License found at {file_path}')
                LOG.info('License OK')
                LOG.info('(You may have to restart the tool to see extended functionality)')
                return True
            except LicenseException as e:
                LOG.info(e)
                return False
        LOG.info('No license found')
        return False

    def _load_geometry_and_state(self):
        geometry = self.settings().get('mainwindow/geometry')
        state = self.settings().get('mainwindow/state')
        if isinstance(geometry, QByteArray) and self.restoreGeometry(geometry):
            if isinstance(state, QByteArray):
                self.restoreState(state)
            return
        self.resize(self.app_width(), self.app_height())
        self._center_window()        

    def _save_geometry_and_state(self):
        self.settings().set('mainwindow/geometry', self.saveGeometry())
        self.settings().set('mainwindow/state', self.saveState())

    def _center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))