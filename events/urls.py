from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.events_home, name="list"),
    path("new/", views.event_create, name="create"),
    path("<int:pk>/", views.event_detail, name="detail"),
]