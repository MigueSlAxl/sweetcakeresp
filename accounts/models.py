from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect
import os
from django.core.files import File
import base64
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo=models.CharField(max_length=150,blank=True,null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1) 
    token_app_session = models.CharField(max_length = 240,null=True, blank=True, default='')
    rut = models.CharField(max_length=12, blank=True, null=True, verbose_name='RUT')
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name='direcciones')
    ntelefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='numero de telefono')
    nemergencia = models.CharField(max_length=15, blank=True, null=True, verbose_name='numero de emergencia')
    local = models.CharField(max_length=50, blank=True, null=True, verbose_name='locales')
    reset_code = models.CharField(max_length=6, null=True, blank=True)
    imagen_user = models.ImageField(upload_to='accounts/', blank=False, null=True)
    def imagen_base64(self):
        if self.imagen_user and hasattr(self.imagen_user, 'url'):
            with self.imagen_user.open(mode='rb') as f:
                img_data = f.read()
            return base64.b64encode(img_data).decode('utf-8')
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.imagen_user:
            # asigna la imagen por defecto si no se ha proporcionado una imagen
            img_path = os.path.join(settings.MEDIA_ROOT, 'accounts/default.jpg')
            with open(img_path, 'rb') as f:
                self.imagen_user.save('default.jpg', File(f), save=False)
        super(Profile, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['user__username']



