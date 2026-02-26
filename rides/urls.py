from django.urls import path

from . import views

app_name = "rides"

urlpatterns = [
    path("", views.ride_list, name="list"),
    path("new/", views.ride_create, name="create"),
    path("<int:pk>/", views.ride_detail, name="detail"),
    path("<int:pk>/edit/", views.ride_edit, name="edit"),
    path("<int:pk>/delete/", views.ride_delete, name="delete"),
    path("<int:pk>/request/", views.ride_request_join, name="request_join"),
    path("requests/<int:request_pk>/respond/", views.ride_request_respond, name="request_respond"),
    path("notifications/", views.notifications, name="notifications"),
    path('my-rides/', views.my_rides, name='my_rides'),
    path('my-rides/cancel/<int:request_pk>/', views.cancel_ride, name='cancel_ride'),
]