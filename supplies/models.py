from django.db import models
import os
from django.conf import settings
import base64
from django.core.files import File


# Create your models here.
class Supplies(models.Model): 
    nombre_insumo = models.CharField(max_length=40 , blank = False , null= False)
    fecha_llegada  = models.DateField( auto_now= False , auto_now_add= False)
    fecha_vencimiento = models.DateField( auto_now= False , auto_now_add= False )
    proveedor = models.CharField(max_length= 30, blank= False , null= False)
    tipo_insumo = models.CharField (max_length=40 , blank = False , null= False)
    numero_lote= models.CharField(max_length=40 , blank = False , null= False)
    marca_producto = models.CharField (max_length=40 , blank = False , null= False)
    cantidad = models.IntegerField ( blank = False , null= False)
    imagen_supplies = models.ImageField (upload_to="supplies/",null=True, blank=True)
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
            img_path = os.path.join(settings.MEDIA_ROOT, 'supplies/default2.jpg')
            with open(img_path, 'rb') as f:
                self.imagen_supplies.save('supplies/default2.jpg', File(f), save=False)
        super(Supplies, self).save(*args, **kwargs)


    class Meta : 
        ordering = ['id']


    def __str__(self) : 
        return self.nombre_insumo
    
    
    
    
    