from django.shortcuts import render
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from .models import Supplier
from django.http import JsonResponse
from rest_framework.response import Response
# Create your views here.

@api_view(['POST'])
def suppliers_suppliers_add_rest(request, format=None):
    if request.method == 'POST':
            nombre_proveedor=request.data['nombre_proveedor']
            rut=request.data['rut']
            tipo_insumo=request.data['tipo_insumo']
            correo_proveedor=request.data['correo_proveedor']
            telefono_proveedor=request.data['telefono_proveedor']
            Categoria_save = Supplier(
                nombre = nombre_proveedor,
                rut=rut,
                tipo_insumo=tipo_insumo,
                correo_proveedor=correo_proveedor,
                telefono_proveedor=telefono_proveedor,
                )
            Categoria_save.save()
            return Response({'Msj':"Proveedor Creada"})
    else:
       return Response({'Msj': "Error método no soportado"})
    

@api_view(['GET'])
def suppliers_suppliers_list_rest(request, format=None):
    if request.method == 'GET':
        suppliers_list = Supplier.objects.all()
        suppliers_json = []
        for es in suppliers_list:
            suppliers_json.append({'id':es.id,'nombre_proveedor':es.nombre_proveedor,'rut':es.rut,'tipo_insumo':es.tipo_insumo,'correo_proveedor':es.correo_proveedor,'telefono_proveedor':es.telefono_proveedor})
        return Response({'ListSup':suppliers_json})
    else:
        return Response({'Msj':"Error método no soportado"})
    
@api_view(['POST'])
def suppliers_suppliers_update_rest(request, format=None):
    if request.method == 'POST':
        try:
            id=request.data['id']
            nombre_proveedor=request.data['nombre_proveedor']
            rut=request.data['rut']
            tipo_insumo=request.data['tipo_insumo']
            correo_proveedor=request.data['correo_proveedor']
            telefono_proveedor=request.data['telefono_proveedor']
            if nombre_proveedor != '':
                Supplier.objects.filter(pk=id).update(nombre_proveedor=nombre_proveedor)
                Supplier.objects.filter(pk=id).update(rut=rut)
                Supplier.objects.filter(pk=id).update(tipo_insumo=tipo_insumo)
                Supplier.objects.filter(pk=id).update(correo_proveedor=correo_proveedor)
                Supplier.objects.filter(pk=id).update(telefono_proveedor=telefono_proveedor)
                suppliers_json=[]
                suppliers_array = Supplier.objects.get(pk=id)
                suppliers_json.append({'id':suppliers_array.id,
                                       'nombre':suppliers_array.nombre_proveedor,
                                       'rut':suppliers_array.rut,
                                       'tipo_insumo':suppliers_array.tipo_insumo,
                                       'correo_proveedor':suppliers_array.correo_proveedor,
                                       'telefono_proveedor':suppliers_array.telefono_proveedor})
                return Response({'Msj':"Datos Actualizados",suppliers_array.nombre_proveedor:suppliers_json}) 
            else:
                return Response({'Msj': "Error los datos no pueden estar en blanco"})
        except Supplier.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})
        
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