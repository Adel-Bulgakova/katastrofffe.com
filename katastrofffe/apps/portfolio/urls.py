# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.categories_list, name='categories_list'),
    url(r'^filter/tag/(?P<tag_name>[a-zA-Zа-яА-Я0-9-_]+)/(?P<page_number>[0-9]+)/$', view=views.filter_by_tag, name='filter_by_tag'),
    url(r'^filter/tag/(?P<tag_name>[a-zA-Zа-яА-Я0-9-_]+)/$', view=views.tag_detail, name='filter_by_tag'),
    url(r'^filter/category/(?P<category_slug>[a-zA-Zа-яА-Я0-9-_]+)/(?P<page_number>[0-9]+)/$', view=views.filter_by_category, name='filter_by_category'),
    url(r'^filter/page/(?P<page_number>[0-9]+)/$', view=views.filter_by_page, name='filter_by_page'),
    url(r'^(?P<hierarchy>.+)/$', views.show_category, name='category'),
]