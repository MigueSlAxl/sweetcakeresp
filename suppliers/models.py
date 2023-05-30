from django.db import models
import base64
from django.core.files import File
import os
from django.conf import settings

# Create your models here.
class Supplier(models.Model):
    rut=models.CharField(max_length=150,blank=False,null=False)
    nombre_proveedor=models.CharField(max_length=150,blank=False,null=False)
    tipo_insumo=models.CharField(max_length=150,blank=False,null=False)
    imagen_insumo=models.ImageField(upload_to='insumo/',blank=False,null=True)
    correo_proveedor=models.EmailField(max_length=150,blank=False,null=False)
    telefono_proveedor=models.CharField(max_length=12,blank=False,null=False)
    def imagen_base64(self):
        if self.imagen_insumo and hasattr(self.imagen_insumo, 'url'):
            with self.imagen_insumo.open(mode='rb') as f:
                img_data = f.read()
            return base64.b64encode(img_data).decode('utf-8')
        else:
            return None
    def save(self, *args, **kwargs):
        if not self.imagen_insumo:
            # asigna la imagen por defecto si no se ha proporcionado una imagen
            img_path = os.path.join(settings.MEDIA_ROOT, 'insumo/default.jpg')
            with open(img_path, 'rb') as f:
                self.imagen_insumo.save('default.jpg', File(f), save=False)
        super(Supplier, self).save(*args, **kwargs)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.nombre_proveedor
