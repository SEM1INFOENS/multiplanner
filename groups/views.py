from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import context
from django.contrib import messages

from .forms import *
from accounting import resolution

@login_required
def showGroups (request):
	user = request.user
	context = {
		'groups' : Group.objects.groups_of_user(user),
	}
	return render(request, 'groups.html',context)


@login_required
def create_group (request):
	context = {'new' : True}
	if request.method == 'POST':
		form = GroupForm(request.POST, creator_user=request.user)
		if form.is_valid():
			group = form.save()
			success = messages.success(request, 'Group has been successfully created')
			return redirect('groups:group-number', ide=group.id)
	else :
		form = GroupForm(creator_user=request.user)
	
	context.update({'form': form})
	return render(request, 'edit_group.html', context)






@login_required
def edit_group (request,ide):
	return render(request, 'groups.html')



@login_required
def group_number (request,ide):
	group = get_object_or_404(Group, pk=ide)
	#balance = resolution.balance_in_floats(group)
	#res = resolution.resolution(group,balance)
	
	if request.method == 'POST':
		form = TransactionForm(request.POST, current_group=group)  
		if form.is_valid():
			transaction = form.save()
			success = messages.success(request, 'Transaction successfully created')
			return redirect('groups:group-number', ide=group.id)
	else:
		form = TransactionForm(current_group=group)	

	transactions = [t for t in group.transactions.all()]
	context= {
		'group' : group,
		#'balance' : balance,
		#'resolution' : res ,
		'transactions' : transactions,
		'form' : form,
	}
	return render(request, 'group_number.html',context)
