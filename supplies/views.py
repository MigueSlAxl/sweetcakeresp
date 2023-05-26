from django.shortcuts import render
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from supplies.models import Supplies
from supplies.serializers import SuppliesSerializer
from rest_framework.response import Response
from rest_framework import generics, viewsets, serializers,status
from django.http import JsonResponse
from PIL import Image
import os
from django.core.files.base import ContentFile
from drf_extra_fields.fields import Base64ImageField
import base64
from django.conf import settings


# Create your views here.
@api_view(['POST']) 

def supplies_add_rest(request, format=None):
    if request.method == 'POST' : 
        serializers = SuppliesSerializer (data=request.data)
        if serializers.is_valid():
            supplies = serializers.save()
            return Response (serializers.data , status=status.HTTP_201_CREATED )
        else: 
            return Response (serializers.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST']) 
def supplies_update_rest(request , format =None):
    if request.method == 'POST' : 
        id=request.data ['id']
        nombre_insumo = request.data['nombre_insumo']
        fecha_llegada = request.data['fecha_llegada']
        fecha_vencimiento=request.data['fecha_vencimiento']
        estado=request.data['estado'] 
        marca_producto = request.data['marca_producto']
        cantidad = request.data['cantidad']
        tipo_insumo= request.data['tipo_insumo']
        imagen_supplies=request.data.get('imagen_supplies')
        if imagen_supplies: 
            image_data = base64.b64decode(imagen_supplies)
            image =Image.open(ContentFile(image_data))
            supplies = Supplies.objects.get(pk=id)
            supplies.nombre_insumo = nombre_insumo
            supplies.fecha_llegada = fecha_llegada
            supplies.fecha_vencimiento = fecha_vencimiento
            supplies.tipo_insumo = tipo_insumo
            supplies.marca_producto = marca_producto
            supplies.cantidad = cantidad
            supplies.imagen.save(f'{supplies.id}.png', ContentFile(image_data), save=True)
        else:
                # Si no se proporciona una imagen, establecer imagen_data como None y cargar la imagen predeterminada
                image_path = os.path.join(settings.MEDIA_ROOT, 'supplies/default2.jpg')
                with open(image_path, 'rb') as f:
                    image_data = f.read()
                Supplies.objects.filter(pk=id).update(nombre_insumo= nombre_insumo)
                Supplies.objects.filter(pk=id).update(tipo_insumo= tipo_insumo)
                Supplies.objects.filter(pk=id).update(fecha_llegada= fecha_llegada)
                Supplies.objects.filter(pk=id).update(fecha_vencimiento= fecha_vencimiento)
                Supplies.objects.filter(pk=id).update(estado= estado)
                Supplies.objects.filter(pk=id).update(marca_producto= marca_producto)
                Supplies.objects.filter(pk=id).update(cantidad= cantidad)
                
                supplies_json = []
                supplies_array = Supplies.objects.get(pk=id)
                supplies_json.append({
                    'id'  : supplies_array.id,
                    'nombre_insumo' : supplies_array.nombre_insumo,
                    'fecha_llegada' : supplies_array.fecha_llegada,
                    'fecha_vencimiento' :supplies_array.fecha_vencimiento,
                    'estado' : supplies_array.estado, 
                    'marca_producto' : supplies_array.marca_producto,
                    'tipo_insumo' : supplies_array.tipo_insumo,
                    'cantidad' : supplies_array.cantidad,})

                return Response({'Msj':"Datos Actualizados",supplies_array.nombre_insumo:supplies_json}) 
        if Supplies.DoesNotExist:
                    return Response({'Msj':"Error no hay coincidencias"})
        if ValueError: 
                return Response ({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})
            



@api_view(['GET'])
def supplies_list_rest_estadocorrecto(request, format=None):
    if request.method == 'GET' : 
        supplies_list = Supplies.objects.filter(estado= 'Correcto' or 'correcto')
        serializers = SuppliesSerializer (supplies_list, many = True)
        return JsonResponse({'List' : serializers.data} , safe=False)
    else:
        return Response({'Msj':"Error método no soportado"})



@api_view(['GET'])
def supplies_list_rest_estadoprogreso(request, format=None):
    if request.method == 'GET' : 
        supplies_list = Supplies.objects.filter(estado= 'En progreso' or 'en progreso')
        serializers = SuppliesSerializer (supplies_list, many = True)
        return JsonResponse({'List' : serializers.data} , safe=False)
    else:
        return Response({'Msj':"Error método no soportado"})

@api_view(['GET'])
def supplies_list_rest(request, format=None):
    if request.method == 'GET' : 
        supplies_list = Supplies.objects.all()
        serializers = SuppliesSerializer (supplies_list, many = True)
        return JsonResponse({'List' : serializers.data} , safe=False)
    else:
        return Response({'Msj':"Error método no soportado"})



@api_view(['POST'])
def supplies_delete_rest(request, format=None):
    if request.method != 'POST':
        return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
        id = int(request.data['id'])
    except (KeyError, ValueError):
        return Response({'error': 'Ingrese un número entero'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        supplies = Supplies.objects.get(pk=id)
    except Supplies.DoesNotExist:
        return Response({'error': 'No existe el usuario'}, status=status.HTTP_404_NOT_FOUND)

    supplies.delete()
    return Response({'detail': 'Usuario eliminado con éxito'})
