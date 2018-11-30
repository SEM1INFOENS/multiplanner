from django.urls import path

from . import views

app_name = 'relationships'

urlpatterns = [
    path('user-search', views.user_search, name='user-search'),
    path('', views.friends, name='friends'),
    path('friendship_request/', views.friendship_request, name='friendship_request'),
]



