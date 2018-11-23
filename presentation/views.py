from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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

def login(request):
    return render(request, 'users/login.html', {})
