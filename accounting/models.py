'''Models of the accounting app'''

from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone


def validate_amount(value):
    '''Checks that the amount is positive and has less than two
    figures after the comma.'''
    try:
        value = float(value)
        assert value >= 0.
        assert round(value, 2) == value
        return value
    except:
        raise ValidationError('{} is neither a positive integer nor a float  number'.format(value))


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
    motive = models.CharField(max_length=1000, blank=True)
    date = models.DateTimeField(default=timezone.now)
    payer = models.ForeignKey(User, on_delete=models.PROTECT,
                              related_name='%(class)s_payer')
    # related_name used to fix the 'reverse accessor' problem
    amount = models.FloatField(validators=[validate_amount])
    beneficiaries = models.ManyToManyField(User)

    def get_beneficiaries(self):
        '''Returns all the beneficiaries of the transaction'''
        return self.beneficiaries.all()

    def __init__(self, motivet, datet, payert, amountt, beneficiariest):
        '''Creates a transaction'''
        super().__init__()

        self.motive = motivet
        self.payer = payert
        self.date = datet
        self.amount = amountt

        self.save()#this have to be after the initialisations of the other fields
        #because else when saving they are set to NULL and this creates an error

        for ben in beneficiariest:
            self.beneficiaries.add(ben)


    def __repr__(self):
        '''Enables to display a Transaction in a convenient way'''
        return "motive : {}, date : {}, payer : {}, amount : {}, beneficiaries : {}" \
        .format(self.motive, self.date, self.payer, self.amount, self.beneficiaries)



class SharedAccount(models.Model):
    '''A shared account is for a group of people that pay together.
    A shared account is not needed unless there are two or more persons in it.'''
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)


    def __init__(self, nameSA, membersSA):
        '''nameSA is the name of the Shared Account, members SA is a list of User'''
        super().__init__()
        self.save()

        self.name = nameSA

        for mem in membersSA:
            self.members.add(mem)



    def __repr__(self):
        '''Enables to display a SharedAccount in a convenient way'''
        return "name : {}, members : {}".format(self.name, self.members)
