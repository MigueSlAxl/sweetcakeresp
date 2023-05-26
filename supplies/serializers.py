from rest_framework import generics, viewsets, serializers,status
from supplies.models import Supplies
from drf_extra_fields.fields import Base64ImageField
import base64
from rest_framework.response import Response
from django.http import JsonResponse




class SuppliesSerializer(serializers.ModelSerializer): 
    imagen_supplies = Base64ImageField(required = False)
    class Meta: 
        model = Supplies
        fields =  ( 'id' , 'nombre_insumo', 'fecha_llegada', 'fecha_vencimiento', 'proveedor', 'tipo_insumo','estado',
                    'numero_lote', 'marca_producto',  'cantidad' , 'imagen_supplies')

