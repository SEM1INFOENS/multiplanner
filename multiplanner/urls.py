"""multiplanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url


from . import views

urlpatterns = [
    #path('', views.index),
    path('', include('presentation.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('presentation.urls', namespace='users')),
    path('agenda/', include('agenda.urls')),
    #url(r'^friends/', include(('relationships.urls', 'friends'), namespace='friends')),
    url(r'^friends/', include('relationships.urls', namespace='friends')),
    #    url(r'^friendship/', include('friendship.urls')),
]
