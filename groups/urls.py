from django.urls import include, path
from django.conf.urls import url


from . import views
app_name = 'groups'
urlpatterns = [
	path('',views.showGroups,name = 'groups'),
	path('new-group', views.create_group, name='new-group'),
	url(r'^edit-group/(?P<ide>[0-9]+)$', views.edit_group, name='edit-group'),
	url(r'^group/(?P<ide>[0-9]+)$', views.group_number, name='group-number'),
    path('group/<int:ide>/invites', views.group_invites, name='group-invites'),  
]
