# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Event, EventMediaData


class EventMediaInline(admin.TabularInline):
    model = EventMediaData
    fields = ('media_file', 'media', 'original_file_info', 'medium_file_info', 'is_video', 'video_link', 'media_title', 'enlarged_thumbnail_size', 'is_published')
    readonly_fields = ('media_file', 'original_file_info', 'medium_file_info')
    extra = 5


class EventAdmin(admin.ModelAdmin):
    fields = (
       'event_thumbnail', 'thumbnail', 'title', 'slug', 'description', 'start_date', 'end_date', 'keywords', 'is_banner', 'created_date', 'published_date', 'is_published')

    readonly_fields = ('event_thumbnail',)
    inlines = [EventMediaInline]
    list_display = ('title', 'start_date', 'end_date', 'is_banner', 'is_published')


admin.site.register(Event, EventAdmin)
