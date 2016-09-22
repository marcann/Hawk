from django.contrib import admin
from .models import Venue, Category, Event, Guest

admin.site.register(Venue)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Guest)
