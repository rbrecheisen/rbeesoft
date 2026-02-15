import os
import sys
import ast
from pathlib import Path
from typing import Dict, Union


class Settings:
    def __init__(self, settings_path):
        self._settings = self.settings_py_to_string_dict(settings_path)

    def settings_py_to_string_dict(
        self,
        settings_path: Union[str, Path],
        *,
        only_uppercase: bool = True,
        include_dunder: bool = False,
    ) -> Dict[str, str]:
        """
        Parse a Django settings.py file and return a dict mapping constant names to
        the RHS expression as source text (string).

        - Does NOT execute/import settings.py (safe).
        - Captures only simple assignments at module scope: NAME = <expr>
        (not destructuring, not augmented assigns, not inside if/for/def/class).
        - Values are stored as strings representing the RHS code so you can later
        write settings.py back out.

        Parameters
        ----------
        settings_path : str | Path
            Path to settings.py
        only_uppercase : bool
            If True, include only names that are all uppercase (common Django style).
        include_dunder : bool
            If True, allow __FOO__ style names. Default False.

        Returns
        -------
        dict[str, str]
            Mapping of constant name -> RHS source code (string).
        """
        settings_path = Path(settings_path)
        src = settings_path.read_text(encoding="utf-8")
        tree = ast.parse(src, filename=str(settings_path), type_comments=True)

        def is_allowed_name(name: str) -> bool:
            if not include_dunder and name.startswith("__") and name.endswith("__"):
                return False
            if only_uppercase and not name.isupper():
                return False
            return True

        out: Dict[str, str] = {}

        # Only consider direct children of the module (module-level statements).
        for node in tree.body:
            # Handle: NAME = <expr>  (possibly multiple targets: A = B = <expr>)
            if isinstance(node, ast.Assign):
                # RHS source text
                rhs = ast.get_source_segment(src, node.value) or ""
                rhs = rhs.strip()

                # Each target may be a Name (ignore Tuple/List destructuring)
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        if is_allowed_name(name):
                            out[name] = rhs

            # Handle: NAME: type = <expr>
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name) and node.value is not None:
                    name = node.target.id
                    if is_allowed_name(name):
                        rhs = ast.get_source_segment(src, node.value) or ""
                        out[name] = rhs.strip()
        return out


class RbeesoftWebApp:
    def __init__(self):
        self._settings = Settings('webapp/settings.py')
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