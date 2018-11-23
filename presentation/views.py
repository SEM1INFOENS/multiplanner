from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounting.models import Transaction

@login_required
def index(request):
    user = request.user
    last_transactions = Transaction.objects.filter(payer=user)
    groups = user.group_set.all()
    context = {'last_transactions': last_transactions, 'groups': groups}
    return render(request, 'users/index.html', context)

@login_required
def page(request, username):
    user = User.objects.get(username=username)
    context = {
        'user' : user,
        'transactions': Transaction.objects.filter(payer=user),
    }
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
