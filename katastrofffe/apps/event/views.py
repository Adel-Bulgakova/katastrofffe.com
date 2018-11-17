# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from .models import Event


def events_list(request):
    events = Event.objects.published()

    return render(request, 'event/events_list.html', {'events': events})


def event_detail(request, event_slug=''):

    event_data = Event.objects.get(slug=event_slug)
    other_events = Event.objects.published().exclude(slug=event_slug)

    return render(request, 'event/event_detail.html', {'event': event_data, 'other_events': other_events})
