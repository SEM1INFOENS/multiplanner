from django.urls import path

from . import views

app_name = 'permissions'

urlpatterns = [
    path('manage_app_admins', views.manage_app_admins, name='manage_app_admins'),
]
