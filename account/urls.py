from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/',    views.login_view,       name='login'),
    path('success/',  views.success_view,      name='success'),
    path('logout/',   views.logout_view,       name='logout'),
    path('register/', views.register_view,     name='register'),
    path('profile/',  views.profile_view,      name='profile'),
    path('profile/<str:username>/', views.profile_view, name='profile_user'),
    path('settings/', views.settings_view,     name='settings'),
    path('settings/profile/',  views.settings_profile,  name='settings_profile'),
    path('settings/security/', views.settings_security, name='settings_security'),
    path('settings/account/',  views.settings_account,  name='settings_account'),
    path('settings/delete/',   views.delete_account,    name='delete_account'),
    path('', views.home_view, name='home'),
]