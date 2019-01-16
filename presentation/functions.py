from random import shuffle
from friendship.models import Friend
from django.utils import timezone
from django.db.models import Q
from djmoney.money import Money
from groups.models import Group, Balance
from agenda.models import Event
from accounting.models import Transaction
from accounting import functions as acc_functions
from accounting.webScraping import get_currency_equivalence
from presentation.models import UserProfile

def queryset_to_list(Q):
    L = []
    for q in Q:
        L.append(q)
    return L

# new method in the Transaction model
# def amount_payed(tr, user):
#         benef = tr.beneficiaries.all()
#         if user == tr.payer:
#             if user in benef:
#                 return round(tr.amount*(1-1/benef.count()), 2)
#             else:
#                 return tr.amount
#         else:
#             if user in benef:
#                 return -round(tr.amount/benef.count(), 2)
#             else:
#                 return 0

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
    amount = tr.amount_payed(user)
    type_, entity = acc_functions.related_entity(tr)
    return (tr, amount, type_,entity)

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

    transactions = Transaction.objects.with_user(u).order_by('-date')[:n]
    transactions_plus = [transaction_infos(tr,u) for tr in transactions]
    return transactions_plus

def balance_of_user(user):
    """Returns the financial balance of user, i.e. the total amount that
    they owe and the total amount that is owed to them"""
    spent = 0
    due = 0

    for tr in Transaction.objects.with_user(u):
        payed = tr.amount_payed(u)
        if payed > 0:
            spent += payed
        elif payed < 0 :
            due += -payed
    return spent, due

