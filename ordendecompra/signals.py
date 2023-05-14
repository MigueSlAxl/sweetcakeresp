from django.db.models.signals import post_save
from django.dispatch import receiver
from insumos.models import Insumos

from ordendecompra.models import OrdenDC

@receiver(post_save, sender=OrdenDC)
def crear_insumos(sender, instance, created, **kwargs):
    if created:
        insumos = Insumos.objects.create(cantidad=instance.cantidad,nombre_insumo=instance.proveedor.tipo_insumo)

from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_app'

    def ready(self):
        import my_app.signals