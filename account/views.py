from django.db.models import Avg, Count
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserRegistrationForm
from rides.models import Ride, RideRequest, Review

def success_view(request):
    return render(request, 'account/success.html')

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'account/login.html')

@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, f'Welcome, {user.get_full_name()}! Your account has been created successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Account created but login failed. Please try logging in.')
                return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserRegistrationForm()

    context = {'form': form, 'title': 'Register'}
    return render(request, 'account/register.html', context)

@require_http_methods(["POST", "GET"])
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def home_view(request):
    context = {'title': 'Home', 'user': request.user}
    return render(request, 'home/home.html', context)


@login_required
def profile_view(request, username=None):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user

    offered_rides = Ride.objects.filter(driver=profile_user).count()
    taken_rides = RideRequest.objects.filter(
        passenger=profile_user,
        status='accepted'
    ).count()

    received_reviews_qs = Review.objects.filter(reviewee=profile_user)
    written_reviews_qs = Review.objects.filter(reviewer=profile_user)

    average_rating = received_reviews_qs.aggregate(avg=Avg('rating'))['avg']
    average_rating = round(average_rating, 1) if average_rating is not None else None

    recent_received_reviews = received_reviews_qs.select_related(
        'reviewer', 'ride'
    ).order_by('-created_at')[:5]

    # Build a set of dates where the user drove a ride
    drove_dates = set(
        Ride.objects.filter(driver=profile_user)
        .values_list('departure_time__date', flat=True)
    )

    # Build a set of dates where the user was a passenger
    passenger_dates = set(
        RideRequest.objects.filter(passenger=profile_user, status='accepted')
        .values_list('ride__departure_time__date', flat=True)
    )

    # Convert to sorted ISO string lists for JS
    drove_dates_list = sorted([d.isoformat() for d in drove_dates])
    passenger_dates_list = sorted([d.isoformat() for d in passenger_dates])

    context = {
        'title': 'Profile',
        'profile_user': profile_user,
        'is_own_profile': profile_user == request.user,
        'offered_rides': offered_rides,
        'taken_rides': taken_rides,
        'average_rating': average_rating,
        'received_reviews_count': received_reviews_qs.count(),
        'written_reviews_count': written_reviews_qs.count(),
        'recent_received_reviews': recent_received_reviews,
        'drove_dates': drove_dates_list,
        'passenger_dates': passenger_dates_list,
    }

    return render(request, 'account/profile.html', context)