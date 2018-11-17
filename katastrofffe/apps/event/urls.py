# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views
from .models import Event

urlpatterns = [
    url(r'^(?P<event_slug>[a-zA-Z0-9-_]+)/$', views.event_detail, name='event_detail'),
    url(r'^$', views.events_list, name='events_list')
]