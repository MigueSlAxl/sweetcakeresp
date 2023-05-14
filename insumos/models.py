from django.db import models
from ordendecompra.models import OrdenDC
# Create your models here.
class Insumos(models.Model):
    nombre_insumo=models.CharField(max_length=150,blank=False,null=False)
    ordendc=models.ForeignKey(OrdenDC,on_delete=models.CASCADE)
    cantidad=models.IntegerField(blank=False,null=False)
    preciounidad=models.IntegerField(blank=False,null=False)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.ordendc.proveedor.tipo_insumo