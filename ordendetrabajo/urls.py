from django.urls import path
from ordendetrabajo import views
# Create your views here.
ordendetrabajo_urlpatterns=[
    path('ordentrabajo_add_rest/',views.ordentrabajo_ordentrabajo_add_rest),
    path('ordentrabajo_list_rest/',views.ordentrabajo_list_rest),
    path('ordentrabajo_edit_rest/',views.ordentrabajo_edit_rest),
    ]