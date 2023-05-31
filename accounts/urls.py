from django.urls import path
from django.contrib import admin
from accounts import views

accounts_urlpatterns = [
    path('api/login/', views.CustomAuthToken.as_view(), name='api_login'),
    path('user_user_list_rest/',views.user_user_list_rest),
    path('user_user_add_rest/',views.user_user_add_rest),
    path('user_admin_add_rest/',views.user_admin_add_rest),
    path('user_user_delete_rest/',views.user_user_delete_rest),
    path('user_user_update_rest/',views.user_user_update_rest),
    path('reset_password/',views.password_reset_email),
    path('reset_password_confirm/',views.password_reset_confirm),
    
    # path('signup/', SignUpView.as_view(), name="signup"),
    # path('profile/', ProfileUpdate.as_view(), name="profile"),  
    # path('profile/email/', EmailUpdate.as_view(), name="profile_email"),       
    # path('profile_edit/', views.profile_edit, name='profile_edit'), 
    
]
