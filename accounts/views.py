from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages


def home(request):
    '''Home view for the accounts app'''
    return render(request, 'accounts/home.html')

def login_view(request):
    """
    Login view for Week 1
    Authenticates Users
    """
    # If the user is logged in, redirect to home page
    if request.user.is_authenticated:
        return redirect('home')  # Use URL name instead of hardcoded path

    # This handles the POST submission
    if request.method == 'POST':
        username = request.POST.get('username')  # .get() is safer than ['username']
        password = request.POST.get('password')

        # Tries to authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')  # Use URL name
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'accounts/login.html')