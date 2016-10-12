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

class EventDeleteForm(forms.ModelForm):

    confirm = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Confirm Delete")

    class Meta:
        model = Event
        fields = ('confirm',)

    def clean(self):
        keyword = "delete"
        if (self.cleaned_data['confirm'].lower() != keyword):
            raise forms.ValidationError("Did not type in proper keyword.")
        return self.cleaned_data


# TODO:10 Make custom widget for date_and_time field in Event.
# TODO:0 Look into why guests are not appearing on the edit page with current implamentation / Look into new solutions.
