''' Test set for the group app '''

from django.test import TestCase
from django.contrib.auth.models import User
from groups.models import *
from django.db.models.query import QuerySet


class GroupTestCase(TestCase):
    print("\n\n - running tests for the group app:\n")

    gt_links = {}
    users_list = []

    def setUp(self):
        #two ways to create users (one does'nt need .save() ):
        a = User.objects.create_user(username='alice')
        b = User.objects.create_user(username='bob')
        c = User(username='carlotta')
        c.save()
        self.users_list = [a, b, c]

        g1 = Group.create_new(name='ab')
        g1.members.add(*[a, b, c])

        g2 = Group.create_new()
        g2.members.add(*[a, b])

        t1 = Transaction.create_new(
            motive="testing",
            payer=a,
            amount=2.2,
            beneficiaries=g1.members.all()
        )
        g1.transactions.add(t1)

        t2 = Transaction.create_new(
            payer=a,
            amount=1.,
            beneficiaries=g1.members.all()
        )
        g1.transactions.add(t2)

        #self.users_list[0].username='test_othername'

        # not working yet:
        #def should_fail():
        #    try:
        #        # should fail because c is not in g1
        #        t2.beneficiaries.add(*[a,b,c,])
        #        return False
        #    except ValidationError:
        #        return True
        #assert should_fail()

        self.gt_links[g1] = [t1, t2]
        self.gt_links[g2] = []


    def test_repr(self):
        print(self.users_list.__repr__())
        print(self.gt_links.__repr__())


    def test_m2m(self):
        groups = Group.objects.all()
        for g in groups:
            print("\nGroup: %i (%s)" %(g.id, g.name))
            assert (g in self.gt_links.keys())


            for t in g.transactions.all():
                print("transaction: %i (%s)" %(t.id, t.motive))
                assert (t in self.gt_links[g])
            for t in self.gt_links[g]:
                assert (t in g.transactions.all())

        for g in self.gt_links.keys():
            assert (g in groups)


    def test_relationship_matrix(self):
        a = User.objects.create_user(username='alice2')
        b = User.objects.create_user(username='bob2')
        c = User.objects.create_user(username='carlotta2')
        self.users_list = [a, b, c]

        g1 = Group.create_new(name='ab')
        g1.members.add(*[a, b, c])

        m1=SecretMark.create_new(a, b, 10)
        m2=SecretMark.create_new(b, c, 9)
        m1.save()
        m2.save()

        M,members = g1.relationship_matrix()

        print("Here comes the relationship matrix")
        print(M)

        assert( M == [[0, 10, 0], [0, 0, 9], [0, 0, 0]])

        m3=SecretMark.create_new(b, a, -10)
        m3.save()
        m4=SecretMark.create_new(c, a, -10)
        m4.save()

        M,members = g1.relationship_matrix()
        assert( M == [[0, 10, 0], [-10, 0, 9], [-10, 0, 0]])

class GroupPermissionsTestCase(TestCase):

    def setUp(self):
        aa = User.objects.create_user('app_admin')
        a = User.objects.create_user('admin')
        m = User.objects.create_user('member')
        u = User.objects.create_user('user')

        # The users should have been added to the folowing groups
        # by the signup view
        from permissions.group import admins, users
        admins = admins()
        users = users()
        admins.user_set.add(aa)
        users.user_set.add(a, m, u)

        g = Group.create_new(name='test permissions', members=[a,m], admins=[a], public=False)

    def test(self):
        from permissions.utils import get_default_permission_name
        has_perm = lambda u, p, i : (u.has_perm(p,i) or u.has_perm(p))
        gp = Group.objects.get(pk=1)
        view_perm = get_default_permission_name(Group, 'view')
        change_perm = get_default_permission_name(Group, 'change')

        aa = User.objects.get(username='app_admin')
        a = User.objects.get(username='admin')
        m = User.objects.get(username='member')
        u = User.objects.get(username='user')
        assert has_perm(aa, view_perm, gp)
        assert has_perm(a, view_perm, gp)
        assert has_perm(m, view_perm, gp)
        assert not has_perm(u, view_perm, gp)
        assert has_perm(aa, change_perm, gp)
        assert has_perm(a, change_perm, gp)
        assert not has_perm(m, change_perm, gp)
        assert not has_perm(u, change_perm, gp)

        gp.public = True
        gp.save()
        aa = User.objects.get(username='app_admin')
        a = User.objects.get(username='admin')
        m = User.objects.get(username='member')
        u = User.objects.get(username='user')
        assert has_perm(aa, view_perm, gp)
        assert has_perm(a, view_perm, gp)
        assert has_perm(m, view_perm, gp)
        assert has_perm(u, view_perm, gp)
        assert has_perm(aa, change_perm, gp)
        assert has_perm(a, change_perm, gp)
        assert not has_perm(m, change_perm, gp)
        assert not has_perm(u, change_perm, gp)

        gp.public = False
        gp.save()
        aa = User.objects.get(username='app_admin')
        a = User.objects.get(username='admin')
        m = User.objects.get(username='member')
        u = User.objects.get(username='user')
        assert has_perm(aa, view_perm, gp)
        assert has_perm(a, view_perm, gp)
        assert has_perm(m, view_perm, gp)
        assert not has_perm(u, view_perm, gp)
        assert has_perm(aa, change_perm, gp)
        assert has_perm(a, change_perm, gp)
        assert not has_perm(m, change_perm, gp)
        assert not has_perm(u, change_perm, gp)


class GroupInviteTestCase(TestCase):

    def setUp(self):
        u = User.objects.create_user(username='alice')
        g = Group.create_new(name='ab')

    def test(self):
        u = User.objects.get(username='alice')
        g = Group.objects.get(pk=1)

        gi = GroupInvite.create_new(g, u)

        assert gi in GroupInvite.related_to_user(u)
        assert gi in GroupInvite.related_to_group(g)
        assert u in GroupInvite.users_invited(g)

        assert u not in g.members.all()

        gi.accept()
        assert u in g.members.all()
        assert u not in GroupInvite.users_invited(g)

        try:
            gi2 = GroupInvite.create_new(g, u)
            assert False
        except SuspiciousOperation:
            pass

        g.members.remove(u)
        assert u not in g.members.all()

        gi = GroupInvite.create_new(g, u)
        gi.decline()
        assert u not in g.members.all()
