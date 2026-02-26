from django.shortcuts import render

from .models import Event


def events_home(request):
    events = Event.objects.all()
    return render(request, "events/events.html", {"events": events})
