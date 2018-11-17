# -*- coding: utf-8 -*-
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Post, PostMediaData


class PostMediaInline(admin.TabularInline):
    model = PostMediaData
    fields = ('media_file', 'media', 'original_file_info', 'medium_file_info', 'is_video', 'video_link', 'media_title', 'is_published')
    readonly_fields = ('media_file', 'original_file_info', 'medium_file_info')
    extra = 5


class PostAdmin(admin.ModelAdmin):
    fields = (
        'post_thumbnail', 'thumbnail', 'enlarged_thumbnail_size', 'slug', 'title', 'preview', 'content', 'keywords',
        'tags', 'category', 'created_date', 'published_date', 'is_published', 'show_post_detail')

    readonly_fields = ('post_thumbnail',)
    inlines = [PostMediaInline]
    list_display = ('slug', 'title', 'category', 'published_date', 'is_published', 'show_post_detail')


class CategoryAdmin(MPTTModelAdmin):
    fields = ('category_thumbnail', 'thumbnail', 'name', 'parent', 'slug', 'published_date', 'is_published')
    readonly_fields = ('category_thumbnail',)
    list_display = ('slug', 'name', 'published_date', 'is_published')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)