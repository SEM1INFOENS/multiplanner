from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Friendships
import operator
import functools
from django.db.models import Q, F


def filter_r(query_list, result):
    result = result.filter(
        functools.reduce(operator.and_,
               (Q(username__icontains=q) for q in query_list)) 
         #reduce(operator.and_,
         #       (Q(content__icontains=q) for q in query_list))
    )
    return result

@login_required
def user_search(request):
    query = request.GET.get('q')
    query_list = query.split()
    u = request.user
    try:
        fs = u.friendships #this works because user is a OneToOneFiels in Friendships
        friends = fs.friend_list.all()
        s_invites = fs.invited_list.all()
    except ObjectDoesNotExist:
        friends = User.objects.none()
        s_invites = User.objects.none()
    #p_invites = Friendships.objects.filter(invited_list=u).user     
    p_invites = User.objects.filter(friendships__invited_list=u)     
    other_users = User.objects.all().difference(friends, s_invites, p_invites)
    context = {
         'query' : query,
         'users' : filter_r(query_list, other_users),
         'p_invites' : filter_r(query_list, p_invites),
         'friends' : filter_r(query_list, friends),
         's_invites' : filter_r(query_list, s_invites),
    }
    return render(request, 'research_user.html', context)
