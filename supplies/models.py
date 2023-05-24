from django.db import models
import os
from django.conf import settings
import base64
from django.core.files import File
from ordendecompra.models import OrdenDC
from django.db.models.signals import post_save
from datetime import datetime



# Create your models here.
class Supplies(models.Model): 
    nombre_insumo = models.CharField(max_length=40 , blank = False , null= False)
    ordendc=models.ForeignKey(OrdenDC,on_delete=models.CASCADE)
    fecha_llegada = models.DateField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    preciounidad=models.IntegerField(blank=False,null=False)
    proveedor = models.CharField(max_length= 30, blank= False , null= False)
    estado=models.CharField(max_length=150,blank=True,null=True)
    tipo_insumo = models.CharField (max_length=40 , blank = False , null= False)
    numero_lote= models.CharField(max_length=40 , blank = True , null= True)
    marca_producto = models.CharField (max_length=40 , blank = True , null= True)
    cantidad = models.IntegerField ( blank = False , null= False)
    imagen_supplies = models.ImageField (upload_to="supplies/",null=True, blank=True)
    class Meta : 
        ordering = ['id']
    def __str__(self) : 
        return self.nombre_insumo
    

def create_supplies(sender, instance, created, **kwargs):
    if created:
        Supplies.objects.create(
            ordendc=instance,
            cantidad=instance.cantidad,
            preciounidad=(instance.costotal / instance.cantidad),
            nombre_insumo=instance.proveedor.tipo_insumo,
            proveedor= instance.proveedor.id,
            estado='En progreso',
            imagen_supplies=instance.proveedor.imagen_insumo, 
            numero_lote = str(instance.proveedor.id)  + str(instance.id) + str(instance.fecha.strftime("%Y%m%d%H%M"))
        )

post_save.connect(create_supplies, sender=OrdenDC)



