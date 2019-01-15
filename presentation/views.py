from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

from accounting.models import Transaction
from agenda.models import Event
from .functions import *
from relationships import functions as rel
from relationships.models import SecretMark

from notify.signals import notify


@login_required
def index(request):
    nb_of_friends = 6
    nb_of_transactions = 5
    user = request.user
    groups = user.group_set.all()
    spent, due = balance_of_user(user)
    context = {
        'loggedin_user' : user,
        'last_transactions': n_transactions_of_user(user, nb_of_transactions),
        'groups': groups,
        'events_invitations' : Event.objects.invited(user),
        'events_will_attend' : Event.objects.attending(user),
        'friendship_requests' : friendship_requests(user),
        'friends' : n_random_friends(user, nb_of_friends),
        'balance' : spent - due,
        'balance_plus' : spent,
        'balance_minus' : -due,
    }

    return render(request, 'users/index.html', context)


@login_required
def settings(request):
    user = request.user

    context = {
        'loggedin_user' : user,
        }

    return render(request, 'users/settings.html', context)


@login_required
def page(request, username):
    user_page = User.objects.get(username=username)
    user = request.user
    context = {
        'user' : user_page,
        'transactions': Transaction.objects.filter(payer=user_page),
    }
    rel_context = rel.friendship_context(user, user_page)
    context.update(rel_context)
    #context['old_context'] = rel_context
    return render(request, 'users/page.html', context)

@login_required
def set_secret_mark(request):
    assert request.method == 'POST'
    redirect_url = request.POST.get('redirect_url')
    user_to_mark = User.objects.get(pk=request.POST.get('user_to_mark'))
    mark = request.POST.get('mark')
    m = SecretMark.create_new(request.user,user_to_mark,mark)
    m.save()
    return redirect(redirect_url)	

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
