"""
WSGI config for katastrofffe project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

# -*- coding: utf-8 -*-

import os,sys

sys.path.insert(0, '/home/m/milena/katastrofffe.com/public_html')
sys.path.insert(0, '/home/m/milena/katastrofffe.com')
sys.path.insert(0, '/home/m/milena/.djangovenv/lib64/python2.7/site-packages/')
os.environ["DJANGO_SETTINGS_MODULE"] = "katastrofffe.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()