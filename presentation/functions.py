from groups.models import Group
from random import shuffle
from friendship.models import Friend

def queryset_to_list(Q):
    L = []
    for q in Q:
        L.append(q)
    return L

def n_random_friends(user, n):
    '''Returns a random list of six friends of the User user'''
    
    friendlist = Friend.objects.friends(user)
    
    if len(friendlist) <= n:
        return friendlist
    
    shuffle(friendlist)
    return friendlist[:n]

def last_news(user):
    user_groups = user.group_set.all()
