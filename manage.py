#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def _activate_virtualenv() -> None:
    """Activate local virtual environment if present."""
    base_dir = Path(__file__).resolve().parent
    candidates = [
        base_dir / ".venv",
        base_dir.parent / ".venv",
    ]
    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate_this.py"
        if not activate_script.exists():
            activate_script = venv_dir / "Scripts" / "activate_this.py"
        if activate_script.exists():
            with open(activate_script, "rb") as file:
                exec(
                    compile(file.read(), str(activate_script), "exec"),
                    {"__file__": str(activate_script)},
                )
            break


def main():
    """Run administrative tasks."""
    _activate_virtualenv()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    try:
        from django.conf import settings
        import rollbar
    except ImportError:
        rollbar = None
    else:
        if getattr(settings, "ROLLBAR", None):
            rollbar.init(
                access_token=settings.ROLLBAR["access_token"],
                environment=settings.ROLLBAR["environment"],
                root=settings.ROLLBAR["root"],
                code_version=settings.ROLLBAR.get("code_version"),
            )

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
