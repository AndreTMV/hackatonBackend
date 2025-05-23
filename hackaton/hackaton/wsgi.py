"""
WSGI config for hackaton project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
import os


from django.core.wsgi import get_wsgi_application
settings_module = 'hackaton.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'hackaton.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
