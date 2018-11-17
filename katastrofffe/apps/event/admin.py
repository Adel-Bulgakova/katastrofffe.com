# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Event


class EventAdmin(admin.ModelAdmin):
    fields = (
       'event_thumbnail', 'thumbnail', 'title', 'slug', 'description', 'start_date', 'end_date', 'keywords', 'is_banner', 'created_date', 'published_date', 'is_published')

    readonly_fields = ('event_thumbnail',)
    list_display = ('title', 'start_date', 'end_date', 'is_banner', 'is_published')


admin.site.register(Event, EventAdmin)
