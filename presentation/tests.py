from django.test import TestCase
from presentation.models import *
from .functions import *
from friendship.models import Friend, FriendshipRequest
# Create your tests here.

def set_inclus(l1,l2):
    for x in l1:
        if x not in l2:
            print(x)
            return False
    return True
        
class FunctionsTestCase(TestCase):
    print("\n\n - running tests for the presentation app:\n")


    def test_six_random_friends(self):

        n = 6
        
        print("six_random_friends")
        a = User.objects.create_user(username='a')
        b = User.objects.create_user(username='b')
        c = User.objects.create_user(username='c')
        d = User.objects.create_user(username='d')
        e = User.objects.create_user(username='e')
        f = User.objects.create_user(username='f')
        g = User.objects.create_user(username='g')
        h = User.objects.create_user(username='h')
        L = [b, c, d, e, f, g, h]
        i = 0
        for u2 in L:
            Friend.objects.add_friend(
                a,                    # The sender
                u2,                   # The recipient
                message='Hi! I (user a)  would like to add you (user u2)') 
            f_req = FriendshipRequest.objects.get(to_user=u2)
            f_req.accept()
            print(Friend.objects.friends(a))
            
            i += 1
            L2 = n_random_friends(a,n)
            if i <= n :
                assert( set_inclus(L2 , L[:i]) and set_inclus(L[:i], L2) )
            else:
                assert( set_inclus(L2 , L) and len(L2)==n )
            
