from django.conf.urls import url
from . import views

urlspatterns = [
    url(r'^$', views.post_list, name='post_list'),
]
