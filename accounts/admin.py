from django.contrib import admin
from accounts.models import UserStandard, User


# Register your models here.

admin.site.register(User)
admin.site.register(UserStandard)
