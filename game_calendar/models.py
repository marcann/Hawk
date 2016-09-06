from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# models

class Venue(models.Model):
    # Describes the venues, location #
    name = models.CharField("Name", max_length=50)
    address = models.CharField("Address", max_length=50)
    description = models.TextField("Description")
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = "Venue"
        verbose_name_plural = "Venues"
        ordering = ['name']

    def __str__(self):
        return self.name

class Category(models.Model):
    # Different types of events (or sports) #
    name = models.CharField("Name", max_length=50)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Event(models.Model):
    # Any event that doesn't span over various day. Comments are used internally,#
    # not meant for publication.#
    title = models.CharField("Title", max_length=50)
    description = models.TextField("Description")
    comments = models.TextField("Comments")
    date_and_time = models.DateTimeField("Date and time")
    price = models.CharField(default="Free", max_length=50)
    venue = models.ForeignKey(Venue)
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['date_and_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('event_detail', args=[self.pk])


# TODO:0 extend the Event model for DWHL Hockey game which allows the storing of scores, locations and comments.
