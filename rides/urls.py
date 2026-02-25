from django.urls import path

from . import views

app_name = "rides"

urlpatterns = [
    path("", views.ride_list, name="list"),
    path("new/", views.ride_create, name="create"),
]