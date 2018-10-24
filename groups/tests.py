''' Test set for the group app '''

from django.test import TestCase
from django.contrib.auth.models import User
from groups.models import *
from django.db.models.query import QuerySet

class GroupTestCase(TestCase):
    #u=User.objects.create_user(username='alice', email='alice@mail.com', password='alicepass')
    #u.save()
    u=User.objects.get(username='alice')

    g=Group( name='abc')
    g2=Group()
    g.save()
    g2.save()
    print(g.members.all())
    g.members.set([u,u,])
    print(g.members.all())
    
    t=TransactionForGroup(
        group = g,
        payer = u,
        amount = 1.,
        )
    t.save()
    t.beneficiaries.set([u,u])
    print("\nt: ",t.__repr__())
    
    print("\nt.beneficiaires:")
    for i in t.get_beneficiaries():
        print(i)

    print("\ng.get_transaction_list:")
    l=g.get_transaction_list()
    print(l)
    for x in l:
        print(x.amount)
