from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages


def home(request):
    '''Home view for the accounts app'''
    return render(request, 'accounts/home.html')

# Create your views here.
def login_view(request):
    """
    Login view for Week 1
    Authenticates Users
    """

    # If the user is logged in it will redirect to the admin page
    if request.user.is_authenticated:
        return redirect('/admin/')

    # This handles the submission
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Tries to authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('/admin/')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'accounts/login.html')