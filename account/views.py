from django.db.models import Avg, Count
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserRegistrationForm
from rides.models import Ride, RideRequest, Review
from datetime import date

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
    
    birthday = profile_user.birthday
    calculated_age = None
    if birthday:
        today = date.today()
        calculated_age = (today - birthday).days // 365

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
        'calculated_age' : calculated_age
    }

    return render(request, 'account/profile.html', context)

@login_required
def settings_view(request):
    return render(request, 'account/account_settings.html')

@login_required
@require_http_methods(["POST"])
def settings_profile(request):
    user = request.user
    username = request.POST.get('username', '').strip()
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    age = request.POST.get('age', '').strip()
    birthday = request.POST.get('birthday', '').strip()

    import re
    from django.contrib.auth import get_user_model
    User = get_user_model()

    if username and username != user.username:
        if len(username) < 3:
            messages.error(request, 'Username must be at least 3 characters.')
            return redirect('account:settings')
        if not re.match(r'^[\w]+$', username):
            messages.error(request, 'Username can only contain letters, numbers, and underscores.')
            return redirect('account:settings')
        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, 'That username is already taken.')
            return redirect('account:settings')
        user.username = username

    user.first_name = first_name
    user.last_name = last_name
    user.Age = int(age) if age.isdigit() else None

    if birthday:
        from datetime import date
        try:
            user.birthday = date.fromisoformat(birthday)
        except ValueError:
            pass

    user.save()
    messages.success(request, 'Profile updated successfully.')
    return redirect('account:settings')


@login_required
@require_http_methods(["POST"])
def settings_security(request):
    user = request.user
    current = request.POST.get('current_password', '')
    new_pw  = request.POST.get('new_password', '')
    confirm = request.POST.get('confirm_password', '')

    import re
    if not user.check_password(current):
        messages.error(request, 'Current password is incorrect.')
        return redirect('account:settings')
    if new_pw != confirm:
        messages.error(request, 'New passwords do not match.')
        return redirect('account:settings')
    if len(new_pw) < 8 or not re.search(r'[A-Z]', new_pw) or not re.search(r'[a-z]', new_pw) \
            or not re.search(r'\d', new_pw) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_pw):
        messages.error(request, 'Password does not meet strength requirements.')
        return redirect('account:settings')

    user.set_password(new_pw)
    user.save()
    from django.contrib.auth import update_session_auth_hash
    update_session_auth_hash(request, user)
    messages.success(request, 'Password updated successfully.')
    return redirect('account:settings')


@login_required
@require_http_methods(["POST"])
def settings_account(request):
    user = request.user
    user.Driver_Status = request.POST.get('driver_status') == 'on'
    user.save()
    messages.success(request, 'Preferences saved.')
    return redirect('account:settings')


@login_required
@require_http_methods(["POST"])
def delete_account(request):
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, 'Your account has been permanently deleted.')
    return redirect('home')