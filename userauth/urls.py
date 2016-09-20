from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register$', views.register, name='register'),
    url(r'^register_success$', views.register_success, name='register_success'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^login_success$', views.login_success, name='login_success'),
    url(r'^logout_success$', views.logout_success, name='logout_success'),
    url(r'^logout$', views.logout_view, name='logout')
]
