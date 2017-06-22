from django.conf.urls import url
from . import views

app_name = 'ac'
urlpatterns = [
    url(r'^start/(?P<config_id>[0-9]+)/$', views.start_server),
    url(r'^stop/(?P<config_id>[0-9]+)/$', views.stop_server),
]
