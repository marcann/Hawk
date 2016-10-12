from django.shortcuts import render, get_object_or_404
from datetime import datetime, date
from calendar import monthrange
from .models import Event, Venue, Guest
from django.utils import timezone
from django.core import serializers
from django.http import HttpResponse
from django.forms.formsets import formset_factory
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import EventForm, GuestForm, EventDeleteForm

def named_month(month_number):
    """
    Return the name of the month, given the number.
    """
    return date(1900, month_number, 1).strftime("%B")

def this_month(request):
    """
    Show calendar of events this month.
    """
    today = timezone.now()
    return calendar(request, today.year, today.month)

def calendar(request, year, month, series_id=None):
    """
    Show calendar of events for a given month of a giver year.
    ''series_id''
    The event series to show. None will shoe all event series.
    """

    my_year = int(year)
    my_month = int(month)
    my_calendar_from_month = datetime(my_year, my_month, 1)
    my_calendar_to_month = datetime(my_year, my_month, monthrange(my_year, my_month)[1])

    my_events = Event.objects.filter(date_and_time__gte=my_calendar_from_month).filter(date_and_time__lte=my_calendar_to_month)
    if series_id:
        my_events = my_events.filter(series=series_id)

    # Calculate values for the calendar controls. 1-indexed (Jan = 1)
    my_previous_year = my_year
    my_previous_month = my_month - 1
    if my_previous_month == 0:
        my_previous_year = my_year - 1
        my_previous_month = 12
    my_next_year = my_year
    my_next_month = my_month + 1
    if my_next_month == 13:
        my_next_year = my_year + 1
        my_next_month = 1
    my_year_after_this = my_year + 1
    my_year_before_this = my_year - 1
    return render(request, "game_calendar/calendar.html", {'events_list': my_events,
                                            'month': my_month,
                                            'month_name': named_month(my_month),
                                            'year': my_year,
                                            'previous_month': my_previous_month,
                                            'previous_month_name': named_month(my_previous_month),
                                            'previous_year': my_previous_year,
                                            'next_month': my_next_month,
                                            'next_month_name': named_month(my_next_month),
                                            'previous_year': my_previous_year,
                                            'next_year': my_next_year,
    })

def event_list(request):
    events = Event.objects.filter(date_and_time__lte=timezone.now()).order_by('date_and_time')
    return render(request, 'game_calendar/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    json_event = serializers.serialize("json", Event.objects.filter(pk=pk))
    json_venues = serializers.serialize("json", Venue.objects.all())
    return render(request, 'game_calendar/event_detail.html', {'event': event, 'json_event': json_event, 'json_venues': json_venues})

@login_required
def event_new(request):
    form = EventForm()
    return render(request, 'game_calendar/event_new.html', {'form': form})
    # TODO:20 Make event save when submitted. Added created_date attribute which will need to be saved here.
    # DONE:40 Add a list of events as part of the base of the site.

@login_required
def event_edit(request, pk):

    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        event_form = EventForm(request.POST)

        if event_form.is_valid():
            # Save Event Info
            event.title = event_form.cleaned_data.get('title')
            event.description = event_form.cleaned_data.get('description')
            event.date_and_time = event_form.cleaned_data.get('date_and_time')
            event.venue = event_form.cleaned_data.get('venue')
            event.category = event_form.cleaned_data.get('category')
            event.price = event_form.cleaned_data.get('price')
            event.email_subject = event_form.cleaned_data.get('email_subject')
            event.email_message = event_form.cleaned_data.get('email_message')
            event.save()

    else:
        event_form = EventForm(instance=event)

    context = {
        'event_form': event_form,
        'event': event,
    }


    return render(request, 'game_calendar/event_edit.html', context)

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventDeleteForm(request.POST, instance=event)
        if form.is_valid():
            event.delete()
            return HttpResponseRedirect('/')
    else:
        form = EventDeleteForm(instance=event)

    return render(request, 'game_calendar/event_delete.html', {'form': form, 'event': event})
