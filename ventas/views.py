from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
import json
import os
import smtplib
from django.urls import reverse
from rest_framework import serializers,status
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from django.http import JsonResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
from productos.models import Productos
from .models import Venta,VentaDetalle
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import Profile
@api_view(['POST'])
def ventas_ventas_add_rest(request):
    datos = request.data
    if isinstance(datos, str):
        datos = json.loads(datos)
    venta = Venta.objects.create(total=0)
    user = request.data['vendedor']
    email=request.data['email']
    nombre = User.objects.get(id=user)
    profile=Profile.objects.get(user=user)
    venta.vendedor = nombre.first_name + ' ' + nombre.last_name
    total_venta = 0
    productos = datos['productos']
    for item in productos:
        id = item['id']
        cantidad = item['cantidad']
        producto = Productos.objects.get(pk=id)
        producto.cantidad = producto.cantidad - cantidad
        if producto.cantidad <= 0:
            producto.estado = 'Vendido'
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
    
    detalle_venta = {
        'vendedor': venta.vendedor,
        'fecha': venta.fecha,
        'local':profile.local,
        'total': venta.total,
        'productos': [
            {
                'id': venta_detalle.producto.id,
                'nombre': venta_detalle.producto.nombre,
                'cantidad': venta_detalle.cantidad,
                'precio_unitario': venta_detalle.precio_unitario,
                'total_producto':(venta_detalle.cantidad*venta_detalle.precio_unitario)
            }
            for venta_detalle in venta.ventadetalle_set.all()
        ]
    }
    html_string = render_to_string('ventas/detalle_venta.html', {'detalle_venta': detalle_venta})
    pdf_file = BytesIO()
    pisa.CreatePDF(html_string, dest=pdf_file)
    pdf_file.seek(0)
    email=request.data['email']
    if email!='':
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER 
        msg['To'] = email
        msg['Subject'] = 'Boleta SweetCake'
        message = MIMEText('Compra Realizada en Sweetcake', 'plain')
        msg.attach(message)
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(pdf_file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename='detalle_venta.pdf')
        msg.attach(part)

        # Enviar el mensaje utilizando el servidor SMTP
        smtp_server = settings.EMAIL_HOST  # Servidor SMTP desde la configuración
        smtp_port = settings.EMAIL_PORT  # Puerto SMTP desde la configuración
        smtp_username = settings.EMAIL_HOST_USER  # Usuario SMTP desde la configuración
        smtp_password = settings.EMAIL_HOST_PASSWORD  # Contraseña SMTP desde la configuración
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
    return Response({'detalle_venta': detalle_venta})


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
            'vendedor':venta.vendedor,
            'fecha': venta.fecha,
            'total': total_venta,
            'productos': productos
        }
        resultado.append(venta_info)

    respuesta = {'listventas': resultado}
    return Response(respuesta)

@api_view(['POST'])
def ventas_ventas_delete_rest(request, format=None):
    if request.method =='POST':
        try: 
            id = request.data['id']
            if isinstance(id, int):
                venta=Venta.objects.get(pk=id)
                venta.delete()
                return Response({'Venta eliminada con éxito'})
            else:
                return Response({'Ingrese un número entero'})
        except Venta.DoesNotExist:
            return Response({'No existe la ID en la BBDD'})
        except ValueError:
            return Response({'Dato inválido'})
    else: 
        return Response({"Error método no soportado"})