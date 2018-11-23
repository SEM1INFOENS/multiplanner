from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
#from .models import Friendships
from friendship.models import Friend
import operator
import functools
from django.db.models import Q, F



def filter_r(query_list, result):
    if query_list==[] :
        print("none")
        r= User.objects.none()
        return r
    else :
        print("not none")
        r = result.filter(
            functools.reduce(operator.and_,
                             (Q(username__icontains=q) for q in query_list)) 
            #reduce(operator.and_,
            #       (Q(content__icontains=q) for q in query_list))
        )
        print(result)
        print(r)
        return r

def qs_of_list(l, c):
    lid = [x.id for x in l]
    return c.objects.filter(pk__in=lid)


@login_required
def user_search(request):
    query = request.GET.get('q')
    query_list = query.split()
    user = request.user
    friends = qs_of_list(Friend.objects.friends(user), User)
    p_invites = qs_of_list([f.from_user for f in Friend.objects.requests(user=user)], User)
    other_users = User.objects.all().difference(friends, p_invites)
    context = {
        'query' : query,
        'p_invites' :   filter_r(query_list, p_invites),
        'friends' :     filter_r(query_list, friends),
        'other_users' : filter_r(query_list, other_users), #the other_usrs are not filtered and I don't understand why..., the bug is present since friendships modification
        # 's_invites' : filter_r(query_list, s_invites),
    }
    return render(request, 'research_user.html', context)


@login_required
def add(request, to_username): #, template_name='friendship/friend/add.html'):
    """ Create a FriendshipRequest """
    context = {'to_username': to_username}

    if request.method == 'POST':
        to_user = User.objects.get(username=to_username)
        from_user = request.user
        try:
            Friend.objects.add_friend(from_user, to_user)
        except AlreadyExistsError as e:
            context['errors'] = ["%s" % e]
        else:
            return redirect('presentation:page', username=to_username)
    return redirect('presentation:page', username=to_username) # it woult be better to redirect the user to it's curent page
