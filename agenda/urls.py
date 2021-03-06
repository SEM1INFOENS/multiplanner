from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views

urlpatterns = [
    path('calendar.ics', views.generate_calendar),
    path('new-event', views.create_event, name='new-event'),
    path('', views.agenda, name='agenda'),
    url(r'^event/(?P<ide>[0-9]+)$', views.event, name='event'),
    url(r'^edit-event/(?P<ide>[0-9]+)$', views.edit_event, name='edit-event'),
    path('invitation_answer/', views.invitation_answer, name='invitation_answer'),
    path('new_sitting', views.new_sitting, name='new_sitting'),
    #url(r'^admin/jsi18n', 'django.views.i18n.javascript_catalog'),
]



