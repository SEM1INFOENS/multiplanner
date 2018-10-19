from django.db import models
from group.models import Group


def validate_amount(value):
    '''Checks that the amount is positive and returns a float which has less than two
    figures after the comma.'''
    try:
        assert value >= 0.0
        return round(float(value), 2)
    except:
        raise ValidationError(
            _('%(value)s is neither a positive integer nor a float  number'),
            params={'value': value},
        )

# def to_choices(l):
#     '''Checks that every element is a string and [x, y, ...] returns [(x, x), (y,y), ...] to be
#     in adequation with choices's requirements'''
#     out = []
#     for s in l:
#         assert isinstance(s, str)
#         out.append((s, s))
#     return out


class Transaction(models.Model):
    '''One person gives money to one or more members of a group.

    Be careful! If the expeditor of the transaction is deleted, the transaction they made as well.
    If the group is deleted, the transactions in it are deleted as well.
    '''
    motive = models.CharField(max_length=1000)
    date = models.DateTimeField()
    expeditor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(validators=[validate_amount])
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class SharedAccount(models.Model):
    '''A shared account is for a group of people that pay together.
    A shared account is not needed unless there are two or more persons in it.'''
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)
