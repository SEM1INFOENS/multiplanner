import django.contrib.auth.models as auth
from guardian.shortcuts import assign_perm
from django.contrib.contenttypes.models import ContentType
from groups.models import Group
from agenda.models import Event
from .utils import get_default_permission_name


manage_group_members_perm_name = 'manage_group_members'

def admins():
    admins, created = auth.Group.objects.get_or_create(name='admins')
    if created:
        assign_perm(get_default_permission_name(Group, 'change'), admins)
        assign_perm(get_default_permission_name(Group, 'view'), admins)
        assign_perm(get_default_permission_name(Event, 'change'), admins)
        assign_perm(get_default_permission_name(Event, 'view'), admins)
        print('admins Group created')

        content_type = ContentType.objects.get_for_model(auth.Group)
        perm, created = auth.Permission.objects.get_or_create(
            codename=manage_group_members_perm_name,
            content_type=content_type,)
        assign_perm(manage_group_members_perm_name, admins, admins)
        print('%s Permission created' % manage_group_members_perm_name)
    return admins

def users():
    users, created = auth.Group.objects.get_or_create(name='users')
    if created:
        users_qs = auth.User.objects.all()
        users.user_set.add(*users_qs)
        print('users Group created')
    return users
