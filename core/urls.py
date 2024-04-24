from django.urls import path
from .views import inicio,registro,ingresar,miscompras,misDatos,nosotros,_servicios,usuarios,poblar
from .views import salir,ficha, reserva

urlpatterns = [
    path('', inicio, name="inicio"),
    path('registro',registro,name="registro"),
    path('ingresar',ingresar ,name="ingresar"),
    path('miscompras',miscompras ,name="miscompras"),
    path('ficha/<servicio_id>',ficha ,name="ficha"),
    path('misDatos',misDatos ,name="misDatos"),
    path('nosotros',nosotros ,name="nosotros"),
    path('_servicios/<accion>/<id>',_servicios ,name="_servicios"),
    path('reserva',reserva,name="reserva"),
    path('salir', salir, name='salir'),
    path('usuarios/<accion>/<id>', usuarios,name="usuarios"),
    path('poblar',poblar,name="poblar"),
]
