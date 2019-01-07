''' Test set for the permissions app '''

from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from .utils import *
#from TransactionTestCase import assertQuerysetEqual
#https://docs.djangoproject.com/en/2.1/topics/testing/tools/#django.test.TransactionTestCase.assertQuerysetEqual
from guardian.shortcuts import assign_perm, remove_perm

class PermGroupTestcase(TestCase):

    def setUp(self):
        a = User.objects.create_user('admin')
        u = User.objects.create_user('user')
        pg = PermGroup.create_new(members=[a])

    def test(self):
        a = User.objects.get(username='admin')
        u = User.objects.get(username='user')

        print('pg:')
        for pg in PermGroup.objects.all():
            pg.clean()

        pg = PermGroup.objects.get(pk=1)
        perm = get_default_permission_name(PermGroup, 'view')

        assert not a.has_perm(perm)
        assert not u.has_perm(perm)

        assign_perm(perm, pg.group)
        # there is a cache system for the permissions
        # if we need to check a permission just after assigning it,
        # it is advised to re-get the user object
        a = User.objects.get(username='admin')
        u = User.objects.get(username='user')
        assert a.has_perm(perm)
        assert not u.has_perm(perm)

        pg.add(u)
        a = User.objects.get(username='admin')
        u = User.objects.get(username='user')
        assert a.has_perm(perm)
        assert u.has_perm(perm)

        pg.remove(*[u])
        a = User.objects.get(username='admin')
        u = User.objects.get(username='user')
        assert a.has_perm(perm)
        assert not u.has_perm(perm)

        pg.clear()
        pg.save()
        a = User.objects.get(username='admin')
        u = User.objects.get(username='user')
        assert not a.has_perm(perm)
        assert not u.has_perm(perm)

        pg.set([u, a])
        a = User.objects.get(username='admin')
        u = User.objects.get(username='user')
        assert a.has_perm(perm)
        assert u.has_perm(perm)
