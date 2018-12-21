# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from .models import Event, EventMediaData


def events_list(request):
    future_events = Event.objects.future_events()
    past_events = Event.objects.past_events()

    return render(request, 'event/events_list.html', {'future_events': future_events, 'past_events': past_events})


def event_detail(request, event_slug=''):

    event_data = Event.objects.get(slug=event_slug)
    event_media = EventMediaData.objects.filter(event=event_data, is_published=True)
    other_events = Event.objects.published().exclude(slug=event_slug)

    return render(request, 'event/event_detail.html', {'event': event_data, 'event_media': event_media, 'other_events': other_events})
