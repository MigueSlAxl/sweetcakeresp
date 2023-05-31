import base64
import os
from django.shortcuts import render
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from .models import Supplier
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets, serializers,status
from drf_extra_fields.fields import Base64ImageField
from django.conf import settings
from PIL import Image
from django.core.files.base import ContentFile
# Create your views here.

class SupplierSerializadorImagenJson(serializers.ModelSerializer):
    imagen_insumo=Base64ImageField(required=False)
    class Meta:
        model=Supplier
        fields=['id','nombre_proveedor','rut','tipo_insumo','correo_proveedor','telefono_proveedor','imagen_insumo']

@api_view(['POST'])
def suppliers_suppliers_add_rest(request, format=None):
    if request.method == 'POST':
        serializer = SupplierSerializadorImagenJson(data=request.data)
        if serializer.is_valid():
            supplier = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SupplierSerializer(serializers.ModelSerializer):
    imagen_insumo = serializers.SerializerMethodField()
    class Meta:
        model = Supplier
        fields = ('id','nombre_proveedor','rut','tipo_insumo','correo_proveedor','telefono_proveedor','imagen_insumo')

    def get_imagen_insumo(self, obj):
        return obj.imagen_base64()
    
@api_view(['GET'])
def suppliers_suppliers_list_rest(request, format=None):
    if request.method == 'GET':
        supplier_list = Supplier.objects.all()
        serializer = SupplierSerializer(supplier_list, many=True)
        return JsonResponse({'ListSup': serializer.data}, safe=False)
    else:
        return Response({'Msj':"Error método no soportado"})

@api_view(['POST'])
def suppliers_suppliers_update_rest(request, format=None):
    if request.method == 'POST':
        try:
            id=request.data['supplierId']
            nombre_proveedor= request.data['nombre_proveedor']
            tipo_insumo = request.data['tipo_insumo']
            rut = request.data['rut']
            correo_proveedor = request.data['correo_proveedor']
            telefono_proveedor = request.data['telefono_proveedor']
            imagen=request.data.get('imagen_insumo')  # Usar get() para evitar KeyError si la imagen no está presente
            # Si imagen no tiene ningún valor, establecer imagen_data como None y cargar una imagen predeterminada
            if imagen:
                # Procesar la imagen
                # data = imagen.split(',', 1)[1]  # Remover el prefijo 'data:image/png;base64,'
                image_data = base64.b64decode(imagen)
                # image = Image.open(ContentFile(image_data))

                # Guardar la imagen en el modelo de base de datos
                supplier = Supplier.objects.get(pk=id)
                supplier.nombre_proveedor = nombre_proveedor
                supplier.rut = rut
                supplier.tipo_insumo =tipo_insumo
                supplier.correo_proveedor= correo_proveedor
                supplier.telefono_proveedor = telefono_proveedor
                supplier.imagen_insumo.save(f'{id}.png', ContentFile(image_data), save=True)
            else:
                # Si no se proporciona una imagen, establecer imagen_data como None y cargar la imagen predeterminada
                image_path = os.path.join(settings.MEDIA_ROOT, 'suppliers/default.jpg')
                with open(image_path, 'rb') as f:
                    image_data = f.read()

                # Guardar la imagen predeterminada en el modelo de base de datos
                supplier = Supplier.objects.get(pk=id)
                supplier.nombre_proveedor = nombre_proveedor
                supplier.rut = rut
                supplier.tipo_insumo =tipo_insumo
                supplier.correo_proveedor= correo_proveedor
                supplier.telefono_proveedor = telefono_proveedor
                supplier.imagen_insumo.save(f'{id}.png', ContentFile(image_data), save=True)
            
            # Serializar los datos y enviar la respuesta
            supplier_array = Supplier.objects.get(pk=id)
            supplier_json={'id':supplier_array.id,'nombre_proveedor':supplier_array.nombre_proveedor,'rut':supplier_array.rut,'tipo_insumo':supplier_array.tipo_insumo,'correo_proveedor': supplier_array.correo_proveedor,'telefono_proveedor':supplier_array.telefono_proveedor}
            return Response({'Msj':"Datos Actualizados",supplier_array.nombre_proveedor:[supplier_json]}) 
        except Supplier.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj':"Metodo no soportado"})
        
@api_view(['POST'])
def suppliers_suppliers_delete_rest(request, format=None):
    if request.method =='POST':
        try: 
            id = request.data['id']
            if isinstance(id, int):
                suppliers_array=Supplier.objects.get(pk=id)
                suppliers_array.delete()
                return Response({'Proveedor eliminado con éxito'})
            else:
                return Response({'Ingrese un número entero'})
        except Supplier.DoesNotExist:
            return Response({'No existe la ID en la BBDD'})
        except ValueError:
            return Response({'Dato inválido'})
    else: 
        return Response({"Error método no soportado"})
    