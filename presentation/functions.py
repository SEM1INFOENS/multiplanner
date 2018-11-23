from groups.models import Group
from random import shuffle

def queryset_to_list(Q):
    L = []
    for q in Q:
        L.append(q)
    return L

# def n_random_friends(user, n):
#         '''Returns a random list of six friends of the User user'''
#         friendqueryset = Friendships.objects.get(user=user).friend_list.all()

#         friendlist = queryset_to_list(friendqueryset)

#         if len(friendlist) <= n:
#             return friendlist

#         shuffle(friendlist)
#         return friendlist[:n]

def last_news(user):
        user_groups = user.group_set.all()
