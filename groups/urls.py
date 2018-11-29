from django.urls import include, path

from . import views
app_name = 'groups'
urlpatterns = [
	path('',views.showGroups,name = 'groups'),
	path('new-group', views.create_group, name='new-group'),
	path('event/(?P<ide>[0-9]+)$', views.groups_number, name='groups-number'),
  
]
