import os
import sys
from webapp.rbeesoftwebappsettings import RbeesoftWebAppSettings


class RbeesoftWebApp:
    def __init__(self):
        self._settings = RbeesoftWebAppSettings('webapp/settings.py')
        print(self._settings)

    def add_setting(self):
        pass

    def run(self):
        self._run_internal('makemigrations')
        self._run_internal('migrate')
        self._run_internal('createadminuser')
        self._run_internal()

    def _run_internal(self, cmd='runserver'):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        args = [sys.argv[0], cmd]
        execute_from_command_line(args)


def main():
    app = RbeesoftWebApp()
    app.run()


if __name__ == '__main__':
    main()