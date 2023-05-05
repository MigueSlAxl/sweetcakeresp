from django.urls import path,include
from productos import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


productos_urlpatterns=[
    path('productos_productos_add_rest/',views.productos_productos_add_rest),
    path('productos_productos_list_rest/',views.productos_productos_list_rest),
    path('productos_productos_update_rest/',views.productos_productos_update_rest),
    path('productos_productos_delete_rest/',views.productos_productos_delete_rest),
]