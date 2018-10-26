'''Models for the agenda app'''

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from groups.models import Group
from accounting.models import Transaction


class TimeRange(models.Model):
    '''A time range is defined by its beginning and its duration.'''
    date = models.DateTimeField()
    duration = models.DurationField()

    def __repr__(self):
        #return "Begins at {}, lasts {}".format(self.date, self.duration)
        return "Between {} and {} ( lasts {} )".format(self.date,(self.date+self.duration), self.duration)


class Event(models.Model):
    '''An event is created by a person, and has a group of person attending it.
    If the subsequent group is deleted (which should not happen unless the event is being deleted),
    the event is automatically deleted.
    It has administrators (at least one). In the case where the last administrator is deleted,
    all members become administrators.
    If the creator is deleted, the event remains and the creator is set to NULL.'''
    date = models.DateTimeField()
    place = models.CharField(max_length=500, blank=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    administrators = models.ManyToManyField(User, related_name='+')
    attendees = models.ForeignKey(Group, on_delete=models.CASCADE)
    invited = models.ManyToManyField(User, related_name='+')
    # why is attendees a group and invited a ManyToManyField...?

    def get_transaction_list(self):
        '''Give the list of the transactions in the event.'''
        return self.transactionforevent_get.all()


class TransactionForEvent(Transaction):
    '''A transaction that was made for a certain event'''

    def validate_transac_event(self, event):
        '''Checks that all the beneficiaries of the transaction did attend the event.'''
        try:
            att = event.attendees.members.all()
            ben = self.beneficiaries.all()
            for beneficiary in ben:
                assert beneficiary in att
            return event

        except:
            message = "Some beneficiaries of a TransactionForEvent don't attend the event."
            raise ValidationError(message)


    event = models.ForeignKey(Event, on_delete=models.PROTECT, \
        validators=[validate_transac_event])


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
