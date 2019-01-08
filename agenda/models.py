'''Models for the agenda app'''

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import datetime as datetime_module
from groups.models import Group
from accounting.models import Transaction
from django.core.exceptions import SuspiciousOperation, ValidationError
from . import sit
from permissions.shortcuts import *



class TimeRange(models.Model):
    '''A time range is defined by its beginning and its duration.'''
    date = models.DateTimeField()
    duration = models.DurationField()

    @classmethod
    def create_new(cls, dateTR, durationTR):
        '''Creates a Time Range starting at dateTR with duration durationTR'''
        tr = cls(date=dateTR, duration=durationTR)
        return tr

    def __repr__(self):
        #return "Begins at {}, lasts {}".format(self.date, self.duration)
        return "Between {} and {} ( lasts {} )".format(self.date, (self.date+self.duration), \
            self.duration)


def combine(date, time, default_time):
    if time == None:
        t = datetime_module.time(*default_time)
    else: t = time
    return datetime_module.datetime.combine(date, t)


class EventManager(models.Manager):
    @classmethod
    def invited(self, user):
        '''List the futur events to which the user is invited'''
        return Event.objects.filter( date__gte=timezone.now(), invited__members=user).exclude(attendees__members__members=user).order_by('creation_date')

    @classmethod
    def attending(self, user):
        '''List the futur events to which the user will attend'''
        return Event.objects.filter( date__gte=timezone.now(), attendees__members__members=user).order_by('time','date').order_by('date')

    @classmethod
    def past_invited(self, user):
        '''List the past events to which the user was invited'''
        return Event.objects.filter( date__lt=timezone.now(), invited__members=user).exclude(attendees__members__members=user).order_by('-date_end')

    @classmethod
    def past_attending(self, user):
        '''List the past events to which the user has attend'''
        return Event.objects.filter( date__lt=timezone.now(), attendees__members__members=user).order_by('-date_end')

    @classmethod
    def past(self, user):
        '''List the past events to which the user was invited or has attended'''
        return Event.objects.filter( date__lt=timezone.now(), invited__members=user).order_by('-date_end')


class Event(models.Model):
    '''An event is created by a person, and has a group of person attending it.
    If the subsequent group is deleted (which should not happen unless the event is being deleted),
    the event is automatically deleted.
    It has administrators (at least one). In the case where the last administrator is deleted,
    all members become administrators.
    If the creator is deleted, the event remains and the creator is set to NULL.'''

    objects = EventManager()

    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(default=timezone.now)
    description = models.CharField(blank=True, max_length=1000)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    default_time = (8,)
    def date_time(self): return combine(self.date, self.time, self.default_time)

    date_end = models.DateField()
    time_end = models.TimeField(blank=True, null=True)
    default_time_end = (19,)
    def date_time_end(self): return combine(self.date_end, self.time_end, self.default_time_end)

    place = models.CharField(max_length=500, blank=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    invited = models.OneToOneField(PermGroup, on_delete=models.CASCADE, related_name='+')
    admins = models.OneToOneField(PermGroup, on_delete=models.CASCADE, related_name='+')
    attendees = models.OneToOneField(Group, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    # why is attendees a group and invited a ManyToManyField...? Because attendees will do things
    # together, it makes sense to consider them as a group.
    # transactions = models.ManyToManyField(Transaction) => use the transactions field of the Group instead

    @classmethod
    def create_new(cls, date, time, date_end, time_end, creator, place='',\
     admins=[], invited=[], attendees=None, public=False, commit=True):
        '''Default method for creating an event
        if public=True, then everyone can see the event
        otherwise only members and invited
        if commit=False then the returnd object is not saved in the db'''
        event = cls(date=date, time=time, date_end=date_end, time_end=time_end, place=place, \
            creator=creator, public=public)
        if attendees==None:
            event.attendees = Group.create_for_event()
        else:
            event.attendees = attendees
        event.admins = PermGroup.create_new(admins)
        event.invited = PermGroup.create_new(invited)
        if commit:
            event.save()
        return event

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # the instance has to be save to set permissions :
        set_admin_perm(self, self.admins)
        set_members_perm(self, self.invited, public=self.public)

    def __repr__(self):
        '''Enables to display an event in a convenient way.'''
        return "date : {}, place : {}, creator : {}, admins : {}, attendees : {}, \
        invited : {}".format(self.date, self.place, self.creator, \
            self.admins, self.attendees, self.invited)

    def __str__(self):
        '''Function used when str(object) is called.
        Also used in the admin interface'''
        return '%s (%s)' % (self.name, str(self.date))

    def get_absolute_url(self):
        return reverse('event', args=(str(self.id),))

    def clean(self):
        ''' don't allow begin_date greater than end_date '''
        if self.date_time() > self.date_time_end():
            raise ValidationError("Event can't end before it has begun")

    def is_over(self):
        return self.date_time_end()<timezone.now()
    def has_begun(self):
        return self.date_time()<=timezone.now()

    def can_accept_invite(self, user):
        ''' to accept an invitation, the event must not be over'''
        return not ((user not in self.invited.all()) or (user in self.attendees.members.all()) or self.is_over())
    #TODO: maby we could have an end of inscription date ?
    def accept_invite(self, user):
        if self.can_accept_invite(user):
            self.attendees.members.add(user)
        else: raise SuspiciousOperation
    def decline_invite(self, user):
        if self.can_accept_invite(user):
            self.invited.remove(user)
        else: raise SuspiciousOperation

    def can_cancel_acceptance(self, user):
        ''' to cancel the comming to an event, the event must not have begun'''
        return not((user not in self.invited.all()) or (user not in self.attendees.members.all()) or self.has_begun())
    def cancel_acceptance(self, user):
        if self.can_cancel_acceptance(user):
            self.attendees.members.remove(user)
        else: raise SuspiciousOperation


class Sitting(models.Model):
    event = models.OneToOneField(Event, primary_key=True, on_delete=models.CASCADE)

    @classmethod
    def set_new(self,event, tables):
        try :
            old_s = event.sitting
            old_s.delete()
        except Sitting.DoesNotExist:
            pass
        try:
            optimal_s = sit.sitting(event, tables)
        except ValueError:
            return False
        s_obj = Sitting(event=event)
        s_obj.save()
        tables_obj = {}
        for i in range(len(tables)):
            t = Table(sitting=s_obj)
            t.save()
            tables_obj[i] = t
        if optimal_s != None:
            for user, i in optimal_s.items():
                tables_obj[i].members.add(user)
        return True

class Table(models.Model):
    sitting = models.ForeignKey(Sitting, unique=False, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, blank=True)


class MeetingRules(models.Model):
    '''A set of rules which creates events.
    They are created by a person, set to NULL if this person should be deleted.
    It has administrators (at least one). In the case where the last administrator is deleted,
    all members become administrators.'''
    minimum_delay = models.DurationField()
    maximum_delay = models.DurationField()
    duration = models.DurationField()
    possible_time_ranges = models.ManyToManyField(TimeRange)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    administrators = models.ManyToManyField(User, related_name='+')

    @classmethod
    def create_new(cls, minimum_delay, maximum_delay, duration, possible_time_ranges, \
        creator, administrators):
        '''Default method for creating a set of meeting rules'''
        meeting = cls(minimum_delay=minimum_delay, maximum_delay=maximum_delay, duration=duration, \
            creator=creator)
        meeting.save()
        meeting.administrators.add(*administrators)
        meeting.possible_time_ranges.add(*possible_time_ranges)
        return meeting

    def __repr__(self):
        '''Enables to display meeting rules in a convenient way.'''
        return "minimum_delay : {}, maximum_delay : {}, duration : {}, possible_time_ranges : {}, \
        creator : {}, administrators : {}".format(self.minimum_delay, self.maximum_delay, \
            self.duration, self.possible_time_ranges, self.creator, self.administrators)
