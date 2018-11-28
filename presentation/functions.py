from groups.models import Group
from agenda.models import Event
from random import shuffle
from friendship.models import Friend
from django.utils import timezone
from accounting.models import Transaction

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

def n_transactions_of_user(u, n):
    """Returns the last n transactions implying an event or group u belongs to,
    sorted in chronological time"""
    groups_queryset = Group.objects.all()
    groups_of_u = []
    for g in queryset_to_list(groups_queryset):
        if u in g.members.all():
            groups_of_u.append(g)

    all_transactions = []
    for g in groups_of_u:
        all_transactions = all_transactions + queryset_to_list(g.transactions.all())

    all_transactions = sorted(all_transactions, key=lambda transaction: transaction.date)
    return all_transactions[-n:]

def balance_of_user(u):
    """Returns the financial balance of user u, i.e. the total amount that
    they owe and the total amount that is owed to them"""
    # groups_queryset = Group.objects.all()
    # groups_of_u = []
    # for g in queryset_to_list(groups_queryset):
    #     if u in g.members.all():
    #         groups_of_u.append(g)

    # spent = 0
    # due = 0

    # for g in groups_of_u:
    #     for tr in queryset_to_list(g.transactions.all()):
    #         benef = queryset_to_list(tr.beneficiaries.all())

    #         if tr.payer == u:
    #             if u in benef:
    #                 spent += round(tr.amount*(1-1/len(benef)), 2)
    #             else:
    #                 spent += tr.amount

    #         elif u in benef:
    #             due += round(tr.amount/len(benef), 2)

    # return spent, due
    spent = 0
    due = 0

    for tr in Transaction.objects.filter(payer=u):
        benef = tr.beneficiaries.all()
        if u in benef:
            spent += round(tr.amount*(1-1/len(benef)), 2)
        else:
            spent += tr.amount

    for tr in Transaction.objects.filter(beneficiaries=u).exclude(payer=u):
        benef = tr.beneficiaries.all()
        due += round(tr.amount/len(benef), 2)

    return spent, due
