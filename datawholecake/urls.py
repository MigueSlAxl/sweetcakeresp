"""datawholecake URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from productos.urls import productos_urlpatterns
from accounts.urls import accounts_urlpatterns
from suppliers.urls import suppliers_urlpatterns
from ordendecompra.urls import ordendc_urlpatterns
from ventas.urls import ventas_urlpatterns
from supplies.urls import supplies_urlpatterns
from ordendetrabajo.urls import ordendetrabajo_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(accounts_urlpatterns)),
    path('productos/',include(productos_urlpatterns)),
    path('suppliers/',include(suppliers_urlpatterns)),
    path('ordendc/',include(ordendc_urlpatterns)),
    path('supplies/',include(supplies_urlpatterns)),
    path('ventas/',include(ventas_urlpatterns)),
    path('ordentrabajo/',include(ordendetrabajo_urlpatterns))
]
admin.site.site_header = 'Wholecake'
admin.site.site_title = 'Wholecake'    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 