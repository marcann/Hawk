from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.this_month, name='calendar_today'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', views.calendar, name='calendar'),
    url(r'^event/(?P<pk>\d+)/$', views.event_detail, name='event_detail'),
    url(r'^event/new/$', views.event_new, name='event_new'),
    url(r'^event/(?P<pk>\d+)/edit/$', views.event_edit, name='event_edit'),
]
