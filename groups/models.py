'''Models for the groups app'''

from django.db import models
from django.contrib.auth.models import User
from accounting.models import Transaction


class Group(models.Model):
    '''A group of people, inside which transactions can be made.
    To make transactions in an event, people will make transactions in the subsequent group.
    '''
    name = models.CharField(max_length=200, blank=True)
    members = models.ManyToManyField(User)
    def get_transaction_list(self):
        return self.transactionforgroup_set.all()
    def __repr__(self):
        '''Enables to display an Event in a convenient way'''
        return "name : {}".format(self.name)

    
class TransactionForGroup(Transaction):
    '''A transaction that was made for a certain group
    '''
    def validate_TransacGroup(group):
        try:
            gp_members = group.members.all()
            ben = self.beneficiaries.all()
            for b in ben:
                assert (b in gp_members)
            return group
        except:
            raise ValidationError("some beneficiaries of a TransactionForGroup are not in the group")
    group = models.ForeignKey(Group, on_delete=models.PROTECT,
                              validators=[validate_TransacGroup])
    def __repr__(self):
        '''Enables to display a TransactionForGroup in a convenient way'''
        return "{}, group : <{}>".format(super(TransactionForGroup, self).__repr__(), self.group.__repr__())
