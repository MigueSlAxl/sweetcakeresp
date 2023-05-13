from django.db import models

# Create your models here.
class Supplier(models.Model):
    rut=models.CharField(max_length=150,blank=False,null=False);
    nombre_proveedor=models.CharField(max_length=150,blank=False,null=False)
    tipo_producto=models.CharField(max_length=150,blank=False,null=False)
    correo_proveedor=models.CharField(max_length=150,blank=False,null=False)
    telefono_proveedor=models.IntegerField(blank=False,null=False)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.nombre_proveedor
