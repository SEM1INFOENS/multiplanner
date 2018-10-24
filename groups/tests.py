''' Test set for the group app '''

from django.test import TestCase
from django.contrib.auth.models import User
from groups.models import *
from django.db.models.query import QuerySet

class GroupTestCase(TestCase):
    #u=User.objects.get(username='alice')
    #u=User.objects.create_user(username='alice', email='alice@mail.com', password='alicepass')
    #u.save()

    #g=Group(members=[u], name='abc')
    #g.save()
    #print("name: %s" % g.name)

    #g2=Group(members=[])
    #g2.save()
    #print("name: %s" % g2.name)
    
    #t=TransactionForGroup(
    #    group = g,
    #    payer = u,
    #    amount = 1.,
    #    beneficiaries = [u]
    #    )
    #t.save()
    #l= g.transactionforgroup_set.all() #.get_queryset()
    #print(isinstance(l, QuerySet))
    #print(l)
    #for x in l:
    #    print(x['amount'])
