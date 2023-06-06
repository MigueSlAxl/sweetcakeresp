import json
from rest_framework import serializers,status
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from django.http import JsonResponse
from rest_framework.response import Response

from productos.models import Productos
from .models import Venta,VentaDetalle

@api_view(['POST'])
def ventas_ventas_add_rest(request):
    datos = request.data
    if isinstance(datos, str):
        datos = json.loads(datos)
    venta = Venta.objects.create(total=0)  # Asignamos un valor inicial al campo total
    total_venta = 0
    productos = datos['productos']
    for item in productos:
        id = item['id']
        cantidad = item['cantidad']
        producto = Productos.objects.get(pk=id)
        producto.cantidad =producto.cantidad - cantidad
        if producto.cantidad<=0:
            producto.estado='Vendido'
        producto.save()
        venta_detalle = VentaDetalle.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio,
        )
        subtotal = producto.precio * cantidad
        total_venta += subtotal
    venta.total = total_venta
    venta.save()
    return Response({'mensaje': 'Cantidad actualizada correctamente.'})

@api_view(['GET'])
def ventas_ventas_list_rest(request):
    ventas = Venta.objects.all()
    resultado = []
    for venta in ventas:
        detalles_venta = VentaDetalle.objects.filter(venta=venta)
        productos = []
        total_venta = 0
        for detalle in detalles_venta:
            producto = detalle.producto
            producto_info = {
                'id': producto.id,
                'nombre': producto.nombre,
                'cantidad': detalle.cantidad,
                'precio_unitario': detalle.precio_unitario,
                'precio_total': detalle.cantidad * detalle.precio_unitario
            }
            productos.append(producto_info)
            total_venta += detalle.cantidad * detalle.precio_unitario

        venta_info = {
            'id_venta': venta.id,
            'fecha': venta.fecha,
            'total': total_venta,
            'productos': productos
        }
        resultado.append(venta_info)

    respuesta = {'listventas': resultado}
    return Response(respuesta)