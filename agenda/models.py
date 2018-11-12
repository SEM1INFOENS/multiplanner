'''Models for the agenda app'''

from django.db import models
from django.contrib.auth.models import User
#from django.core.exceptions import ValidationError
from groups.models import Group
from accounting.models import Transaction
from relationships.models import SecretMark

from treasuremap.fields import LatLongField


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


class Event(models.Model):
    '''An event is created by a person, and has a group of person attending it.
    If the subsequent group is deleted (which should not happen unless the event is being deleted),
    the event is automatically deleted.
    It has administrators (at least one). In the case where the last administrator is deleted,
    all members become administrators.
    If the creator is deleted, the event remains and the creator is set to NULL.'''
    name = models.CharField(max_length=100)
    description = models.CharField(blank=True, max_length=1000)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    place = LatLongField(blank=True, null=True)
    #place = models.CharField(max_length=500, blank=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    administrators = models.ManyToManyField(User, related_name='+')
    attendees = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE)
    invited = models.ManyToManyField(User, related_name='+')
    # why is attendees a group and invited a ManyToManyField...? Because attendees will do things
    # together, it makes sense to consider them as a group.
    transactions = models.ManyToManyField(Transaction, blank=True)


    @classmethod
    def create_new(cls, date, place, creator, administrators, attendees, invited, transactions):
        '''Default method for creating an event'''
        event = cls(date=date, place=place, creator=creator, attendees=attendees)
        event.save()
        event.administrators.add(*administrators)
        event.invited.add(*invited)
        event.transactions.add(*transactions)
        return event

    def __repr__(self):
        '''Enables to display an event in a convenient way.'''

        return "date : {}, place : {}, creator : {}, administrators : {}, attendees : {}, \
        invited : {}, transactions : {}".format(self.date, self.place, self.creator, \
            self.administrators, self.attendees, self.invited, self.transactions)

    def __str__(self):
        '''Function used when str(object) is called.
        Also used in the admin interface'''
        return '%s (%s)' % (self.name, str(self.date))

    def relationship_matrix(self):
        '''Returns M matrix of size n*n with n the number of attendees
        with M[i][j] the secrete mark i gave j, 0 if no such mark exists'''
        list_att = self.attendees.members.all()
        n = len(list_att)

        M = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            # I cannot find a way to do it without two loops, because a mark is between user1 
            # and user2 and I don't find a way to know the number of user2 without being as 
            # long as with a loop
            for j in range(n):
                try:
                    M[i][j] = SecretMark.objects.get(user=list_att[i], marked_user=list_att[j])
                except SecretMark.DoesNotExist:
                    ()
        return M


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
