'''Models for the permission app'''

from django.db import models
import django.contrib.auth as auth
from django.core.exceptions import ValidationError
from guardian.shortcuts import assign_perm as g_assign_perm


class NoNameGroup(models.Model):
    ''' to create auth Group without having to specify a name '''

    @classmethod
    def create_new(self, commit=True):
        obj = self()
        obj.save()
        ide = str(obj.id)
        g_name = 'PermGroup_{}'.format(ide)
        g = auth.models.Group(name=g_name)
        if commit:
            g.save()
        return g


class PermGroup(models.Model):
    ''' PermGroup has the same goal as auth.models.Group
    but with the possibility to get the members of the group without reverse match
    also it is simpler to instanciate
    ! please don't use self.members.add or self.group.user_set.add
    ! -> same for remove, clear, all and set '''

    members = models.ManyToManyField(auth.models.User, blank=True)
    group = models.OneToOneField(auth.models.Group, on_delete=models.CASCADE)

    @classmethod
    def create_new(self, members=[], commit=True):
        if not commit and members !=[]:
            raise ValueError('PermGroup.create_new : commit==False incompatible with members!=[]')
        pg = PermGroup()
        g = NoNameGroup.create_new(commit=False)
        pg.group = g
        if commit:
            pg.save()
        if members!=[]:
            pg.add(*members)
        return pg

    def save(self):
        self.group.save()
        self.group = self.group
        super().save()
        return self

    def clean(self):
        if self.pk: #the obj has to be saved to test the members field
            if set(self.members.all()) != set(self.group.user_set.all()):
                raise ValidationError("PermGroup : members inconsistant with group")

    def add(self, *objs):
        ''' add a user to the PermGroup '''
        self.members.add(*objs)
        self.group.user_set.add(*objs)

    def remove(self, *objs):
        ''' remove a user from the PermGroup '''
        self.members.remove(*objs)
        self.group.user_set.remove(*objs)

    def clear(self):
        ''' clears the users from the PermGroup '''
        self.members.clear()
        self.group.user_set.clear()

    def set(self, objs):
        ''' set user list to the PermGroup '''
        self.members.set(objs)
        self.group.user_set.set(objs)

    def all(self):
        return self.members.all()

    def assign_perm(self, perm, instance):
        assert False
