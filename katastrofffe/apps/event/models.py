# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import random, string, math
import datetime
from django.db import models
from django.utils import timezone
from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile


def set_file_path(filename, path):

    random_name = ''.join(random.choice(string.ascii_letters + string.digits) for n in range(12))
    name, ext = os.path.splitext(filename)
    full_file_name = random_name + ext
    return os.path.join(path, full_file_name)


def get_file_size(instance):
    if not instance or instance.size == 0:
        return "0B"

    file_size = instance.size

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(file_size, 1024)))
    p = math.pow(1024, i)
    s = round(file_size / p, 2)
    return "%s %s" % (s, size_name[i])


def get_file_dimension(instance):
    return "%sx%s" % (instance.width, instance.height)


def image_preview(instance):
    file_preview = '<img src="%s" width=150>' % (instance.url)
    return file_preview


def upload_event_thumbnail(instance, filename):
    path = "events_thumbs/"
    upload_path = set_file_path(filename, path)
    return upload_path


class EventsManager(models.Manager):
    def published(self, **kwargs):
        return self.filter(is_published=True, **kwargs).order_by(
            '-created_date')

    def future_events(self, **kwargs):
        return self.filter(is_published=True, **kwargs).filter(end_date__gte=datetime.date.today()).order_by(
            '-created_date')

    def past_events(self, **kwargs):
        return self.filter(is_published=True, **kwargs).filter(end_date__lte=datetime.date.today()).order_by(
            '-created_date')


class Event(models.Model):
    thumbnail = models.ImageField(
        u"Change thumbnail",
        upload_to='events_thumbs/'
    )

    event_thumb = models.ImageField(
        u"Event thumb",
        upload_to='events_thumbs/thumbs/',
        blank=True,
        null=True
    )

    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        help_text="Short descriptive unique name for use in urls",
    )

    title = models.CharField(
        max_length=255,
        help_text="Short descriptive name for this event"
    )

    description = models.TextField(
        blank=True,
        null=True,
        default="",
        help_text="Description",
    )

    start_date = models.DateField(
        blank=True,
        null=True
    )

    end_date = models.DateField(
        blank=True,
        null=True
    )

    keywords = models.TextField(
        blank=True,
        null=True,
        default="",
    )

    is_banner = models.BooleanField(
        default=False,
        help_text="This event will be shown on main page as a banner"
    )

    created_date = models.DateField(default=timezone.now)
    published_date = models.DateField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    objects = EventsManager()

    __original_image_filename = None

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self.__original_image_filename = self.thumbnail.name

    def __str__(self):
        return self.title

    def create_resized_images(self, *args, **kwargs):

        if self.thumbnail.name != self.__original_image_filename:
            image = Image.open(StringIO(self.thumbnail.read()))
            if hasattr(self.thumbnail.file, 'content_type'):
                content_type = self.thumbnail.file.content_type
                if content_type == 'image/jpeg':
                    pil_type = 'jpeg'
                    file_extension = 'jpg'
                elif content_type == 'image/png':
                    pil_type = 'png'
                    file_extension = 'png'

                image_random_name = ''.join(random.choice(string.ascii_letters + string.digits) for n in range(12))

                # Resize original image (640x1280)
                image.thumbnail((640, 1280), Image.ANTIALIAS)
                temp_handle_original = StringIO()
                image.save(temp_handle_original, pil_type, quality=80)
                temp_handle_original.seek(0)
                suf_original = SimpleUploadedFile(image_random_name, temp_handle_original.read(), content_type=content_type)
                self.thumbnail.save(
                    '%s.%s' % (os.path.splitext(suf_original.name)[0], file_extension),
                    suf_original,
                    save=False
                )

                # Create thumbnail (300x300)
                image.thumbnail((300, 300), Image.ANTIALIAS)
                temp_handle_thumb = StringIO()
                image.save(temp_handle_thumb, pil_type, quality=90)
                temp_handle_thumb.seek(0)
                suf = SimpleUploadedFile(image_random_name, temp_handle_thumb.read(), content_type=content_type)
                self.event_thumb.save(
                    '%s_300x300.%s' % (os.path.splitext(suf.name)[0], file_extension),
                    suf,
                    save=False
                )

    def save(self, *args, **kwargs):

        self.create_resized_images()

        force_update = False
        if self.id:
            force_update = True

        super(Event, self).save(force_update=force_update)

    def event_thumbnail(self):
        if self.event_thumb:
            return image_preview(self.event_thumb)
        return image_preview(self.thumbnail)

    event_thumbnail.allow_tags = True
    event_thumbnail.short_description = "Current event thumbnail"


def upload_event_media_file(instance, filename):
    path = "events_media/"
    upload_path = set_file_path(filename, path)
    return upload_path


class EventMediaManager(models.Manager):
    def published(self, **kwargs):
        return self.filter(is_published=True, **kwargs).order_by('-pk')


class EventMediaData(models.Model):
    event = models.ForeignKey(Event)

    media = models.ImageField(
        verbose_name=u"Event Media",
        upload_to='events_media/'
    )

    media_medium = models.ImageField(
        u"Event Media medium",
        upload_to='events_media/medium/',
        blank=True,
        null=True
    )

    media_thumb = models.ImageField(
        u"Event Media thumbnail",
        upload_to='events_media/thumbs/',
        blank=True,
        null=True
    )

    media_title = models.CharField(
        u"Event media item title",
        max_length=500,
        blank=True,
        null=True
    )

    is_video = models.BooleanField(default=False)

    video_link = models.CharField(
        u"Link on event video",
        max_length=500,
        blank=True,
        null=True
    )

    enlarged_thumbnail_size = models.BooleanField(
        default=False,
        help_text="Set enlarged thumbnail image.",
    )

    is_published = models.BooleanField(default=True)

    objects = EventMediaManager()

    def save(self, *args, **kwargs):
        if not self.media:
            return

        image = Image.open(StringIO(self.media.read()))

        if hasattr(self.media.file, 'content_type'):
            content_type = self.media.file.content_type
            if content_type == 'image/jpeg':
                pil_type = 'jpeg'
                file_extension = 'jpg'
            elif content_type == 'image/png':
                pil_type = 'png'
                file_extension = 'png'

            image_random_name = ''.join(random.choice(string.ascii_letters + string.digits) for n in range(12))

            # Resize original image (1280x1280) if size > 150KB
            image.thumbnail((1280, 1280), Image.ANTIALIAS)
            temp_handle_original= StringIO()
            if self.media.size > 180000:
                image.save(temp_handle_original, pil_type, quality=90)
            else:
                image.save(temp_handle_original, pil_type)
            temp_handle_original.seek(0)
            suf_original = SimpleUploadedFile(image_random_name, temp_handle_original.read(), content_type=content_type)
            self.media.save(
                '%s.%s' % (os.path.splitext(suf_original.name)[0], file_extension),
                suf_original,
                save=False
            )

            # Create medium thumbnail (640x1280)
            image.thumbnail((640, 1280), Image.ANTIALIAS)
            temp_handle_medium = StringIO()
            image.save(temp_handle_medium, pil_type, quality=80)
            temp_handle_medium.seek(0)
            suf_medium = SimpleUploadedFile(image_random_name, temp_handle_medium.read(), content_type=content_type)
            self.media_medium.save(
                '%s_640x1280.%s' % (os.path.splitext(suf_medium.name)[0], file_extension),
                suf_medium,
                save=False
            )

            # Create thumbnail (200x200)
            image.thumbnail((200, 200), Image.ANTIALIAS)
            temp_handle_thumb = StringIO()
            image.save(temp_handle_thumb, pil_type, quality=90)
            temp_handle_thumb.seek(0)
            suf = SimpleUploadedFile(image_random_name, temp_handle_thumb.read(), content_type=content_type)
            self.media_thumb.save(
                    '%s_200x200.%s' % (os.path.splitext(suf.name)[0], file_extension),
                    suf,
                    save=False
                )

        force_update = False
        if self.id:
            force_update = True

        super(EventMediaData, self).save(force_update=force_update)

    def extension(self):
        name, extension = os.path.splitext(self.media.name)
        return extension

    def media_file(self):
        if self.media_thumb:
            return image_preview(self.media_thumb)
        return image_preview(self.media)

    def original_file_info(self):
        file_size = get_file_size(self.media)
        file_size2 = self.media.size
        dimension = "%sx%s" % (self.media.width, self.media.height)
        # return "%s\n%s\n%s" % (file_size2, file_size, dimension)
        return "%s\n%s" % (file_size, dimension)

    def medium_file_info(self):
        file_size = get_file_size(self.media_medium)
        dimension = "%sx%s" % (self.media_medium.width, self.media_medium.height)
        return "%s\n%s" % (file_size, dimension)

    media_file.allow_tags = True
    media_file.short_description = "Current image"
    original_file_info.short_description = "Original file info"
    medium_file_info.short_description = "Medium file info"

    class Meta:
        verbose_name = u"Event media"
        verbose_name_plural = u"Event media"