from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

from accounting.models import Transaction
from agenda.models import Event
from groups.models import Group
from .functions import *
from relationships import functions as rel
from relationships.models import SecretMark
from presentation.models import UserProfile
from presentation.forms import UserSettingsForm


from notify.signals import notify


@login_required
def index(request):
    nb_of_friends = 6
    nb_of_transactions = 5
    user = request.user
    groups = Group.objects.containsUser(user)
    spent, due = balance_of_user(user)
    context = {
        'loggedin_user' : user,
        'last_transactions': n_transactions_of_user(user, nb_of_transactions),
        'groups': groups,
        'events_invitations' : Event.objects.invited(user),
        'events_will_attend' : Event.objects.attending(user),
        'friendship_requests' : friendship_requests(user),
        'friends' : n_random_friends(user, nb_of_friends),
        'balance' : (spent*100 - due*100)/100,
        'balance_plus' : spent,
        'balance_minus' : -due,
    }
    
    for e in Event.objects.attending(user):
        nb_days = (e.date_time() - timezone.now()).days
        nb_minutes = (e.date_time() - timezone.now()).seconds /60
        nb_hours = nb_minutes/60
        print(e.date_time() - timezone.now())
        if ((nb_days <= 0) & (e.notifications_sent == 0)):
            e.notifications_sent = e.notifications_sent + 1
            e.save()
            notify.send(user, recipient = user, actor=e, verb = 'is in %d hours and %d minutes from now.' % (nb_hours,nb_minutes%60), nf_type = 'upcoming_event')
    return render(request, 'users/index.html', context)

@login_required
def page(request, username):
    user_page = User.objects.get(username=username)
    user = request.user
    context = {
        'user_page' : user_page,
        'transactions': Transaction.objects.filter(payer=user_page),
    }
    rel_context = rel.friendship_context(user, user_page)
    context.update(rel_context)
    from permissions.views import manage_app_admins_context
    admin_context = manage_app_admins_context(user, user_page)
    context.update(admin_context)
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
            from permissions.group import users
            users = users()
            users.user_set.add(user)
            auth_login(request, user)
            return redirect('users:index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    return render(request, 'users/login.html', {})

@login_required
def settings(request):
    user = request.user
    user_profile = UserProfile.get_or_create(user)
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
    else:
        form = UserSettingsForm(instance=user_profile)
    return render(request, 'users/settings.html', {'form': form})
