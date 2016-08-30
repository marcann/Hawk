from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.game_calendar, name='game_calendar'),
]
