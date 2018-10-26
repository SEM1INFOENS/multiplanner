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

        now = timezone.now()
        t = Transaction('this is a tango test', now, tango, 20, [tango])

    def test(self):
        assert True
