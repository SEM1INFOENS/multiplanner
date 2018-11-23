from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('users/<str:username>/', views.page, name='page')
]
