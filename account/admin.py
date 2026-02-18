from django.contrib import admin
from account.models import Car
from account.models import User


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('CAR_MAKE', 'CAR_MODEL')
    list_filter = ('CAR_MAKE', 'CAR_MODEL')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('Username', 'Email', 'Driver_Status', 'Verified_Status')
    list_filter = ('Username', 'Email', 'Driver_Status', 'Verified_Status')
