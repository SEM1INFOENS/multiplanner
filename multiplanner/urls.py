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


urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('', include('presentation.urls', namespace='users')),
    path('admin/', admin.site.urls),
    path('agenda/', include('agenda.urls')),
    path('groups/', include('groups.urls', namespace='groups')),
    path('friends/', include('relationships.urls', namespace='friends')),
    path('accounting/', include('accounting.urls')),
    path('permissions/', include('permissions.urls')),
    url(r'^notifications/', include('notify.urls', 'notifications')),
]
