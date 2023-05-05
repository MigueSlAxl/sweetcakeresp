from io import BytesIO
from django.shortcuts import render
from rest_framework import generics, viewsets, serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from drf_extra_fields.fields import Base64ImageField
from django.http import JsonResponse
import base64
from productos.models import Productos
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
import os
# Create your views here.
class ProductoSerializadorImagenJson(serializers.ModelSerializer):
    imagen=Base64ImageField(required=False)
    class Meta:
        model=Productos
        fields=['id','nombre','precio','fecha_elaboracion','fecha_vencimiento','categoria','imagen']

@api_view(['POST'])
def productos_productos_add_rest(request, format=None):
    if request.method == 'POST':
        serializer = ProductoSerializadorImagenJson(data=request.data)
        if serializer.is_valid():
            producto = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ProductosSerializer(serializers.ModelSerializer):
    imagen = serializers.SerializerMethodField()

    class Meta:
        model = Productos
        fields = ('id', 'nombre', 'precio', 'fecha_elaboracion', 'fecha_vencimiento', 'categoria', 'imagen')

    def get_imagen(self, obj):
        return obj.imagen_base64()
    
@api_view(['GET'])
def productos_productos_list_rest(request, format=None):
    if request.method == 'GET':
        productos_list = Productos.objects.all()
        serializer = ProductosSerializer(productos_list, many=True)
        return JsonResponse({'List': serializer.data}, safe=False)
    else:
        return Response({'Msj':"Error método no soportado"})

@api_view(['POST'])
def productos_productos_update_rest(request, format=None):
    if request.method == 'POST':
        try:
            producto_id=request.data['productoId']
            nombre= request.data['nombre']
            categoria = request.data['categoria']
            precio = request.data['precio']
            fecha_elaboracion = request.data['fecha_elaboracion']
            fecha_vencimiento = request.data['fecha_vencimiento']
            imagen=request.data.get('imagen')  # Usar get() para evitar KeyError si la imagen no está presente
            # Si imagen no tiene ningún valor, establecer imagen_data como None y cargar una imagen predeterminada
            if imagen:
                # Procesar la imagen
                # data = imagen.split(',', 1)[1]  # Remover el prefijo 'data:image/png;base64,'
                image_data = base64.b64decode(imagen)
                image = Image.open(ContentFile(image_data))

                # Guardar la imagen en el modelo de base de datos
                producto = Productos.objects.get(pk=producto_id)
                producto.nombre = nombre
                producto.categoria = categoria
                producto.precio = precio
                producto.fecha_elaboracion = fecha_elaboracion
                producto.fecha_vencimiento = fecha_vencimiento
                producto.imagen.save(f'{producto_id}.png', ContentFile(image_data), save=True)
            else:
                # Si no se proporciona una imagen, establecer imagen_data como None y cargar la imagen predeterminada
                image_path = os.path.join(settings.MEDIA_ROOT, 'productos/default.jpg')
                with open(image_path, 'rb') as f:
                    image_data = f.read()

                # Guardar la imagen predeterminada en el modelo de base de datos
                producto = Productos.objects.get(pk=producto_id)
                producto.nombre = nombre
                producto.categoria = categoria
                producto.precio = precio
                producto.fecha_elaboracion = fecha_elaboracion
                producto.fecha_vencimiento = fecha_vencimiento
                producto.imagen.save(f'{producto_id}.png', ContentFile(image_data), save=True)
            
            # Serializar los datos y enviar la respuesta
            producto_array = Productos.objects.get(pk=producto_id)
            producto_json={'id':producto_array.id,'nombre':producto_array.nombre,'categoria':producto_array.categoria,'fecha_elaboracion':producto_array.fecha_elaboracion,'fecha_vencimiento': producto_array.fecha_vencimiento,'precio':producto_array.precio}
            return Response({'Msj':"Datos Actualizados",producto_array.nombre:[producto_json]}) 
        except Productos.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj':"Metodo no soportado"})

@api_view(['POST'])
def productos_productos_delete_rest(request, format=None):
    if request.method =='POST':
        try: 
            id = request.data['id']
            if isinstance(id, int):
                productos_array=Productos.objects.get(pk=id)
                productos_array.delete()
                return Response({'Producto eliminado con éxito'})
            else:
                return Response({'Ingrese un número entero'})
        except Productos.DoesNotExist:
            return Response({'No existe la ID en la BBDD'})
        except ValueError:
            return Response({'Dato inválido'})
    else: 
        return Response({"Error método no soportado"})