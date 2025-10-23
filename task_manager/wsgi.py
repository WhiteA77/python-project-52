"""
WSGI config for task_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")

application = get_wsgi_application()

if getattr(settings, "ROLLBAR", None):
    try:
        import rollbar
    except ImportError:
        rollbar = None
    else:
        rollbar.init(
            access_token=settings.ROLLBAR["access_token"],
            environment=settings.ROLLBAR["environment"],
            root=settings.ROLLBAR["root"],
            code_version=settings.ROLLBAR.get("code_version"),
        )
