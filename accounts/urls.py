from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from accounts import views
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns

accounts_urlpatterns = [
    path('user_user_add_rest/',views.user_user_add_rest),
    path('user_user_list_rest/',views.user_user_list_rest),
    # path('user_user_update_rest/',views.user_user_update_rest),
    path('user_user_delete_rest/',views.user_user_delete_rest),
    path('login_user_rest/',views.login_user_rest),
    path('logout_user_rest/',views.logout_user_rest),
    path('user_login_rest/',views.user_login_rest),
    path('get_user_rest/',views.get_user_rest),
    path('register_api/',views.register_api),
] 
