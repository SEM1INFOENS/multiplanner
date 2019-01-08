''' Test set for the accounting app '''

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from accounting.models import *
from accounting.resolution import *

from groups.models import *
import numpy as np


class SharedAccountTestcase(TestCase):
    sa_list=[]

    def setUp(self):
        bob = User()
        bob.username = "blou"
        bob.save()

        sa_name="this is bob"
        sa = SharedAccount.create_new(sa_name, [bob])
        self.sa_list=[(sa, sa_name)]


    def test_sharedaccount(self):
        for (sa, sa_name) in self.sa_list:
            assert sa.name == sa_name



class TransactionTestCase(TestCase):

    def setUp(self):
        tango = User()
        tango.username = 'tango'
        tango.save()

        bravo = User(username='bravo')
        bravo.save()

        now = timezone.now()
        self.benef = [tango, bravo]
        transaction = Transaction.create_new(tango, 20, self.benef, motive='testing', date=now)
        self.tr = transaction


    def test(self):
        assert set(self.tr.get_beneficiaries()) == set(self.benef)


''' Test set for the resolution app '''

class ResolutionTestCase(TestCase) :
    people = []
    group = []
    transaction = []

    def setUp (self):
        self.group = []
        for i in range(10):
            name = 'Person '+ str(i)
            self.people.append(User.objects.create_user(username= name))

        self.group.append(Group.create_new(name = 'test0'))
        self.group[0].members.add(*self.people)

        for i in range(10):
            t = Transaction.create_new(
                motive = "Transaction " + str(i),
                payer = self.people[np.random.randint(0,10)],
                amount = np.random.randint(1,11),
                beneficiaries = self.group[0].members.all()
            )
            t.save()
            self.group[0].transactions.add(t)
            self.transaction.append(t)

        #group: 1 euro transaction, 3 people
        self.group.append(Group.create_new(name = 'test1'))
        self.group[1].members.add(*[self.people[0],self.people[1],self.people[2]])
        t = Transaction(
                motive = "Transaction Supplementaire",
                payer = self.people[0],
        )
        t.save()
        TransactionPart(transaction=t, amount=0.33, beneficiary=self.people[0]).save()
        TransactionPart(transaction=t, amount=0.33, beneficiary=self.people[1]).save()
        TransactionPart(transaction=t, amount=0.34, beneficiary=self.people[2]).save()
        # now the splitting will be done in the form
        # so this test is a bit useless now...
        # t = Transaction.create_new(
        #         motive = "Transaction Supplementaire",
        #         payer = self.people[0],
        #         amount = 1,
        #         beneficiaries = self.group[1].members.all()
        # )
        self.group[1].transactions.add(t)

    def test_initialisation (self):
        print (self.group)
        for i in range(len(self.transaction)):
            b = [u.id for u in self.transaction[i].get_beneficiaries()]
            print (self.transaction[i].payer,'|',b)


    def test_balance_in_fractions (self):
        members,balanceFrac = balance_in_fractions (self.group[0])
        print (balanceFrac)
        print (members)
        assert (sum(balanceFrac)==0)
        balanceFloat = balance_in_floats(self.group[0])
        assert(balanceFloat[i] == balanceFrac[i] for i in range(len(balanceFloat)))

        members,balance = balance_in_fractions (self.group[1])
        print (balance)
        print (members)
        assert (sum(balance)==0)


    def test_balance_in_floats (self) :
        balance = balance_in_floats(self.group[1])
        print('\n\n\n----------------------------', balance[0])
        assert (balance[0] == 0.67)
        assert (balance[1] == -0.34 or balance[2] == -0.34)
        assert (balance[1] == -0.33 or balance[2] == -0.33)

    def test_resolution (self) :
        balance = balance_in_floats(self.group[1])
        res = resolution_tuple(self.group[1],balance)
        for i in res:
            print (i[0], "should give", i[1], "an amount of", i[2])
