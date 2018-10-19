'''Models for the groups app'''

from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    '''A group of people, inside which transactions can be made.
    To make transactions in an event, people will make transactions in the subsequent group.
    '''
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)
