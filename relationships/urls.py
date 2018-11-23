from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views

app_name = 'relationships'

urlpatterns = [
    url(r'^user-search', views.user_search, name='user-search'),
    path('add/<str:to_username>', views.add, name='add'),
]



