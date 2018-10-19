'''Models for the groups app'''

from django.db import models
from django.contrib.auth.models import User
from accounting.models import Transaction


class Group(models.Model):
    '''A group of people, inside which transactions can be made.
    To make transactions in an event, people will make transactions in the subsequent group.
    '''
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)

    
class TreasactionForGroup(Transaction):
    '''A transaction that was made for a certain group
    '''
    def validate_TransacGroup(group):
        try:
            att = event.group.members.all()
            ben = self.beneficiaries.all()
            for b in ben:
                assert (b in att)
                return group
        except:
            raise ValidationError("some beneficiaries of a TransactionForGroup are not in the group")
    group = models.ForeignKey(Group, on_delete=models.PROTECT,
                              validators=[validate_TransacGroup])
