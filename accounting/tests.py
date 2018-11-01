''' Test set for the accounting app '''

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from accounting.models import *


class SharedAccountTestcase(TestCase):
    sa_list=[]
    
    def SetUp(self):
        bob = User()
        bob.username = "blou"
        bob.save()

        sa_name="this is bob"
        sa = SharedAccount(sa_name, [bob])
        self.sa_list=[(sa, sa_name)]

        
    def test_sharedaccount(self):
        for (sa, sa_name) in self.sa_list:
            assert sa.name == sa_name
        


class TransactionTestCase(TestCase):

    def SetUp(self):
        tango = User()
        tango.username = 'tango'
        tango.save()

        bravo = User(username='bravo')
        bravo.save()

        now = timezone.now()
        transaction = Transaction.create_new(tango, 20, [tango, bravo], motive='testing', date=now)

    def test(self):
        assert True
