from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def validate_amount(value):
    '''Checks that the amount is positive and returns a float which has less than two
    figures after the comma.'''
    try:
        assert value >= 0.0
        return round(float(value), 2)
    except:
        raise ValidationError(
            _('%(value)s is neither a positive integer nor a float  number'),
            params={'value': value},
        )

# def to_choices(l):
#     '''Checks that every element is a string and [x, y, ...] returns [(x, x), (y,y), ...] to be
#     in adequation with choices's requirements'''
#     out = []
#     for s in l:
#         assert isinstance(s, str)
#         out.append((s, s))
#     return out


class TimeRange(models.Model):
    '''A time range is defined by its beginning and its duration.'''
    date = models.DateTimeField()
    duration = models.DurationField()

    def __repr__(self):
        return "Begins at {}, lasts {}".format(self.date, self.duration)


class Group(models.Model):
    '''A group of people, inside which transactions can be made.
    To make transactions in an event, people will make transactions in the subsequent group.
    '''
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)


class Transaction(models.Model):
    '''One person gives money to one or more members of a group.

    Be careful! If the expeditor of the transaction is deleted, the transaction they made as well.
    If the group is deleted, the transactions in it are deleted as well.
    '''
    motive = models.CharField(max_length=1000)
    date = models.DateTimeField()
    expeditor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(validators=[validate_amount])
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Event(models.Model):
    '''An event is created by a person, and has a group of person attending it.
    If the subsequent group is deleted (which should not happen unless the event is being deleted),
    the event is automatically deleted.
    It has administrators (at least one). In the case where the last administrator is deleted,
    all members become administrators.
    If the creator is deleted, the event remains and the creator is set to NULL.'''
    date = models.DateTimeField()
    place = models.CharField(max_length=500, blank=True)
    #place specification could be better: GPS coordonates...?
    creator = models.ForeignKey(User, on_delete=models.SET_NULL)
    administrators = models.ManyToManyField(User) 
    attendees = models.ForeignKey(Group, on_delete=models.CASCADE)
    invited = models.ManyToManyField(User)


class MeetingRules(models.Model):
    '''A set of rules which creates events.
    They are created by a person, set to NULL if this person should be deleted.
    It has administrators (at least one). In the case where the last administrator is deleted,
    all members become administrators.'''
    minimum_delay = models.DurationField()
    maximum_delay = models.DurationField()
    duration = models.DurationField()
    possible_time_ranges = models.ManyToManyField(TimeRange)
    creator = models.ForeignKey(User, on_delete=SET_NULL)
    administrators = models.ManyToManyField(User)


class Friendships(models.Model):
    '''Friendships is an extension for Users which adds a list of friends and a list of invited
    friends. It is symmetrical.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend_list = models.ManyToManyField(User)
    invited_list = models.ManyToManyField(User)
    

class SharedAccount(models.Model):
    '''A shared account is for a group of people that pay together.
    A shared account is not needed unless there are two or more persons in it.'''
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)
