from rest_framework import serializers,status
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from django.http import JsonResponse
from rest_framework.response import Response
from .models import OrdenDC
# Create your views here.

class OrdendcSerializadorImagenJson(serializers.ModelSerializer):
    class Meta:
        model=OrdenDC
        fields=['id','fecha','proveedor','cantidad','costototal']

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
            ordendc_json.append({'id':es.id,'nombre':es.fecha,'cantidad':es.cantidad,'costotal':es.costotal,'proveedor':es.proveedor})
        return Response({'ListODC':ordendc_json})
    else:
        return Response({'Msj':"Error método no soportado"})