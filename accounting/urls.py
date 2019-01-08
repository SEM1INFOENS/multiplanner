from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views
app_name = 'accounting'
urlpatterns = [
    path('transaction-details/<int:ide>', views.transaction_details, name='transaction-details'),
]
