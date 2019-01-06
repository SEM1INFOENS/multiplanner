import django.contrib.auth as auth
from guardian.shortcuts import assign_perm
from .utils import *
from groups.models import Group
from agenda.models import Event



admins, created = auth.models.Group.objects.get_or_create(name='admins')
if created:
    assign_perm(get_default_permission_name(Group, 'change'), admins)
    assign_perm(get_default_permission_name(Group, 'view'), admins)
    assign_perm(get_default_permission_name(Event, 'change'), admins)
    assign_perm(get_default_permission_name(Event, 'view'), admins)
    print('admins Group created')

users, created = auth.models.Group.objects.get_or_create(name='users')
if created:
    users_qs = auth.models.User.objects.all()
    users.user_set.add(*users_qs)
    print('users Group created')
