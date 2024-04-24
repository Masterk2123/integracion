# Create your views here.
from django.shortcuts import  render, redirect
from datetime import date
from django.contrib.auth.models import User
from .poblar import poblar_bd
from .models import Perfil,Servicio
from .forms import RegistroClienteForm, IngresarForm,ServicioForm,UsuarioForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .tools import eliminar_registro #, verificar_eliminar_registro
# from core.templatetags.custom_filters import formatear_dinero, formatear_numero
# from .models import Mascota

# Create your views here.

def inicio(request): 
    if request.method == 'POST':
        buscar = request.POST.get('buscar')
        registros = Servicio.objects.filter(nombre__icontains=buscar).order_by('nombre')
    else:
        registros = Servicio.objects.all().order_by('nombre')

    servicios = []
    for registro in registros:
        servicios.append(obtener_info_producto(registro.id))
    datos = { 'servicios': servicios }
    return render(request, "core/inicio.html",datos)

def ficha(request,servicio_id):
    context = obtener_info_producto(servicio_id)
    return render(request, 'core/Ficha.html', context)

def reserva(request):
    return render(request,'core/Reserva.html')

def salir(request):
    logout(request)
    return redirect(inicio)

def obtener_info_producto(servicio_id):

    servicios = Servicio.objects.get(id=servicio_id)
    
    return {
        'id':servicios.id,
        'nombre': servicios.nombre,
        'descripcion': servicios.descripcion,
        'precio':servicios.precio,
        'imagen': servicios.imagen,
    }


def _servicios(request, accion, id):
    if request.method == 'POST':

        if accion == 'crear':
            form = ServicioForm(request.POST, request.FILES)

        elif accion == 'actualizar':
            form = ServicioForm(request.POST, request.FILES, instance=Servicio.objects.get(id=id))

        if form.is_valid():
            producto = form.save()
            form = ServicioForm(instance=producto)
            messages.success(request, f'El producto "{str(producto)}" se logró {accion} correctamente')
            return redirect(_servicios, 'actualizar', producto.id)
        else:
            messages.error(request, f'No se pudo {accion} el Producto, pues el formulario no pasó las validaciones básicas')
            return redirect(_servicios, 'actualizar', id)

    if request.method == 'GET':

        if accion == 'crear':
            form = ServicioForm()

        elif accion == 'actualizar':
            form = ServicioForm(instance=Servicio.objects.get(id=id))

        elif accion == 'eliminar':
            messages.success(request, eliminar_registro(Servicio, id))
            return redirect(_servicios, 'crear', '0')

    servicio = Servicio.objects.all()

    datos = {
        'form': form,
        'servicios': servicio
    }
    return render(request, 'core/servicios.html', datos)

def poblar(request):
    poblar_bd()
    return redirect(inicio)

def registro(request):
    form = RegistroClienteForm()
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            rut = form.cleaned_data['rut']
            direccion = form.cleaned_data['direccion']
            subscrito = form.cleaned_data['subscrito']
            Perfil.objects.create(
                usuario=user, 
                tipo_usuario='Cliente', 
                rut=rut, 
                direccion=direccion, 
                subscrito=subscrito,
                imagen=request.FILES['imagen'])
            return redirect(ingresar)
            
    return render(request, "core/registro.html", {'form': form})

def misDatos(request):
    form = RegistroClienteForm()
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            rut = form.cleaned_data['rut']
            direccion = form.cleaned_data['direccion']
            subscrito = form.cleaned_data['subscrito']
            Perfil.objects.create(
                usuario=user, 
                tipo_usuario='Cliente', 
                rut=rut, 
                direccion=direccion, 
                subscrito=subscrito,
                imagen=request.FILES['imagen'])
            return redirect(ingresar)
            
    return render(request, "core/misDatos.html", {'form': form})


def salir(request):
    logout(request)
    return redirect(inicio)


def ingresar(request):

    if request.method == "POST":
        form = IngresarForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(inicio)
            messages.error(request, 'La cuenta o la password no son correctos')
    
    return render(request, "core/ingresar.html", {
        'form':  IngresarForm(),
        'perfiles': Perfil.objects.all(),
    })


def miscompras(request):
    return render(request, 'core/miscompras.html')



def nosotros(request):
    return render(request, "core/nosotros.html")

def piePagina(request):
    return render(request, "core/piePagina.html")


def usuarios(request,accion,id):

    if request.method == 'POST':

        if accion == 'crear':
            form = UsuarioForm(request.POST, request.FILES)

        elif accion == 'actualizar':
            form = UsuarioForm(request.POST, request.FILES, instance=Perfil.objects.get(id=id))

        if form.is_valid():
            perfil = form.save()
            form = UsuarioForm(instance=perfil)
            messages.success(request, f'El Perfil "{str(perfil)}" se logró {accion} correctamente')
            return redirect(usuarios, 'actualizar', perfil.id)
        else:
            messages.error(request, f'No se pudo {accion} el Perfil, pues el formulario no pasó las validaciones básicas')
            return redirect(usuarios, 'actualizar', id)

    if request.method == 'GET':

        if accion == 'crear':
            form = UsuarioForm()

        elif accion == 'actualizar':
            form = UsuarioForm(instance=Perfil.objects.get(id=id))

        elif accion == 'eliminar':
            messages.success(request, eliminar_registro(Perfil, id))
            return redirect(usuarios, 'crear', '0')

    perfil = Perfil.objects.all()

    datos = {
        'form': form,
        'perfiles': perfil
    }
    return render(request, "core/usuarios.html",datos)