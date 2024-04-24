from django.contrib import admin
# from .models import  Carrito, Perfil,Bodega,Boleta,DetalleBoleta
from .models import Servicio,Categoria,Producto,Perfil
# Register your models here.

admin.site.register(Servicio)
admin.site.register(Categoria)
admin.site.register(Producto)
# admin.site.register(Carrito)
admin.site.register(Perfil)
# admin.site.register(Bodega)
# admin.site.register(Boleta)
# admin.site.register(DetalleBoleta)