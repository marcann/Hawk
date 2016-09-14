from django.db import models
from django.conf import settings
from django.utils import timezone
from .helpers import get_lat, get_lng

# models

class Venue(models.Model):
    # Describes the venues, location #
    name = models.CharField("Name", max_length=50)
    full_address = models.CharField(blank=True, max_length=100)
    street_address = models.CharField("Street Address", max_length=50)
    city = models.CharField("City", max_length=20, default="Montreal")
    country = models.CharField("Country", max_length = 20, default="Canada")
    province = models.CharField("Province", max_length=2, default="QC")
    postal_code = models.CharField("Postal Code", max_length=6)
    lat = models.CharField(blank=True, max_length=50)
    lng = models.CharField(blank=True, max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = "Venue"
        verbose_name_plural = "Venues"
        ordering = ['name']

    def __str__(self):
        return self.name

    def _get_display_address(self):
        return ", ".join([self.street_address, self.city, self.province, self.postal_code])
    full_address = property(_get_display_address)

    def _get_geocode(self):
        return "%s" % ( self.postal_code)
    geo_address = property(_get_geocode)

    def save(self, *args, **kwargs):
        if not (self.lat and self.lng):
            if self.postal_code:
                location = self.geo_address
                self.lat = get_lat(location)
                self.lng = get_lng(location)
            else:
                location = '+'.join(filter(None, (self.address, self.city, self.province, self.country)))
                self.lat = get_lat(location)
                self.lng = get_lng(location)
        super(Venue, self).save(*args, **kwargs)


class Category(models.Model):
    # Different types of events (or sports) #
    name = models.CharField("Name", max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

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
