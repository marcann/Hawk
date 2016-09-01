from django.shortcuts import render
from game_calendar.models import Event
from django.utils import timezone


def get_event_lists(request):
    today = timezone.now()
    events_future = Event.objects.order_by('date_and_time').filter(date_and_time__gte=today)
    events_past = Event.objects.order_by('date_and_time').filter(date_and_time__lte=today).reverse()
    return {'events_future': events_future,
            'events_past': events_past}
