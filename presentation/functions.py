from groups.models import Group
from agenda.models import Event
from random import shuffle
from friendship.models import Friend
from django.utils import timezone
from django.db.models import Q
from accounting.models import Transaction

def queryset_to_list(Q):
    L = []
    for q in Q:
        L.append(q)
    return L

def amount_payed(tr, user):
        benef = tr.beneficiaries.all()
        if user == tr.payer:
            if user in benef:
                return round(tr.amount*(1-1/benef.count()), 2)
            else:
                return tr.amount
        else:
            if user in benef:
                return -round(tr.amount/benef.count(), 2)
            else:
                return 0
    
def n_random_friends(user, n):
    '''Returns a random list of six friends of the User user'''

    friendlist = Friend.objects.friends(user)

    if len(friendlist) <= n:
        return friendlist

    shuffle(friendlist)
    return friendlist[:n]

def last_news(user):
    user_groups = user.group_set.all()


def friendship_requests(user):
    '''List the user's friendship requests'''
    return Friend.objects.unrejected_requests(user=user)

def transaction_infos(tr, user):
    amount = amount_payed(tr, user)
    try:
        group = Group.objects.get(transactions=tr)
        try:
            event = group.event
            return (tr, amount, 'event', event)
        except Event.DoesNotExist:
            return (tr, amount, 'group', group)
    except Group.DoesNotExist:
        return (tr, amount, '', None)
    

def n_transactions_of_user(u, n):
    """Returns the last n transactions implying an event or group u belongs to,
    sorted in chronological time"""
    # groups_queryset = Group.objects.all()
    # groups_of_u = []
    # for g in queryset_to_list(groups_queryset):
    #     if u in g.members.all():
    #         groups_of_u.append(g)

    # all_transactions = []
    # for g in groups_of_u:
    #     all_transactions = all_transactions + queryset_to_list(g.transactions.all())

    # all_transactions = sorted(all_transactions, key=lambda transaction: transaction.date)
    # return all_transactions[-n:]
    
    transactions = Transaction.objects.filter(Q(payer=u) | Q(beneficiaries=u)).distinct().order_by('date')[:n]
    transactions_plus = [transaction_infos(tr,u) for tr in transactions]
    return transactions_plus

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

    for tr in Transaction.objects.filter(Q(payer=u) | Q(beneficiaries=u)).distinct():
        payed = amount_payed(tr, u)
        if payed > 0:
            spent += payed
        elif payed < 0 :
            due += -payed
    return spent, due
