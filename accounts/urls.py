from django.urls import path
from django.contrib import admin
from accounts import views

accounts_urlpatterns = [
    path('api/login/', views.CustomAuthToken.as_view(), name='api_login'),
    path('user_user_list_rest/',views.user_user_list_rest),
    # path('signup/', SignUpView.as_view(), name="signup"),
    # path('profile/', ProfileUpdate.as_view(), name="profile"),  
    # path('profile/email/', EmailUpdate.as_view(), name="profile_email"),       
    # path('profile_edit/', views.profile_edit, name='profile_edit'), 
    
]
