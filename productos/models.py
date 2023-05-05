from django.db import models
import base64
from django.core.files import File
import os
from django.conf import settings
# Create your models here.

class Categoria(models.Model):
    nombre=models.CharField(max_length=150,blank=False,null=False)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.nombre

class Productos(models.Model):
    nombre=models.CharField(max_length=150,blank=False,null=False)
    precio=models.CharField(max_length=20,blank=False,null=False)
    fecha_elaboracion=models.DateField(auto_now=False,auto_now_add=False)
    fecha_vencimiento=models.DateField(auto_now=False,auto_now_add=False)
    categoria=models.CharField(max_length=150,blank=False,null=False)
    imagen=models.ImageField(upload_to='productos/',blank=False,null=True)
    def imagen_base64(self):
        if self.imagen and hasattr(self.imagen, 'url'):
            with self.imagen.open(mode='rb') as f:
                img_data = f.read()
            return base64.b64encode(img_data).decode('utf-8')
        else:
            return None
    def save(self, *args, **kwargs):
        if not self.imagen:
            # asigna la imagen por defecto si no se ha proporcionado una imagen
            img_path = os.path.join(settings.MEDIA_ROOT, 'productos\default.jpg')
            with open(img_path, 'rb') as f:
                self.imagen.save('productos/default.jpg', File(f), save=False)
        super(Productos, self).save(*args, **kwargs)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.nombre
    