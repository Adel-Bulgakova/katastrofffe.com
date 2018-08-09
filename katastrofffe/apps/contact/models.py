# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Contact(models.Model):
    published_date = models.DateTimeField('Date of publication', auto_now_add=True)
    email = models.CharField(max_length=100)
    message = models.TextField()

    def __unicode__(self):
        return self.email