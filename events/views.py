from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .forms import EventForm
from .models import Event


def events_home(request):
    events = Event.objects.all()
    return render(request, "events/events.html", {"events": events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    rides = event.rides.select_related('driver').all()
    return render(request, "events/event_detail.html", {"event": event, "rides": rides})


@login_required
@require_http_methods(["GET", "POST"])
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            messages.success(request, "Event created!")
            return redirect("events:list")
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.creator != request.user:
        messages.error(request, "You can only edit events you created.")
        return redirect("events:detail", pk=pk)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated!")
            return redirect("events:detail", pk=pk)
    else:
        form = EventForm(instance=event)

    return render(request, "events/event_form.html", {"form": form, "editing": True})


@login_required
@require_http_methods(["POST"])
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.creator != request.user:
        messages.error(request, "You can only delete events you created.")
        return redirect("events:detail", pk=pk)

    event.delete()
    messages.success(request, "Event deleted.")
    return redirect("events:list")