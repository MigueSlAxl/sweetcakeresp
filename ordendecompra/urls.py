from django.urls import path
from ordendecompra import views


ordendc_urlpatterns=[
    path('ordendc_ordendc_add_rest/',views.ordendc_ordendc_add_rest),
]