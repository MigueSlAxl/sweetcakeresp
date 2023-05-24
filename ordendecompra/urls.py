from django.urls import path
from ordendecompra import views


ordendc_urlpatterns=[
    path('ordendc_ordendc_add_rest/',views.ordendc_ordendc_add_rest),
    path('ordendc_ordendc_list_rest/',views.ordendc_ordendc_list_rest),
    path('ordendc_ordendc_update_rest/',views.ordendc_ordendc_update_rest),
    path('ordendc_ordendc_delete_rest/',views.ordendc_ordendc_delete_rest),
    path('ordendc_ordendc_list_supplies_rest/',views.ordendc_ordendc_list_supplies_rest),
    path('ordendc_ordendc_update_status_rest/',views.ordendc_ordendc_update_status_rest),
]