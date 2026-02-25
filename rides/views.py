from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render, get_object_or_404

from .forms import RideForm
from .models import Ride


def ride_list(request):
    rides = Ride.objects.select_related("driver").all()
    return render(request, "ride_list.html", {"rides": rides})


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
