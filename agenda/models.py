from django.db import models
from group.models import Group


class TimeRange(models.Model):
    '''A time range is defined by its beginning and its duration.'''
    date = models.DateTimeField()
    duration = models.DurationField()

    def __repr__(self):
        return "Begins at {}, lasts {}".format(self.date, self.duration)


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

