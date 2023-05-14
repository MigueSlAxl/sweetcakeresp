from django.db import models
from ordendecompra.models import OrdenDC
from django.db.models.signals import post_save
# Create your models here.
class Insumos(models.Model):
    nombre_insumo=models.CharField(max_length=150,blank=False,null=False)
    ordendc=models.ForeignKey(OrdenDC,on_delete=models.CASCADE)
    cantidad=models.IntegerField(blank=False,null=False)
    preciounidad=models.IntegerField(blank=False,null=False)
    estado=models.CharField(max_length=150,blank=False,null=False)
    imagen_insumo=models.ImageField(upload_to='insumo/',blank=False,null=True)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.nombre_insumo
    
def create_insumos(sender, instance, created, **kwargs):
    if created:
        Insumos.objects.create(ordendc=instance,cantidad=instance.cantidad,preciounidad=(instance.costotal/instance.cantidad),nombre_insumo=instance.proveedor.tipo_insumo,estado='En progreso',imagen_insumo=instance.proveedor.imagen_insumo)

post_save.connect(create_insumos, sender=OrdenDC)