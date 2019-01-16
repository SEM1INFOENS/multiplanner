from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required_or_403
from django.template import context
from django.contrib import messages

from permissions.utils import get_default_permission_name
from permissions.forms import PermGroupForm
from .forms import *
from accounting.forms import TransactionForm
from accounting import resolution
from .models import Group, Balance, GroupInvite
from djmoney.money import Money

@login_required
def showGroups (request):
    user = request.user
    groups  = Group.objects.containsUser(user)
    context = {
	'groups' : groups ,
    }
    return render(request, 'groups.html',context)


@login_required
def create_group (request):
    context = {'new' : True}
    if request.method == 'POST':
        group_form = GroupForm(request.POST, creator_user=request.user)
        admins_form = PermGroupForm(request.POST, prefix='admins')
        members_form = PermGroupForm(request.POST)
        if group_form.is_valid() and admins_form.is_valid() and members_form.is_valid():
            group_form.instance.admins = admins_form.save()
            group_form.instance.members = members_form.save()
            group = group_form.save()
            group.save()
            success = messages.success(request, 'Group has been successfully created')
            for m in group.members.all():
                b = Balance (user=m,group = group,amount = Money(0,group.currency))
                b.save()
            return redirect('groups:group-number', ide=group.id)
    else :
        group_form = GroupForm(creator_user=request.user)
        admins_form = PermGroupForm(label='admins', prefix='admins', initial=[request.user])
        members_form = PermGroupForm(label='members')
    context.update({'group_form': group_form, 'admins_form': admins_form, 'members_form': members_form})
    return render(request, 'edit_group.html', context)


change_perm = get_default_permission_name(Group, 'change')
@login_required
@permission_required_or_403(change_perm, (Group, 'pk', 'ide'), accept_global_perms=True)
def edit_group(request,ide):
    context = {'new' : False}
    group = get_object_or_404(Group, pk=ide)

    if request.method == 'POST':
        group_form = GroupForm(request.POST, creator_user=request.user, instance=group)
        admins_form = PermGroupForm(request.POST, prefix='admins', instance=group.admins)
        members_form = PermGroupForm(request.POST, instance=group.members)
        if group_form.is_valid() and admins_form.is_valid() and members_form.is_valid():
            balances = Balance.objects.balancesOfGroup(group)
            admins_form.save()
            members_form.save()
            group = group_form.save()
            group.save()

            # If the number of members changes then update balances in group
            u = []
            for b in balances:
                if b.user not in group.members.all():
                    b.delete()
                else:
                    u.append(b.user)
            for m in group.members.all():
                if m not in u:
                    b = Balance(user=m,group = group,amount = Money(0,group.currency))
                    b.save()

            success = messages.success(request, 'Group successfully modified')
            return redirect('groups:group-number', ide=group.id)
    else :
        group_form = GroupForm(creator_user=request.user, instance=group)
        admins_form = PermGroupForm(label='admins', prefix='admins', instance=group.admins)
        members_form = PermGroupForm(label='members', instance=group.members)

    context.update({'ide': group.id, 'group_form': group_form, 'admins_form': admins_form, 'members_form': members_form})
    return render(request, 'edit_group.html', context)


view_perm = get_default_permission_name(Group, 'view')
@login_required
@permission_required_or_403(view_perm, (Group, 'pk', 'ide'), accept_global_perms=True)
def group_number(request,ide):
    group = get_object_or_404(Group, pk=ide)
    # For the moment calculate the balance each time we click on the group
    balance = resolution.balance_in_floats(group)
    balance1 = [b for b in balance]
    res = resolution.resolution_tuple(group,balance1)

    if request.method == 'POST':
        form = TransactionForm(request.POST, current_group=group, between_members=True)
        if form.is_valid():
            transaction = form.save()
            success = messages.success(request, 'Transaction successfully created')
            return redirect('accounting:transaction-details', ide=transaction.id)
    else:
        form = TransactionForm(current_group=group, between_members=True)

    list_context =[]
    members = [m for m in group.members.all()]
    for i in range(len(balance)):
        list_context.append((members[i],balance[i]))
    perm_name = get_default_permission_name(Group,'change')
    can_edit = request.user.has_perm(perm_name) or request.user.has_perm(perm_name, group)

    context= {
	'group' : group,
    'can_edit' : can_edit,
	'list_context' : list_context,
	'resolution' : res ,
	'transactions' :  group.transactions.all(),
	'form' : form,
    }
    return render(request, 'group_number.html',context)


change_perm = get_default_permission_name(Group, 'change')
@login_required
@permission_required_or_403(change_perm, (Group, 'pk', 'ide'), accept_global_perms=True)
def group_invites(request,ide):
    group = get_object_or_404(Group, pk=ide)
    if request.method == 'POST':
        form = GroupInviteForm(request.POST, current_group=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invitations succesfully sent')
            return redirect('groups:group-number', ide=group.id)
    else:
        form = GroupInviteForm(current_group=group)

    context= {
	'group' : group,
    'invited' : GroupInvite.users_invited(group),
	'form' : form,
    }
    return render(request, 'group_invites.html',context)
