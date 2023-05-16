from django.db import models
import os
from django.conf import settings
import base64
from django.core.files import File
from ordendecompra.models import OrdenDC
from django.db.models.signals import post_save



# Create your models here.
class Supplies(models.Model): 
    nombre_insumo = models.CharField(max_length=40 , blank = False , null= False)
    ordendc=models.ForeignKey(OrdenDC,on_delete=models.CASCADE)
    fecha_llegada  = models.DateField( auto_now= False , auto_now_add= False)
    fecha_vencimiento = models.DateField( auto_now= False , auto_now_add= False )
    preciounidad=models.IntegerField(blank=False,null=False)
    proveedor = models.CharField(max_length= 30, blank= False , null= False)
    estado=models.CharField(max_length=150,blank=True,null=True)
    tipo_insumo = models.CharField (max_length=40 , blank = False , null= False)
    numero_lote= models.CharField(max_length=40 , blank = False , null= False)
    marca_producto = models.CharField (max_length=40 , blank = True , null= True)
    cantidad = models.IntegerField ( blank = False , null= False)
    imagen_supplies = models.ImageField (upload_to="supplies/",null=True, blank=True)
    class Meta : 
        ordering = ['id']
    def __str__(self) : 
        return self.nombre_insumo



def create_supplies(sender, instance, created, **kwargs):
    if created:
        Supplies.objects.create(ordendc=instance,cantidad=instance.cantidad,preciounidad=(instance.costotal/instance.cantidad)
        ,nombre_insumo=instance.proveedor.tipo_insumo,estado='En progreso'
        ,imagen_supplies=instance.proveedor.imagen_insumo, 
        marca_producto= instance.marca_producto, 
        numero_lote= (instance.proveedor.id + instance.ordendc.id +instance.ordendc.fecha))






#falta marca producto ,n lote , fecha_llgada, fecha_vencimiento
#ID PROVEEDOR+ ID ORDENCOMPRA+FECHA CREACION 


post_save.connect(create_supplies, sender=OrdenDC)



