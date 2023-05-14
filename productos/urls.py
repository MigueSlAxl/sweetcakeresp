from django.urls import path
from productos import views

productos_urlpatterns=[
    path('productos_productos_add_rest/',views.productos_productos_add_rest),
    path('productos_productos_list_rest/',views.productos_productos_list_rest),
    path('productos_productos_update_rest/',views.productos_productos_update_rest),
    path('productos_productos_delete_rest/',views.productos_productos_delete_rest),
    #categoria
    path('productos_categoria_add_rest/',views.productos_categoria_add_rest),
    path('productos_categoria_list_rest/',views.productos_categoria_list_rest),
    path('productos_categoria_update_rest/',views.productos_categoria_update_rest),
    path('productos_categoria_delete_rest/',views.productos_categoria_delete_rest),
]