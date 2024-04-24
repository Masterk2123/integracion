from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from core.templatetags.custom_filters import formatear_dinero
from django.db import models
from django.db.models import Min
from django.db import connection


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre categoría')
    
    class Meta:
        db_table = 'Categoria'
        verbose_name = "Categoría de producto"
        verbose_name_plural = "Categorías de productos"
        ordering = ['nombre']
    
    def __str__(self):
        return f'{self.nombre}'
    
    def acciones(self):
        return {
            'accion_eliminar': 'eliminar la Categoría',
            'accion_actualizar': 'actualizar la Categoría'
        }

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, verbose_name='Categoría')
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre producto')
    descripcion = models.CharField(max_length=400, blank=False, null=False, verbose_name='Descripción')
    precio = models.IntegerField(blank=False, null=False, verbose_name='Precio')
    descuento_subscriptor = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='% Descuento subscriptor'
    )
    descuento_oferta = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='% Descuento oferta'
    )
    imagen = models.ImageField(upload_to='productos/', blank=False, null=False, verbose_name='Imagen')
    
    class Meta:
        db_table = 'Producto'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['categoria', 'nombre']

    def __str__(self):
        return f'{self.nombre} (ID {self.id})'
    
    def acciones():
        return {
            'accion_eliminar': 'eliminar el Producto',
            'accion_actualizar': 'actualizar el Producto'
        }


class Servicio(models.Model):
    # categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, verbose_name='Categoría')
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre del servicio')
    descripcion = models.CharField(max_length=400, blank=False, null=False, verbose_name='Descripción')
    precio = models.IntegerField(blank=False, null=False, verbose_name='Precio')
    
    imagen = models.ImageField(upload_to='productos/', blank=False, null=False, verbose_name='Imagen')
    
    class Meta:
        db_table = 'Servicio'
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = [ 'nombre'] 

    def __str__(self):
        return f'{self.nombre} '
    
    def acciones():
        return {
            'accion_eliminar': 'eliminar el Servicios',
            'accion_actualizar': 'actualizar el Servicios'
        }
class Perfil(models.Model):
    USUARIO_CHOICES = [
        ('Cliente', 'Cliente'),
        ('Administrador', 'Administrador'),
        ('Superusuario', 'Superusuario'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(
        choices=USUARIO_CHOICES,
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Tipo de usuario'
    )
    rut = models.CharField(max_length=15, blank=False, null=False, verbose_name='RUT')
    # nombre = models.CharField(max_length=40, blank=False, null=False, verbose_name='Nombre')
    # apellido = models.CharField(max_length=40, blank=False, null=False, verbose_name='Apellido')
    # correo = models.CharField(max_length=30, blank=False, null=False, verbose_name='Correo')
    direccion = models.CharField(max_length=400, blank=False, null=False, verbose_name='Dirección')
    subscrito = models.BooleanField(blank=False, null=False, verbose_name='Subscrito')
    imagen = models.ImageField(upload_to='perfiles/', blank=False, null=False, verbose_name='Imagen')
    
    class Meta:
        db_table = 'Perfil'
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"
        ordering = ['tipo_usuario']

    def __str__(self):
        subscrito = ''
        if self.tipo_usuario == 'Cliente':
            subscrito = ' subscrito' if self.subscrito else ' no subscrito'
        return f'{self.usuario.first_name} {self.usuario.last_name} (ID {self.id} - {self.tipo_usuario}{subscrito})'
    
    def acciones():
        return {
            'accion_eliminar': 'eliminar el Perfil',
            'accion_actualizar': 'actualizar el Perfil'
        }

