from django.db import models

from productos.models import Productos

# Create your models here.
class Venta(models.Model):
    fecha=models.DateTimeField(auto_now_add=True)
    total=models.PositiveIntegerField(blank=False,null=False)
    vendedor=models.CharField(max_length=150,blank=False,null=False)

class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    precio_unitario = models.PositiveIntegerField(blank=False,null=False)