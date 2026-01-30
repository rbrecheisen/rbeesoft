import sys
from PySide6 import QtWidgets
from rbeesoft.app.ui.rbeesoftmainwindow import RbeesoftMainWindow


def main():
    QtWidgets.QApplication.setApplicationName('rbeesoft.app')
    app = QtWidgets.QApplication(sys.argv)
    window = RbeesoftMainWindow(
        bundle_identifier='rbeesoft.nl',
        app_name='example',
        app_title='Rbeesoft App Example',
        width=800,
        height=600,
        app_icon=app.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowForward),
    )
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()