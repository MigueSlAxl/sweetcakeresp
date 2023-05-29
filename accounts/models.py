from django.db import models
<<<<<<< Updated upstream
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
=======
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect
>>>>>>> Stashed changes
import os
from django.core.files import File
import base64
from django.conf import settings
<<<<<<< Updated upstream
# Create your models here.


class User(AbstractUser):
    
    is_client = models.BooleanField(default=True, verbose_name="Cliente")
    is_admin = models.BooleanField(default=False, verbose_name="Admin")
    imagen = models.ImageField(upload_to='accounts/', blank=False, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='users'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='users'
    )

=======

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo=models.CharField(max_length=150,blank=True,null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1) 
    token_app_session = models.CharField(max_length = 240,null=True, blank=True, default='')
    first_session = models.CharField(max_length = 240,null=True, blank=True, default='Si')
    cargo = models.CharField(max_length=12, blank=True, null=True, verbose_name='cargos')
    rut = models.CharField(max_length=12, blank=True, null=True, verbose_name='RUT')
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name='direcciones')
    ntelefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='numero de telefono')
    nemergencia = models.CharField(max_length=15, blank=True, null=True, verbose_name='numero de emergencia')
    local = models.CharField(max_length=50, blank=True, null=True, verbose_name='locales')
    imagen = models.ImageField(upload_to='accounts/', blank=False, null=True)
>>>>>>> Stashed changes
    def imagen_base64(self):
        if self.imagen and hasattr(self.imagen, 'url'):
            with self.imagen.open(mode='rb') as f:
                img_data = f.read()
            return base64.b64encode(img_data).decode('utf-8')
        else:
            return None
<<<<<<< Updated upstream

    def save(self, *args, **kwargs):
        if not self.imagen:
            # asigna la imagen por defecto si no se ha proporcionado una imagen
            img_path = os.path.join(settings.MEDIA_ROOT, 'accounts/default1.jpg')
            with open(img_path, 'rb') as f:
                self.imagen.save('accounts/default1.jpg', File(f), save=False)
        super(User, self).save(*args, **kwargs)
=======
>>>>>>> Stashed changes

    def save(self, *args, **kwargs):
        if not self.imagen:
            # asigna la imagen por defecto si no se ha proporcionado una imagen
            img_path = os.path.join(settings.MEDIA_ROOT, 'accounts/default.jpg')
            with open(img_path, 'rb') as f:
                self.imagen.save('default.jpg', File(f), save=False)
        super(Profile, self).save(*args, **kwargs)
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"





class UserStandard(User):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='userstandard')
    cargo = models.CharField(max_length=12, verbose_name="cargo", default="")
    rut = models.CharField(max_length=12, blank=True, null=True, verbose_name='RUT')
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name='direccion')
    ntelefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='numero de telefono')
    nemergencia = models.CharField(max_length=15, blank=True, null=True, verbose_name='numero de emergencia')
    local = models.CharField(max_length=50, blank=True, null=True, verbose_name='local')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at = models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)


    class Meta:
        verbose_name = "userstandard"
        verbose_name_plural = "usersstandard"
    
    def __str__(self):
        return self.user.username
