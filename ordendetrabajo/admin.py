from django.contrib import admin

from ordendetrabajo.models import OrdenTrabajo,InsumoOrden,Trabajador

# Register your models here.
admin.site.register(OrdenTrabajo)
admin.site.register(InsumoOrden)
admin.site.register(Trabajador)