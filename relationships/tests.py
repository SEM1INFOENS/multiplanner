from django.test import TestCase
from django.contrib.auth.models import User
from relationships.models import *

class GroupTestCase(TestCase):
    u=User.objects.get(username='alice')

    m1=SecretMark(user=u, marked_user=u, mark=10)
    m2=SecretMark(user=u, marked_user=u, mark=9)
    m1.save()
    m2.save()
    
    l=u.secretmark_set.all()
    print(l)
    for i in l:
        print(i.mark)
