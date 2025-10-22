#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def _locate_venv() -> Path | None:
    base_dir = Path(__file__).resolve().parent
    for candidate in (base_dir / ".venv", base_dir.parent / ".venv"):
        if candidate.exists():
            return candidate
    return None


def _prepare_environment() -> None:
    venv_dir = _locate_venv()
    if venv_dir is None:
        return
    if Path(sys.prefix).resolve() != venv_dir.resolve():
        os.execvp("uv", ["uv", "run", "python", *sys.argv])


def main():
    """Run administrative tasks."""
    _prepare_environment()
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
