from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.register, name='register'),
    url(r'^register_success$', views.register_success, name='register_success'),
]
