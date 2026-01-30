import sys
from PySide6 import QtWidgets
from rbeesoft.app.ui.rbeesoftmainwindow import RbeesoftMainWindow


class MainWindow(RbeesoftMainWindow):
    def __init__(self, app_icon):
        super(MainWindow, self).__init__(
            bundle_identifier='rbeesoft.nl',
            app_name='example',
            app_title='Rbeesoft App Example',
            width=800,
            height=600,
            app_icon=app_icon,
        )


def main():
    QtWidgets.QApplication.setApplicationName('example')
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowForward))
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()