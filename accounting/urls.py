from django.urls import include, path

from . import views
app_name = 'accounting'
urlpatterns = [
	path('',views.showGroups,name = 'groups'),
]
