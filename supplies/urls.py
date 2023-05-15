from django.urls import path,include
from supplies import views
from rest_framework import routers


supplies_urlpatterns=[
    path ('supplies_add_rest/' , views.supplies_add_rest),
    path ('supplies_update_rest/' , views.supplies_update_rest),
    path ('supplies_list_rest/' , views.supplies_list_rest),
    path ('supplies_delete_rest/' , views.supplies_delete_rest),
]

