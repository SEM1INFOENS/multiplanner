from groups.models import Group
from agenda.models import Event
from random import shuffle
from friendship.models import Friend
from django.utils import timezone

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

def events_invitations(user):
    '''List the futur events to which the user is invited'''
    return Event.objects.filter( date__gte=timezone.now(), invited=user).exclude(attendees__members=user).order_by('creation_date')


def events_will_attend(user):
    '''List the futur events to which the user will attend'''
    return Event.objects.filter( date__gte=timezone.now(), attendees__members=user).order_by('time','date').order_by('date')

def friendship_requests(user):
    '''List the user's friendship requests'''
    return Friend.objects.unrejected_requests(user=user)



