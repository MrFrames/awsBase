"""
WSGI config for awsBase project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

import sys

sys.path.append("/opt/bitnami/apps/django/django_projects/Project")
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/binami/apps/django/django_projects/Projects/egg_cache")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "awsBase.settings")

application = get_wsgi_application()
