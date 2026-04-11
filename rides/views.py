from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render, get_object_or_404
from .models import Ride, RideRequest

from .forms import RideForm
from .models import Ride


def ride_list(request):
    rides = Ride.objects.select_related("driver").all()

    search_query = request.GET.get("search")
    ride_type = request.GET.get("type")

    if search_query:
        rides = rides.filter(
            pickup_location__icontains=search_query
        ) | rides.filter(
            destination__icontains=search_query
        )

    if ride_type:
        rides = rides.filter(ride_type=ride_type)

    return render(request, "ride_list.html", {"rides": rides, "search_query": search_query, "selected_type": ride_type})


@login_required
@require_http_methods(["GET", "POST"])
def ride_create(request):
    # Drivers-only rule (uses your custom User field Driver_Status)
    is_driver = getattr(request.user, "Driver_Status", False)
    if not is_driver:
        messages.error(request, "Only drivers can post rides.")
        return redirect("rides:list")

    if request.method == "POST":
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.driver = request.user
            ride.save()
            messages.success(request, "Ride posted!")
            return redirect("rides:list")
    else:
        form = RideForm()

    return render(request, "ride_form.html", {"form": form})

@login_required
@require_http_methods(["GET", "POST"])
def ride_edit(request, pk):
    ride = get_object_or_404(Ride, pk=pk)

    if ride.driver != request.user:
        messages.error(request, "You can only edit your own rides.")
        return redirect("rides:list")

    if request.method == "POST":
        form = RideForm(request.POST, instance=ride)
        if form.is_valid():
            form.save()
            messages.success(request, "Ride updated!")
            return redirect("rides:list")
    else:
        form = RideForm(instance=ride)

    return render(request, "ride_form.html", {"form": form})

@login_required
@require_http_methods(["POST"])
def ride_delete(request, pk):
    ride = get_object_or_404(Ride, pk=pk)

    if ride.driver != request.user:
        messages.error(request, "You can only delete your own rides.")
        return redirect("rides:list")

    ride.delete()
    messages.success(request, "Ride deleted.")
    return redirect("rides:list")

def ride_detail(request, pk):
    ride = get_object_or_404(Ride, pk=pk)
    user_request = None

    if request.user.is_authenticated:
        user_request = RideRequest.objects.filter(ride=ride, passenger=request.user).first()

    return render(request, 'ride_detail.html', {'ride': ride, 'user_request': user_request})


@login_required
@require_http_methods(["POST"])
def ride_request_join(request, pk):
    ride = get_object_or_404(Ride, pk=pk)

    if ride.driver == request.user:
        messages.error(request, "You can't request to join your own ride.")
        return redirect('rides:detail', pk=pk)

    if RideRequest.objects.filter(ride=ride, passenger=request.user).exists():
        messages.error(request, "You've already requested to join this ride.")
        return redirect('rides:detail', pk=pk)

    RideRequest.objects.create(ride=ride, passenger=request.user)
    messages.success(request, "Request sent!")
    return redirect('rides:detail', pk=pk)


@login_required
def notifications(request):
    if not request.user.Driver_Status:
        messages.error(request, "Only drivers have notifications.")
        return redirect('rides:list')

    pending_requests = RideRequest.objects.filter(
        ride__driver=request.user,
        status='pending'
    ).select_related('passenger', 'ride')

    return render(request, 'notifications.html', {'pending_requests': pending_requests})

@login_required
@require_http_methods(["POST"])
def ride_request_respond(request, request_pk):
    ride_request = get_object_or_404(RideRequest, pk=request_pk, ride__driver=request.user)
    action = request.POST.get('action')

    if action == 'accept':
        if ride_request.ride.seats_available() <= 0:
            messages.error(request, "Cannot accept request. This ride is full.")
        else:
            ride_request.status = 'accepted'
            messages.success(request, f"You accepted {ride_request.passenger.username}'s request.")
    elif action == 'deny':
        ride_request.status = 'denied'
        messages.success(request, f"You denied {ride_request.passenger.username}'s request.")

    ride_request.save()
    return redirect('rides:notifications')

@login_required
def my_rides(request):
    # Get all ride requests by this user that have been accepted
    accepted_rides = RideRequest.objects.filter(
        passenger=request.user,
        status='accepted'
    ).select_related('ride', 'ride__driver')  # fetch related ride & driver info

    return render(request, 'my_rides.html', {'accepted_rides': accepted_rides})

@login_required
@require_http_methods(["POST"])
def cancel_ride(request, request_pk):
    ride_request = get_object_or_404(RideRequest, pk=request_pk, passenger=request.user)

    ride_request.delete()
    messages.success(request, f"You have canceled your ride with {ride_request.ride.driver.username}.")
    return redirect('rides:my_rides')