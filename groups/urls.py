from django.urls import include, path

from . import views
app_name = 'groups'
urlpatterns = [
	path('',views.showGroups,name = 'groups'),
]
