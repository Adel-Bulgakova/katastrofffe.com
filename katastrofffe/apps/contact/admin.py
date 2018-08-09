# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Contact


class ContactAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('email', 'message', 'published_date')
    fieldsets = [
        (None, {'fields':()}),
        ]

    def __init__(self, *args, **kwargs):
        super(ContactAdmin, self).__init__(*args, **kwargs)
        # self.list_display_links = (None, )


admin.site.register(Contact, ContactAdmin)