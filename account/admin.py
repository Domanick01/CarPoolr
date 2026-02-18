from django.contrib import admin
from account.models import Car, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('CAR_MAKE', 'CAR_MODEL')
    list_filter = ('CAR_MAKE', 'CAR_MODEL')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Columns to display in the admin list view
    list_display = ('username', 'email', 'Driver_Status', 'Verified_Status', 'is_staff')
    
    # Filters for the right-hand sidebar
    list_filter = ('Driver_Status', 'Verified_Status', 'is_staff', 'is_superuser', 'is_active')
    
    # Fields to show when editing a user
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'Age', 'Phone_Number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Driver info', {'fields': ('Driver_Status', 'Verified_Status', 'Rating')}),
    )
    
    # Fields to show when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'Age', 'Phone_Number', 'Driver_Status', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
