import functools
import operator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from django.core.exceptions import ObjectDoesNotExist
from friendship.models import Friend
from django.db.models import Q
from . import functions


def filter_r(query_list, result):
    ''' Supposed to filter only the User in the QuerySet "render"
    which username match one of the strings in "query_list"'''


    if query_list == []:
        print("none")
        r = User.objects.none()
    else:
        print("not none")
        r = result.filter(
            functools.reduce(operator.and_,
                             (Q(username__icontains=q) for q in query_list))
        )


        print(result)
        print(r)
    return r

def qs_of_list(l, c):
    ''' QuerySet of objects from class "c" contailed in the list "l" '''
    lid = [x.id for x in l]
    return c.objects.filter(pk__in=lid)


@login_required
def user_search(request):
    ''' view for the search results page '''
    query = request.GET.get('q')
    query_list = query.split()
    user = request.user
    friends = qs_of_list(Friend.objects.friends(user), User)
    p_invites = qs_of_list([f.from_user for f in Friend.objects.requests(user=user)], User)

    no = friends.union(p_invites, qs_of_list([request.user], User))
    l = []
    for v in User.objects.all():
        if v not in no:
            l.append(v)

    other_users = qs_of_list(l, User)
    #the proper way to do that would be User.objects.all().difference(friends, p_invites, \
    # qs_of_list([request.user], User))
    # However, using difference breaks the code (filter_r does not manage to filter)


    context = {
        'query' : query,
        'p_invites' :   filter_r(query_list, p_invites),
        'friends' :     filter_r(query_list, friends),
        'other_users' : filter_r(query_list, other_users),
        #the other_usrs are not filtered and I don't understand why...,
        #the bug is present since friendships modification
    }
    return render(request, 'research_user.html', context)


@login_required
def friends(request):
    ''' view for the main friends page'''
    user = request.user
    context = {
        'friends' :   Friend.objects.friends(user),
        'p_invites' : [fr.from_user for fr in Friend.objects.unrejected_requests(user=user)],
        's_invites' : [fr.to_user for fr in Friend.objects.sent_requests(user=user)],
    }
    return render(request, 'friends.html', context)

@login_required
def friendship_request(request):
    ''' view caled when a friendship button si clicked '''
    assert request.method == 'POST'
    redirect_url = request.POST.get('redirect_url')
    user_page = User.objects.get(username=request.POST.get('user_page'))
    functions.friendship_update(request, user_page)
    return redirect(redirect_url)
