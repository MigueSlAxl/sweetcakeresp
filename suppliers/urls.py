from django.urls import path,include
from suppliers import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


suppliers_urlpatterns=[
    path('suppliers_suppliers_add_rest/',views.suppliers_suppliers_add_rest),
    path('suppliers_suppliers_list_rest/',views.suppliers_suppliers_list_rest),
    path('suppliers_suppliers_update_rest/',views.suppliers_suppliers_update_rest),
    path('suppliers_suppliers_delete_rest/',views.suppliers_suppliers_delete_rest),
    ]