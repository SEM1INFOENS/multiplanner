from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

from accounting.models import Transaction
from .functions import *
from relationships import functions as rel

@login_required
def index(request):
    nb_of_friends = 6
    user = request.user
    last_transactions = Transaction.objects.filter(payer=user)
    groups = user.group_set.all()
    context = {
        'loggedin_user' : user,
        'last_transactions': last_transactions,
        'groups': groups,
        'events_invitations' : events_invitations(user),
        'events_will_attend' : events_will_attend(user),
        'friendship_requests' : friendship_requests(user),
        'friends' : n_random_friends(user, nb_of_friends)
    }
    return render(request, 'users/index.html', context)

@login_required
def page(request, username):
    user_page = User.objects.get(username=username)
    user = request.user
    if request.method == 'POST':
        success = rel.friendship_update(request, user_page)
    context = {
        'user' : user_page,
        'transactions': Transaction.objects.filter(payer=user_page),
    }
    rel_context = rel.friendship_context(user, user_page)
    context.update(rel_context)
    #context['old_context'] = rel_context
    return render(request, 'users/page.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('users:index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    return render(request, 'users/login.html', {})
