from django.test import TestCase
from presentation.models import *
from .functions import *
# Create your tests here.

class FunctionsTestCase(TestCase):
    print("\n\n - running tests for the presentation app:\n")


    def test_six_random_friends(self):
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
        friendship = Friendships.create_new(a, [], [])

        for i in range(6):
            friendship.friend_list.add(L[i])

            assert(six_random_friends(a) == L[:i+1])

        friendship.friend_list.add(h)
        assert(len(six_random_friends(a)) == 6)
