from guardian.shortcuts import assign_perm, remove_perm
from .models import PermGroup
from .utils import get_default_permission_name


def set_public(obj):
    ''' set an obj as public (every user can view) '''
    model = type(obj)
    from .group import users
    users = users()
    view_perm = get_default_permission_name(model, 'view')
    assign_perm(view_perm, users, obj)

def set_private(obj):
    ''' set an obj as private (only admins and members can view) '''
    model = type(obj)
    from .group import users
    users = users()
    view_perm = get_default_permission_name(model, 'view')
    remove_perm(view_perm, users, obj)


def set_admin_perm(obj, group):
    ''' give to a PermGroup (the group parameter)
    the rights to administer the obj'''
    assert type(group) == PermGroup
    model = type(obj)
    change_perm = get_default_permission_name(model, 'change')
    view_perm = get_default_permission_name(model, 'view')
    assign_perm(change_perm, group.group, obj)
    assign_perm(view_perm, group.group, obj)

def set_members_perm(obj, group, public=False):
    ''' give to a PermGroup (the group parameter)
    the members righs for the obj'''
    assert type(group) == PermGroup
    model = type(obj)
    view_perm = get_default_permission_name(model, 'view')
    assign_perm(view_perm, group.group, obj)

    if public:
        set_public(obj)
    else:
        set_private(obj)

def assign_user_view_perm(obj, user):
    model = type(obj)
    view_perm = get_default_permission_name(model, 'view')
    assign_perm(view_perm, user, obj)

def remove_user_view_perm(obj, user):
    model = type(obj)
    view_perm = get_default_permission_name(model, 'view')
    remove_perm(view_perm, user, obj)
