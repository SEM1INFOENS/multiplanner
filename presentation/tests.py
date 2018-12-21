from django.test import TestCase
from presentation.models import *
from .functions import *
from friendship.models import Friend, FriendshipRequest

#import coverage
# Create your tests here.

def set_inclus(l1,l2):
    for x in l1:
        assert x in l2

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
                set_inclus(L2 , L[:i]) and set_inclus(L[:i], L2)
            else:
                set_inclus(L2 , L) and len(L2)==n

    def test_latest_transactions(self):
        import time

        A = User.objects.create_user(username='A')
        B = User.objects.create_user(username='B')
        C = User.objects.create_user(username='C')

        trAB = Transaction.create_new(payer=A, amount=10, beneficiaries=[A, B], motive='1')
        time.sleep(.001)
        trAC = Transaction.create_new(payer=A, amount=10, beneficiaries=[A, C], motive='2')
        time.sleep(.001)
        trABC = Transaction.create_new(payer=A, amount=10, beneficiaries=[A, B, C], motive='3')

        groupAB = Group.create_new(name='AB', members=[A, B], transactions=[trAB])
        groupAC = Group.create_new(name='AC', members=[A, C], transactions=[trAC])
        groupABC = Group.create_new(name='ABC', members=[A, B, C], transactions=[trABC])

        n_tr = lambda u,n : [tr for (tr,info1,info2,info3) in n_transactions_of_user(u,n)]
        assert set(n_tr(A, 1)) == {trABC}
        assert set(n_tr(A, 2)) == {trABC, trAC}
        assert set(n_tr(A, 3)) == {trABC, trAC, trAB}
        assert set(n_tr(B, 1)) == {trABC}
        assert set(n_tr(B, 2)) == {trABC, trAB}
        assert set(n_tr(C, 1)) == {trABC}
        assert set(n_tr(C, 2)) == {trABC, trAC}

    def test_balance_of_user(self):

        A = User.objects.create_user(username='A')
        B = User.objects.create_user(username='B')
        C = User.objects.create_user(username='C')

        trAB = Transaction.create_new(payer=A, amount=10, beneficiaries=[A, B], motive='1')
        trAC = Transaction.create_new(payer=C, amount=10, beneficiaries=[A, C], motive='2')
        trABC = Transaction.create_new(payer=B, amount=60, beneficiaries=[A, B, C], motive='3')

        groupAB = Group.create_new(name='AB', members=[A, B], transactions=[trAB])
        groupAC = Group.create_new(name='AC', members=[A, C], transactions=[trAC])
        groupABC = Group.create_new(name='ABC', members=[A, B, C], transactions=[trABC])

        assert balance_of_user(A) == (5, 25)
        # paid 10/2=5 for B ; C paid 10/2=5 and B paid 60/3=20 for A
        assert balance_of_user(B) == (40, 5)
        # paid 60*2/3=40 for A and C ; A paid 10/2=5 for B
        assert balance_of_user(C) == (5, 20)
        # paid 10/2=5 for A ; B paid 60/3=20 for C
