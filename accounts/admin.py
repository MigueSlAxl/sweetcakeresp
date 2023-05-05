from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Profile,User
admin.site.register(Permission)
admin.site.register(Profile)