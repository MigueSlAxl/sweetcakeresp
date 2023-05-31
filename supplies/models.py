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
    fecha_llegada = models.DateField(auto_now_add=True,blank=True, null=False)
    fecha_vencimiento = models.DateField(auto_now_add=True , blank=True, null=False)
    preciounidad=models.IntegerField(blank=False,null=False)
    proveedor = models.CharField(max_length= 30, blank= False , null= False)
    estado=models.CharField(max_length=150,blank=True,null=True)
    tipo_insumo = models.CharField (max_length=40 , blank = False , null= False)
    numero_lote= models.CharField(max_length=40 , blank = True , null= True)
    marca_producto = models.CharField (max_length=40 , blank = True , null= True)
    cantidad = models.IntegerField ( blank = False , null= False)
    imagen_supplies = models.ImageField (upload_to="insumo/",null=True, blank=True)
    def imagen_base64(self):
        if self.imagen_supplies and hasattr(self.imagen_supplies, 'url'):
            with self.imagen_supplies.open(mode='rb') as f:
                img_data = f.read()
            return base64.b64encode(img_data).decode('utf-8')
        else:
            return None
    def save(self, *args, **kwargs):
        if not self.imagen_supplies:
            # asigna la imagen por defecto si no se ha proporcionado una imagen
            img_path = os.path.join(settings.MEDIA_ROOT, 'insumo/default.jpg')
            with open(img_path, 'rb') as f:
                self.imagen_supplies.save('default.jpg', File(f), save=False)
        super(Supplies, self).save(*args, **kwargs)    
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
            nombre_insumo="Por asignar",
            proveedor= instance.proveedor.nombre_proveedor,
            estado='En progreso',
            tipo_insumo = instance.proveedor.tipo_insumo, 
            marca_producto = 'Por asignar',
            imagen_supplies=instance.proveedor.imagen_insumo, 
            numero_lote = str(instance.proveedor.id)  + str(instance.id) + str(instance.fecha.strftime("%Y%m%d%H%M"))
        )

post_save.connect(create_supplies, sender=OrdenDC)



