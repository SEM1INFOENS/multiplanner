'''Models for the groups app'''

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import SuspiciousOperation
#from django.core.exceptions import ValidationError
from django.urls import reverse
from djmoney.models.fields import MoneyField, CurrencyField
from djmoney.settings import CURRENCY_CHOICES, DEFAULT_CURRENCY
from accounting.models import Transaction
from permissions.models import PermGroup
from relationships.models import SecretMark
from permissions.shortcuts import *
from django.urls import reverse
from djmoney.models.fields import MoneyField, Money
from permissions.shortcuts import assign_user_view_perm, remove_user_view_perm

class GroupManager(models.Manager):

    @classmethod
    def all(self):
        return Group.objects.filter(inEvent=False)

    @classmethod
    def containsUser(self, user):
        return Group.objects.filter(inEvent=False, members__members=user)


class Group(models.Model):
    '''A group of people, inside which transactions can be made.
    To make transactions in an event, people will make transactions in the subsequent group.
    '''
    objects = GroupManager()
    _choices = (('USD','US Dollar'),('EUR','Euro'),('RUB','Russian Ruble'))

    name = models.CharField(max_length=200, blank=True)
    members = models.OneToOneField(PermGroup, on_delete=models.CASCADE, related_name='+')
    admins = models.OneToOneField(PermGroup, null=True, blank=True, on_delete=models.CASCADE, related_name='+')
    transactions = models.ManyToManyField(Transaction, blank=True)
    inEvent = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    currency =  CurrencyField(default=DEFAULT_CURRENCY, choices=CURRENCY_CHOICES)


    @classmethod
    def create_new(cls, name='', members=[], admins=[], transactions=[], public=False, commit=True):
        '''Default method for creating a group
        if public=True, then everyone can see the group,
        otherwise only members and admins
        if commit=False then the returnd object is not saved in the db'''
        members_gp = PermGroup.create_new(members)
        admins_gp = PermGroup.create_new(admins)
        group = cls(name=name, members=members_gp, admins=admins_gp, public=public)
        if commit:
            group.save()
            group.transactions.add(*transactions)
        if not commit and transactions!=[] :
            raise SuspiciousOperation('groups.Group.create_new : commit=False with transactions!=[] is impossible')
        return group

    @classmethod
    def create_for_event(cls,currency):
        '''Default method for creating a group for an event
        the group is invisible to the users, so nobody has perm to view, edit...'''
        members_gp = PermGroup.create_new()
        group = cls(members=members_gp)
        group.public = False
        group.inEvent = True
        group.currency = currency
        group.save(set_perms=False)
        return group

    def save(self, set_perms=True, *args, **kwargs):
        super().save(*args, **kwargs)
        # the instance has to be save to set permissions :
        if set_perms:
            set_admin_perm(self, self.admins)
            set_members_perm(self, self.members, public=self.public)

    def __repr__(self):
        '''Enables to display a group in a convenient way'''
        return "name : {}, members : {}, transactions : {}".\
        format(self.name, self.members.members, self.transactions)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Group{}".format(self.id)

    def get_absolute_url(self):
        return reverse('groups:group-number', args=(str(self.id),))

    def relationship_matrix(self):
        '''Returns M matrix of size n*n with n the number of attendees
        with M[i][j] the secrete mark i gave j, 0 if no such mark exists'''
        list_mem = [m for m in self.members.all()]
        n = len(list_mem)

        M = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            # I cannot quicker way than to do it without two loops, because a mark is between user1
            # and user2 and I don't find a way to know the number of user2 without being as
            # long as with a loop
            for j in range(n):
                try:
                    M[i][j] = SecretMark.objects.get(user=list_mem[i], marked_user=list_mem[j]).mark
                except SecretMark.DoesNotExist:
                    ()
        return M, list_mem


class GroupInvite(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_groupinvite_set')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('group', 'user'),)

    @classmethod
    def create_new(cls, group, user):
        if user in group.members.all():
            raise SuspiciousOperation("GroupInvite already sent to this user for this group")
        gi = cls(group=group, user=user)
        gi.save()
        assign_user_view_perm(group, user)
        return gi

    def accept(self):
        user = self.user
        group = self.group
        self.group.members.add(user)
        b = Balance (user=user,group = group,amount = Money(0,group.currency))
        b.save()
        self.delete()
        remove_user_view_perm(self.group, self.user)

    def decline(self):
        self.delete()
        remove_user_view_perm(self.group, self.user)

    @classmethod
    def related_to_group(cls, group):
        return cls.objects.filter(group=group)

    @classmethod
    def related_to_user(cls, user):
        return cls.objects.filter(user=user)

    @classmethod
    def users_invited(cls, group):
        '''returns the list of users invited to a certain group'''
        return User.objects.filter(user_groupinvite_set__group=group)


class BalanceManager(models.Manager):
    @classmethod
    def balancesOfGroup(self, group):
        return Balance.objects.filter(group = group)

    @classmethod
    def balancesOfUser(self, user):
        return Balance.objects.filter(user=user)
    @classmethod
    def balanceOfUserInGroup (self, user, group):
        return Balance.objects.filter(group = group, user=user)

class Balance (models.Model):
    ''' A balance is related to a person in a group
    This class is made to prevent from calculating the balance
    each time we click on the group number'''
    objects = BalanceManager()

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)

    amount = MoneyField(max_digits=14, decimal_places=2, default_currency=DEFAULT_CURRENCY)

    @classmethod
    def create_new(cls, user, group, amount):
        '''Default method for creating a balance'''
        balance = cls(user=user,group=group,amount=amount)
        balance.save()
        return balance
