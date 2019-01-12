'''Models for the groups app'''

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousOperation
#from django.core.exceptions import ValidationError
from accounting.models import Transaction
from permissions.models import PermGroup
from relationships.models import SecretMark
from permissions.shortcuts import *
from django.urls import reverse

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

    name = models.CharField(max_length=200, blank=True)
    members = models.OneToOneField(PermGroup, on_delete=models.CASCADE, related_name='+')
    admins = models.OneToOneField(PermGroup, null=True, blank=True, on_delete=models.CASCADE, related_name='+')
    transactions = models.ManyToManyField(Transaction, blank=True)
    inEvent = models.BooleanField(default=False)
    public = models.BooleanField(default=False)

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
    def create_for_event(cls):
        '''Default method for creating a group for an event
        the group is invisible to the users, so nobody has perm to view, edit...'''
        members_gp = PermGroup.create_new()
        group = cls(members=members_gp)
        group.public = False
        group.inEvent = True
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
