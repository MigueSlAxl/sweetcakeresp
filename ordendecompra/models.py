from django.db import models
from suppliers.models import Supplier
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class OrdenDC(models.Model):
    fecha=models.DateTimeField(auto_now_add=True)
    proveedor=models.ForeignKey(Supplier,on_delete=models.CASCADE)
    cantidad=models.IntegerField(default=0,blank=False,null=False)
    costotal=models.IntegerField(default=0,blank=False,null=False)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.proveedor.nombre_proveedor