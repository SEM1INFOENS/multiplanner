from relationships.models import Friendships
from random import shuffle

def queryset_to_list(Q):
    L = []
    for q in Q:
        L.append(q)
    return L

def six_random_friends(u):
        '''Returns a random list of six friends of the User u'''
        friendqueryset = Friendships.objects.get(user=u).friend_list.all()

        friendlist = queryset_to_list(friendqueryset)

        if len(friendlist) <= 6:
            return friendlist

        shuffle(friendlist)
        return friendlist[:6]