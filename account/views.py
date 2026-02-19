from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import CustomUserRegistrationForm

def success_view(request):
    return render(request, 'account/success.html')

@require_http_methods(["GET", "POST"])
def login_view(request):
    '''
    Docstring for login_view
    
    :param request: Description
    '''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after login
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'account/login.html')

@require_http_methods(["GET", "POST"])
def register_view(request):
    """
    Handle user registration with form validation and user creation
    """
    
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        
        if form.is_valid():
            # Create user with hashed password (handled by UserCreationForm)
            user = form.save()
            
            # Get username and password for authentication
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            # Authenticate and login the user
            authenticated_user = authenticate(
                username=username,
                password=password
            )
            
            if authenticated_user is not None:
                login(request, authenticated_user)
                
                # Success message
                messages.success(
                    request,
                    f'Welcome, {user.get_full_name()}! Your account has been created successfully.'
                )
                
                # Redirect to home page
                return redirect('home')
            else:
                # This shouldn't happen, but just in case
                messages.error(
                    request,
                    'Account created but login failed. Please try logging in.'
                )
                return redirect('login')
        else:
            # Form has validation errors
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        # GET request - show empty form
        form = CustomUserRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Register'
    }
    
    return render(request, 'account/register.html', context)

@require_http_methods(["POST", "GET"])
def logout_view(request):
    """
    Handle user logout
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return render(request, 'account/login.html')

@login_required
def home_view(request):
    """
    Home page - only accessible to authenticated users
    """
    context = {
        'title': 'Home',
        'user': request.user
    }
    
    return render(request, 'home/home.html', context) #i dont think this will work but we will see


#next thing to implement profiles 
# @login_required
# def profile_view(request):
#     """
#     User profile page
#     """
#     context = {
#         'title': 'Profile',
#         'user': request.user
#     }
    
#     return render(request, 'accounts/profile.html', context)