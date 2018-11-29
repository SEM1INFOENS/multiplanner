from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . import forms

@login_required
def showGroups (request):
	return render(request, 'groups.html')


@login_required
def create_group (request):
	if request.method == 'POST':
		form = forms.EventForm(request.POST, creator_user=request.user)
	else :
		pass
	return render(request, 'groups.html')


@login_required
def groups_number (request):
	return render(request, 'groups.html')
