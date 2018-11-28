'''Models for the agenda app'''

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime as datetime_module
#from django.core.exceptions import ValidationError
from groups.models import Group
from accounting.models import Transaction
from django.core.exceptions import SuspiciousOperation
#from treasuremap.fields import LatLongField



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

class Event(models.Model):
    '''An event is created by a person, and has a group of person attending it.
    If the subsequent group is deleted (which should not happen unless the event is being deleted),
    the event is automatically deleted.
    It has administrators (at least one). In the case where the last administrator is deleted,
    all members become administrators.
    If the creator is deleted, the event remains and the creator is set to NULL.'''
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

    #place = LatLongField(blank=True, null=True)
    place = models.CharField(max_length=500, blank=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    administrators = models.ManyToManyField(User, related_name='+')
    attendees = models.OneToOneField(Group, on_delete=models.CASCADE)
    invited = models.ManyToManyField(User, related_name='+')
    # why is attendees a group and invited a ManyToManyField...? Because attendees will do things
    # together, it makes sense to consider them as a group.
    # transactions = models.ManyToManyField(Transaction) => use the transactions field of the Group instead


    @classmethod
    def create_new(cls, date, time, date_end, time_end, place, creator, administrators, attendees, invited):
        '''Default method for creating an event'''
        event = cls(date=date, time=time, date_end=date_end, time_end=time_end, place=place, \
            creator=creator, attendees=attendees)
        event.save()
        event.administrators.add(*administrators)
        event.invited.add(*invited)
        return event

    def __repr__(self):
        '''Enables to display an event in a convenient way.'''

        return "date : {}, place : {}, creator : {}, administrators : {}, attendees : {}, \
        invited : {}".format(self.date, self.place, self.creator, \
            self.administrators, self.attendees, self.invited)

    def __str__(self):
        '''Function used when str(object) is called.
        Also used in the admin interface'''
        return '%s (%s)' % (self.name, str(self.date))

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

    def can_cancel_acceptance(self, user):
        ''' to cancel the comming to an event, the event must not have begun'''
        return not((user not in self.invited.all()) or (user not in self.attendees.members.all()) or self.has_begun())
    def cancel_acceptance(self, user):
        if self.can_cancel_acceptance(user):
            self.attendees.members.remove(user)
        else: raise SuspiciousOperation


# class TransactionForEvent(Transaction):
#     '''A transaction that was made for a certain event'''
#     def validate_transac_event(self, event):
#         '''Checks that all the beneficiaries of the transaction did attend the event.'''
#         try:
#             att = event.attendees.members.all()
#             ben = self.beneficiaries.all()
#             for beneficiary in ben:
#                 assert beneficiary in att
#             return event
#         except:
#             message = "Some beneficiaries of a TransactionForEvent don't attend the event."
#             raise ValidationError(message)
#     event = models.ForeignKey(Event, on_delete=models.PROTECT, \
#         validators=[validate_transac_event])


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
