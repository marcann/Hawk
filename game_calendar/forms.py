from django import forms
from django.forms.formsets import BaseFormSet
from .models import Event, Venue, Category, Guest
from userauth.models import CustomUser

class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super(EventForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Event
        fields = ('title', 'description', 'date_and_time', 'price',
        'venue', 'category', 'email_subject', 'email_message',)


#class VenueForm:


#class CategoryForm:


class GuestForm(forms.Form):

    class Meta:
        model = Guest

# TODO Make custom widget for date_and_time field in Event.
# TODO Look into why guests are not appearing on the edit page with current implamentation / Look into new solutions.
