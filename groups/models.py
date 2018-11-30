'''Models for the groups app'''

from django.db import models
from django.contrib.auth.models import User
#from django.core.exceptions import ValidationError
from accounting.models import Transaction
from relationships.models import SecretMark


class GroupManager(models.Manager):
    def groups_of_user (self,user):
        ''' Lists the groups that the user belong to '''
        # we should exclude the groups that are in events !!  How to do it ??
        return Group.objects.filter(members = user).order_by('name')

class Group(models.Model):
    '''A group of people, inside which transactions can be made.
    To make transactions in an event, people will make transactions in the subsequent group.
    '''

    objects = GroupManager()

    name = models.CharField(max_length=200, blank=True)
    members = models.ManyToManyField(User, blank=True)
    transactions = models.ManyToManyField(Transaction, blank=True)

    @classmethod
    def create_new(cls, name, members, transactions):
        '''Default method for creating a group'''
        group = cls(name=name)
        group.save()
        group.members.add(*members)
        group.transactions.add(*transactions)
        return group

    def __repr__(self):
        '''Enables to display a group in a convenient way'''
        return "name : {}, members : {}, transactions : {}".\
        format(self.name, self.members, self.transactions)

    def __str__(self):
        members = '|'.join([m.username for m in self.members.all()])
        if members == "": members = "empty"
        return "{}:{} [{}]".format(self.id, self.name, members)

    def relationship_matrix(self):
        '''Returns M matrix of size n*n with n the number of attendees
        with M[i][j] the secrete mark i gave j, 0 if no such mark exists'''
        list_mem = self.members.all()
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
        return M


# class TransactionForGroup(Transaction):
#     '''A transaction that was made for a certain group
#     '''
#     def validate_transac_group(self, group):
#         '''Checks that all the beneficiaries of the transaction are in the group'''
#         try:
#             gp_members = group.members.all()
#             ben = self.beneficiaries.all()
#             for beneficiary in ben:
#                 assert beneficiary in gp_members
#             return group
#         except:
#             message = "Some beneficiaries of a TransactionForGroup are not in the group."
#             raise ValidationError(message)

#     group = models.ForeignKey(Group, on_delete=models.PROTECT,
#                               validators=[validate_transac_group])
#     def __repr__(self):
#         '''Enables to display a TransactionForGroup in a convenient way'''
#         return "{}, group : <{}>".format(super(TransactionForGroup, self). \
#             __repr__(), self.group.__repr__())
