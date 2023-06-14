import base64
from django.db import transaction
import json
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from django.http import JsonResponse
from rest_framework.response import Response
from ordendetrabajo.models import InsumoOrden, OrdenTrabajo, Trabajador
from productos.models import Productos
from supplies.models import Supplies
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
# Create your views here.

@api_view(['POST'])
def ordentrabajo_ordentrabajo_add_rest(request):
    nombre_producto = request.data['nombre_producto']
    precio_producto = request.data['precio_producto']
    estado_producto = request.data['estado_producto']
    cantidad_producto = request.data['cantidad_producto']
    categoria=request.data['categoria']
    imagen=request.data['imagen']
    admin_id = request.data['admin']
    producto = Productos.objects.create(
        nombre=nombre_producto,
        precio=precio_producto,
        estado=estado_producto,
        cantidad=cantidad_producto,
        categoria_id=categoria
    )
    orden_trabajo = OrdenTrabajo.objects.create(producto=producto,
                                            admin_id=admin_id)
    if imagen:
        # Decodificar la imagen base64 y guardarla en el modelo de base de datos
        # ext = format.split('/')[-1]
        image_data = ContentFile(base64.b64decode(imagen), name=f'{producto.id}')
        producto.imagen.save(f'{producto.id}', image_data, save=True)
    productos_creados=[]        
    productos_creados.append({
        'id': producto.id,
        'nombre_producto': producto.nombre,
        'precio_producto': producto.precio,
        'estado_producto': producto.estado,
        'cantidad_producto': producto.cantidad,
        'categoria':producto.categoria.id,
        'admin':orden_trabajo.admin.id,
        
    })
    return Response({'mensaje': 'Órdenes de trabajo creadas correctamente.', 'productos_creados': productos_creados})


@api_view(['GET'])
def ordentrabajo_list_rest(request):
    productos = Productos.objects.filter(estado='Elaboracion')
    productos_data = []

    for producto in productos:
        insumos_utilizados = InsumoOrden.objects.filter(orden_trabajo__producto=producto)
        insumos_data = []
        for insumo_orden in insumos_utilizados:
            insumo_data = {
                'id': insumo_orden.insumo.id,
                'nombre': insumo_orden.insumo.nombre_insumo,
                'cantidad_utilizada': insumo_orden.cantidad_utilizada
            }
            insumos_data.append(insumo_data)
        
        ordenes_trabajo = OrdenTrabajo.objects.filter(producto=producto)
        ordenes_trabajo_data = []
        for orden_trabajo in ordenes_trabajo:
            orden_trabajo_data = {
                'id': orden_trabajo.id,
                'admin': orden_trabajo.admin.id,
                'trabajador': orden_trabajo.trabajador_id,
                'insumos_utilizados': insumos_data
            }
            ordenes_trabajo_data.append(orden_trabajo_data)

        imagen_base64 = ''
        if producto.imagen:
            with open(producto.imagen.path, 'rb') as img_file:
                imagen_data = img_file.read()
                imagen_base64 = base64.b64encode(imagen_data).decode('utf-8')
        
        producto_data = {
            'id': producto.id,
            'nombre_producto': producto.nombre,
            'precio_producto': producto.precio,
            'estado_producto': producto.estado,
            'cantidad_producto': producto.cantidad,
            'lote': producto.lote,
            'fecha_elaboracion': producto.fecha_elaboracion,
            'fecha_vencimiento': producto.fecha_vencimiento,
            'categoria': producto.categoria_id,
            'imagen': imagen_base64,
            'ordenes_trabajo': ordenes_trabajo_data
        }
        productos_data.append(producto_data)

    return Response({"ListTrabajos": productos_data})


@api_view(['POST'])
def ordentrabajo_edit_rest(request):
    # Obtener los datos enviados en la solicitud
    datos = request.data
    if isinstance(datos, str):
        datos = json.loads(datos)

    producto_id = datos.get('producto_id')
    fecha_elaboracion=datos.get('fecha_elaboracion')
    fecha_vencimiento=datos.get('fecha_vencimiento')
    estado=datos.get('estado')
    trabajador_id=datos.get('trabajador')
    imagen_base64 = datos.get('imagen')
    insumos = datos.get('insumos', [])
    
    try:
        # Obtener la Orden de Trabajo que contiene el producto
        ordendetrabajo = OrdenTrabajo.objects.get(producto_id=producto_id)
        producto=Productos.objects.get(pk=producto_id)
        producto.fecha_elaboracion=fecha_elaboracion
        producto.fecha_vencimiento=fecha_vencimiento
        producto.estado=estado
        producto.lote=f"{producto.nombre[:2]}-{producto.categoria_id}"
        producto.save()
        
        with transaction.atomic():
            insumos_agregados = []
            for insumo_data in insumos:
                insumo_id = insumo_data.get('insumo_id')
                cantidad_utilizada = insumo_data.get('cantidad_utilizada')
                
                # Verificar si el insumo ya está agregado a la orden de trabajo
                if InsumoOrden.objects.filter(orden_trabajo=ordendetrabajo, insumo_id=insumo_id).exists():
                    # El insumo ya está agregado, se puede actualizar la cantidad utilizada si es necesario
                    insumo_orden = InsumoOrden.objects.get(orden_trabajo=ordendetrabajo, insumo_id=insumo_id)
                    insumo_orden.cantidad_utilizada =insumo_orden.cantidad_utilizada+ cantidad_utilizada
                    insumo_orden.save()
                else:
                    # El insumo no está agregado, se crea una nueva instancia de InsumoOrden
                    insumo = Supplies.objects.get(id=insumo_id)
                    insumo_orden = InsumoOrden.objects.create(
                        orden_trabajo=ordendetrabajo,
                        insumo=insumo,
                        cantidad_utilizada=cantidad_utilizada
                    )
                
                # Agregar los datos del insumo a la lista de insumos agregados
                insumo_agregado = {
                    'insumo_id': insumo_id,
                    'cantidad_utilizada': cantidad_utilizada
                }
                insumos_agregados.append(insumo_agregado)
            if imagen_base64:
                format, imgstr = imagen_base64.split(';base64,')
                ext = format.split('/')[-1]
                image_data = ContentFile(base64.b64decode(imgstr), name=f'{producto.id}.{ext}')
                producto.imagen.save(f'{producto.id}.{ext}', image_data, save=True)

            producto_data = {
            'id': producto.id,
            'nombre_producto': producto.nombre,
            'precio_producto': producto.precio,
            'estado_producto': producto.estado,
            'cantidad_producto': producto.cantidad,
            'lote': producto.lote,
            'fecha_elaboracion': producto.fecha_elaboracion,
            'fecha_vencimiento': producto.fecha_vencimiento,
            'categoria': producto.categoria_id,
            'trabajador':ordendetrabajo.trabajador_id,
            'insumos_utilizados': insumos_agregados
        }
            
            
            return Response({'mensaje': 'Insumos agregados correctamente.','producto_actualizado': producto_data})
    
    except OrdenTrabajo.DoesNotExist:
        return Response({'error': 'No se encontró una Orden de Trabajo para el producto especificado.'}, status=404)
    
