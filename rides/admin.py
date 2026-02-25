from django.contrib import admin

from .models import Ride


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ("pickup_location", "destination", "price", "departure_time", "driver")
    list_filter = ("departure_time",)
    search_fields = ("pickup_location", "destination", "driver__username")
