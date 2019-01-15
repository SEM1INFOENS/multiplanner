'''Models of the accounting app'''

from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from djmoney.settings import DEFAULT_CURRENCY
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q

# def validate_amount(value):
#  '''Checks that the amount is positive and has less than two
#  figures after the comma.'''
#  try:
#      value = float(value)
#      assert value >= 0.
#      assert round(value, 2) == value
#      return value
#  except:
#      raise ValidationError('{} is neither a positive integer nor a float  number'.format(value))


class TransactionManager(models.Manager):

    @classmethod
    def with_user(self, user):
        return Transaction.objects.filter(Q(payer=user) | Q(transactionpart__beneficiary=user)).distinct()
    def get_transaction_part_with_transaction (self,transaction):
        return TransactionPart.objects.filter(transaction = transaction)


class Transaction(models.Model):
    '''One person gives money to one or more members of a group.
    Be careful! If the expeditor of the transaction is deleted, the transaction they made as well.
    If the group is deleted, the transactions in it are deleted as well.
    '''
    objects = TransactionManager()

    motive = models.CharField(max_length=1000, blank=True)
    date = models.DateTimeField(default=timezone.now)
    payer = models.ForeignKey(User, on_delete=models.PROTECT,
                              related_name='%(class)s_payer')
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency=DEFAULT_CURRENCY)
    calculated =  models.BooleanField(default=False)

    @classmethod
    def create_new(cls, payer, amount, beneficiaries, motive='', date=None):
        '''Default method for creating transaction and itès TransactionPart
        given a list of beneficiaries
        where every beneficiaries pay the same share
        this method is just to simplify testing'''
        if date==None:
            date = timezone.now()
        transaction = cls(motive=motive, date=date, payer=payer)
        transaction.save()
        share = amount/len(beneficiaries)
        for b in beneficiaries:
            TransactionPart(transaction=transaction, beneficiary=b, amount=share).save()
        return transaction

    def get_beneficiaries(self):
        '''Returns all the beneficiaries of the transaction'''
        trp = self.transactionpart_set.all()
        return list(set([t.beneficiary for t in trp]))

    def amount_payed(self, user):
        if user == self.payer:
            amounts = self.transactionpart_set.all().exclude(beneficiary=user).values_list('amount', flat=True)
            return sum(amounts)
        else:
            amounts = self.transactionpart_set.filter(beneficiary=user).values_list('amount', flat=True)
            return -sum(amounts)

    def total_amount(self):
        amounts = self.transactionpart_set.all().values_list('amount', flat=True)
        return sum(amounts)

    def __repr__(self):
        '''Enables to display a Transaction in a convenient way'''
        return "motive : {}, date : {}, payer : {}, amount : {}, beneficiaries : {}" \
        .format(self.motive, self.date, self.payer, self.total_amount(), self.get_beneficiaries())

    def __str__(self):
        if len(self.get_beneficiaries()) <= 3:
            ben = [b.username for b in self.get_beneficiaries()]
            return "{} ({} payed {} for {})".format(self.motive, self.payer.username, self.amount, ", ".join(ben))
        else:
            return "{} ({} payed)".format(self.motive, self.payer.username)


    def get_absolute_url(self):
        return reverse('accounting:transaction-details', args=(str(self.id),))

class TransactionPart(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    beneficiary = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency=DEFAULT_CURRENCY)



class SharedAccount(models.Model):
    '''A shared account is for a group of people that pay together.
    A shared account is not needed unless there are two or more persons in it.'''
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)

    @classmethod
    def create_new(cls, nameSA, membersSA):
        '''nameSA is the name of the Shared Account, members SA is a list of User'''
        sa = cls(name=nameSA)
        sa.save()
        sa.members.add(*membersSA)
        return sa

    def __repr__(self):
        '''Enables to display a SharedAccount in a convenient way'''
        return "name : {}, members : {}".format(self.name, self.members)

    def __str__(self):
        members = [m.username for m in self.members.all()]
        return "{} [{}]".format(self.name, "|".join(members))
