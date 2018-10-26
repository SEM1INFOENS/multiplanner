from django.test import TestCase
from django.contrib.auth.models import User
from relationships.models import *

class GroupTestCase(TestCase):
    print("\n\n - running tests for the relationship app:\n")

    gt_links = {}
    users_list = []
    
    def setUp(self):    
        a = User.objects.create_user(username='alice')
        b = User.objects.create_user(username='bob')
        c = User(username='carlotta')
        c.save()
        self.users_list = [a,b,c,]

        m1=SecretMark(user=a, marked_user=b, mark=10)
        m2=SecretMark(user=b, marked_user=c, mark=9)
        m1.save()
        m2.save()

    def test_mark(self):
        u_qs=User.objects.all()
        for u in u_qs:
            print("\n-user %s\nmarks given:" %u.username)
            for m in u.secretmark_set.all():
                print(" to %s: %i" %(m.marked_user.username, m.mark))
                #assert (m.user==u)

            print("marks recived:")
            for m in u.marked_user_set.all():
                print(" from %s: %i" %(m.user.username, m.mark))
                #assert (m.marked_user==u)
