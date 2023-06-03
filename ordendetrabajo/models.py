from django.db import models
from productos.models import Productos
from supplies.models import Supplies
from django.contrib.auth.models import User
# Create your models here.

class Trabajador(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
class OrdenTrabajo(models.Model):
    admin=models.ForeignKey(User,on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    insumos = models.ManyToManyField(Supplies, through='InsumoOrden')
    trabajador=models.ForeignKey(Trabajador,on_delete=models.CASCADE,null=True)

class InsumoOrden(models.Model):
    orden_trabajo = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Supplies, on_delete=models.CASCADE)
    cantidad_utilizada = models.PositiveIntegerField(null=False)