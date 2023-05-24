from rest_framework import serializers,status
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from django.http import JsonResponse
from rest_framework.response import Response

from supplies.models import Supplies
from .models import OrdenDC
# Create your views here.

class OrdendcSerializadorImagenJson(serializers.ModelSerializer):
    class Meta:
        model=OrdenDC
        fields=['id','fecha','proveedor','cantidad','costotal']

@api_view(['POST'])
def ordendc_ordendc_add_rest(request, format=None):
    if request.method == 'POST':
        serializer = OrdendcSerializadorImagenJson(data=request.data)
        if serializer.is_valid():
            ordendc = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['GET'])
def ordendc_ordendc_list_rest(request, format=None):
    if request.method == 'GET':
        ordendc_list = OrdenDC.objects.all()
        ordendc_json = []
        for es in ordendc_list:
            ordendc_json.append({'id':es.id,'fecha':es.fecha,'cantidad':es.cantidad,'costotal':es.costotal,'proveedor':es.proveedor.id})
        return Response({'ListOdc':ordendc_json})
    else:
        return Response({'Msj':"Error método no soportado"})

    
@api_view(['POST'])
def ordendc_ordendc_update_rest(request, format=None):
    if request.method == 'POST':
        try:
            ordendc_id=request.data['id']
            proveedor=request.data['proveedor']
            cantidad=request.data['cantidad']
            costotal=request.data['costotal']
            if proveedor != '':
                OrdenDC.objects.filter(pk=ordendc_id).update(proveedor=proveedor)
                OrdenDC.objects.filter(pk=ordendc_id).update(cantidad=cantidad)
                OrdenDC.objects.filter(pk=ordendc_id).update(costotal=costotal)
                ordendc_json=[]
                ordendc_array = OrdenDC.objects.get(pk=ordendc_id)
                ordendc_json.append({'id':ordendc_array.id,'proveedor':ordendc_array.proveedor,'cantidad':ordendc_array.cantidad,'costotal':ordendc_array.costotal})
                return Response({'Msj':"Datos Actualizados",ordendc_array.nombre:ordendc_json})
            else:
                return Response({'Msj': "Error los datos no pueden estar en blanco"})
        except OrdenDC.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})
    
@api_view(['POST'])
def ordendc_ordendc_delete_rest(request, format=None):
    if request.method =='POST':
        try: 
            id = request.data['id']
            if isinstance(id, int):
                ordendc=OrdenDC.objects.get(pk=id)
                ordendc.delete()
                return Response({'Categoria eliminada con éxito'})
            else:
                return Response({'Ingrese un número entero'})
        except OrdenDC.DoesNotExist:
            return Response({'No existe la ID en la BBDD'})
        except ValueError:
            return Response({'Dato inválido'})
    else: 
        return Response({"Error método no soportado"})
    
@api_view(['GET'])
def ordendc_ordendc_list_supplies_rest(request, format=None):
    if request.method == 'GET':
        ordendc_list = OrdenDC.objects.filter(supplies__estado='En progreso')
        ordendc_json = []
        for es in ordendc_list:
            ordendc_json.append({'id':es.id,'fecha':es.fecha,'cantidad':es.cantidad,'costotal':es.costotal,'proveedor':es.proveedor.id})
        return Response({'ListOdc':ordendc_json})
    else:
        return Response({'Msj':"Error método no soportado"})
    
@api_view(['POST'])
def ordendc_ordendc_update_status_rest(request, format=None):
    if request.method =='POST':
        try: 
            id = request.data['id']
            if isinstance(id, int):
                supplies=Supplies.objects.filter(ordendc=id).update(estado='Correcto')
                return Response({'Orden recibida con exito'})
            else:
                return Response({'Ingrese un número entero'})
        except OrdenDC.DoesNotExist:
            return Response({'No existe la ID en la BBDD'})
        except ValueError:
            return Response({'Dato inválido'})
    else: 
        return Response({"Error método no soportado"})