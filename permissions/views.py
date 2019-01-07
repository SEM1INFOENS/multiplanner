from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#from guardian.decorators import permission_required_or_403
#from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseForbidden


#@permission_required_or_403(manage_group_members_perm_name, admins, accept_global_perms=True)
@login_required
def manage_app_admins(request):
    ''' view to call when a 'add_app_admin'
    or 'remove_app_admin' button is pressed'''
    from .group import admins, manage_group_members_perm_name
    user = request.user
    if not user.has_perm(manage_group_members_perm_name, admins or\
        user.has_perm(manage_group_members_perm_name)):
        return HttpResponseForbidden()
    assert request.method == 'POST'
    redirect_url = request.POST.get('redirect_url')
    user_page = User.objects.get(username=request.POST.get('user_page'))
    if "add_app_admin" in request.POST:
        admins.user_set.add(user_page)
    if "remove_app_admin" in request.POST:
        admins.user_set.remove(user_page)
    return redirect(redirect_url)


def manage_app_admins_context(user, user_page):
    ''' returns a context that specifies
    if a user is alowed to add or remove an app-admin'''
    from .group import manage_group_members_perm_name, admins
    can_manage = user.has_perm(manage_group_members_perm_name, admins) or\
        user.has_perm(manage_group_members_perm_name)
    context = {
        'can_add_app_admin' : can_manage and (admins not in user_page.groups.all()),
        'can_remove_app_admin' : can_manage and (admins in user_page.groups.all()),
    }
    return context
