from guardian.shortcuts import assign_perm
from .models import PermGroup
from .utils import get_default_permission_name

def set_admin_perm(obj, group):
    ''' give to a PermGroup (the group parameter)
    the rights to administer the obj'''
    assert  type(group)==PermGroup
    model = type(obj)
    change_perm = get_default_permission_name(model, 'change')
    view_perm =   get_default_permission_name(model, 'view')
    assign_perm(change_perm, group.group, obj)
    assign_perm(view_perm, group.group, obj)

def set_members_perm(obj, group, public=False, all_admin=False):
    ''' give to a PermGroup (the group parameter)
    the members righs for the obj'''
    assert  type(group)==PermGroup
    model = type(obj)
    view_perm =   get_default_permission_name(model, 'view')
    assign_perm(view_perm, group.group, obj)

    if public:
        #assign_perm(obj, "the group with all users", view_perm)
        assert False

    if all_admin:
        change_perm = get_default_permission_name(model, 'change')
        assign_perm(obj, group.group, change_perm)
