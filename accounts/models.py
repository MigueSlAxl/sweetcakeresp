from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
import os
from django.core.files import File
import base64
from django.conf import settings
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
            img_path = os.path.join(settings.MEDIA_ROOT, 'accounts/default1.jpg')
            with open(img_path, 'rb') as f:
                self.imagen.save('accounts/default1.jpg', File(f), save=False)
        super(User, self).save(*args, **kwargs)

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
