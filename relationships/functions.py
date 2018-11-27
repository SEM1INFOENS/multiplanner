from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from friendship.models import Friend, FriendshipRequest
from django.contrib import messages


def friendship_context(user, user_page):
    '''returns a context that specifies which friendship operations are possible or not'''  
    print(Friend.objects.sent_requests(user=user))
    uSendPage = user_page in [fr.to_user for fr in Friend.objects.sent_requests(user=user)]
    pageSendU = user in [fr.to_user for fr in Friend.objects.sent_requests(user=user_page)]
    uRecivedPage = user_page in [fr.from_user for fr in Friend.objects.unrejected_requests(user=user)]
    areFr = Friend.objects.are_friends(user,user_page)
    nsame = not (user == user_page)
    context = {
        'can_add' : nsame and (not areFr) and (not uSendPage) and (not pageSendU),
        'can_cancel' : nsame and (not areFr) and uSendPage ,
        'can_accept_decline' : nsame and (not areFr) and uRecivedPage,
        'can_remove' : nsame and areFr,
    }
    return context


#it woud be great to introduce a semaphore to ensure the context does not changes during the tests...
@login_required
def friendship_update(request, user_page):
    ''' update the friendship status according to the buttons pressed by the user'''
    user = request.user
    context = friendship_context(user, user_page)
    assert(request.method == 'POST')
    try:
        if "add" in request.POST:
            assert context['can_add']
            Friend.objects.add_friend(user, user_page)
            messages.info(request, "friendship request sent to {}".format(user_page))
        if "cancel" in request.POST:
            assert context['can_cancel']
            fr = FriendshipRequest.objects.get(to_user=user_page, from_user=user)
            fr.cancel()
            messages.info(request, "friendship request to {} canceled".format(user_page))
        if "accept" in request.POST:
            assert context['can_accept_decline']
            fr = FriendshipRequest.objects.get(to_user=user, from_user=user_page)
            fr.accept()
            messages.success(request, "you are now friend with {}".format(user_page))
        if "decline" in request.POST:
            assert context['can_accept_decline']
            fr = FriendshipRequest.objects.get(to_user=user, from_user=user_page)
            fr.reject()
            messages.info(request, "you refused {}'s friendship request".format(user_page))
        if "remove" in request.POST:
            assert context['can_remove']
            Friend.objects.remove_friend(user, user_page)
            messages.info(request, "you are not any more friend with {}".format(user_page))
        return True
    except AssertionError:
        messages.warning(request, "something changed between page load and click")
        return False


