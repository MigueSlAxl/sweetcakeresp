from django.urls import path,include
from django.shortcuts import render
from ventas import views
# Create your views here.
ventas_urlpatterns=[
    path('ventas_ventas_add_rest/',views.ventas_ventas_add_rest),
    path('ventas_ventas_list_rest/',views.ventas_ventas_list_rest),
    path('ventas_ventas_delete_rest/',views.ventas_ventas_delete_rest),
    ]