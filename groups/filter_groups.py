''' Filtering functions for groups '''
from django.db import models
from django.contrib.auth.models import User
from .models import *
from agenda.models import *

def all_groups_of_user (user):
	return Group.objects.filter(members = user).order_by('name')


def groups_not_in_events ():
	pass
#	att = Event.objects.all()
#	for i in att:
#		i.attendees
#	return Group.objects.difference(att)

def groups_of_user(user) :
#	return groups_not_in_events().filter(members = user).order_by('name')
	return Group.objects.filter(members = user).order_by('name')
	
