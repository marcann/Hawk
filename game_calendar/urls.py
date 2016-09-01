from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.this_month, name='calendar'),
    url(r'^(?P<pk>\d+)/$', views.event_detail, name='event_detail'),
]
