# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views
from .models import Contact

urlpatterns = [
    url(r'^$', views.contact_page, name='contact_page'),
]