from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views

urlpatterns = [
    path('new-event', views.create_event, name='new-event'),
    #url(r'^admin/jsi18n', 'django.views.i18n.javascript_catalog'),
]
