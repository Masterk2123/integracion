import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import  Servicio,Producto,Categoria,Perfil
# Carrito, Perfil, Boleta, DetalleBoleta, Bodega, 

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
            usuario.is_user=False
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')
            usuario.is_user=True

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    # eliminar_tabla('Bodega')
    # eliminar_tabla('DetalleBoleta')
    # eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    # eliminar_tabla('Carrito')
    # eliminar_tabla('Producto')
    eliminar_tabla('Servicio')
    # eliminar_tabla('Categoria')
    # eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd():
    eliminar_tablas()
    print('tablas eliminadas')
    crear_usuario(
        username='cevans',
        tipo='Cliente', 
        nombre='Chris', 
        apellido='Evans', 
        correo='cevans@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='15499707-3', 
        direccion='123 Main Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/cevans.jpg')

    crear_usuario(
        username='eolsen',
        tipo='Cliente', 
        nombre='Elizabeth', 
        apellido='Olsen', 
        correo='eolsen@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='19090011-2', 
        direccion='Albert Street, New York, \nNew York 10001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/eolsen.jpg')

    crear_usuario(
        username='tholland',
        tipo='Cliente', 
        nombre='Tom', 
        apellido='Holland', 
        correo='tholland@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='23548549-0', 
        direccion='105 Apple Park Way, \nCupertino, CA 95014 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/tholland.jpg')

    crear_usuario(
        username='sjohansson',
        tipo='Cliente', 
        nombre='Scarlett', 
        apellido='Johansson', 
        correo='sjohansson@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12788999-4', 
        direccion='350 5th Ave, \nNew York, NY 10118 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/sjohansson.jpg')

    crear_usuario(
        username='admin',
        tipo='Administrador', 
        nombre='admin', 
        apellido='', 
        correo='admin@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='16543210-8', 
        direccion='10 Pine Road, Miami, \nFlorida 33101 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/cpratt.jpg')
    
    crear_usuario(
        username='mruffalo',
        tipo='Administrador', 
        nombre='Mark', 
        apellido='Ruffalo', 
        correo='mruffalo@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21123344-7', 
        direccion='1600 Pennsylvania Avenue NW, \nWashington, D.C. \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/mruffalo.jpg')

    crear_usuario(
        username='super',
        tipo='Superusuario',
        nombre='Robert',
        apellido='Downey Jr.',
        correo='rdowneyjr@marvel.com',
        es_superusuario=True,
        es_staff=True,
        rut='18472636-6',
        direccion='15 Oak Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos',
        subscrito=False,
        imagen='perfiles/rdowneyjr.jpg')
    
    # categorias_data = [
    #     { 'id':1, 'nombre': 'autos'},
    #     { 'id':2, 'nombre': 'motos'},
    #     { 'id':3, 'nombre': 'bicicletas'},
    #     { 'id':4, 'nombre': 'aviones'}
    # ]

    # print('Crear categorías')
    # for categoria in categorias_data:
    #     Categoria.objects.create(**categoria)
    # print('Categorías creadas correctamente')

    servicios = [
        {
            # 'categoria': Categoria.objects.get(id=3),
            'id':1,
            'nombre': 'Cambio de aceite y filtro',
            'descripcion': '''
            Cambia de aceite con nosotros con nuestra actual promocion, 40% de descuento.
            ''',
            'precio': 40000,
            'imagen': 'productos/cambio aceite.jpg'
        },
        {
            # 'categoria': Categoria.objects.get(id=3),
            'id':2,
            'nombre': 'Polarizado',
            'descripcion': '''
            Es 100% material internacional de calidad.
            (Disponibles en todas las tonalidades incluso las permitidas para la revisión técnica)
            ''',
            'precio': 60000,
            'imagen': 'productos/Polar1.jpg'
        },
        {
            # 'categoria': Categoria.objects.get(id=3),
            'id':3,
            'nombre': 'Ajuste de motor',
            'descripcion': '''
            ¿Escuchas sonidos extraños en tu auto y no rinde en las subidas como antes? Realiza un ajuste del motor y sientelo como antes
            (incluye revision, diagnostico y cotizacion)
            ''',
            'precio': 65000,
            'imagen': 'productos/Ajustemotor.jpg'
        },
        {
            # 'categoria': Categoria.objects.get(id=3),
            'id':4,
            'nombre': 'Repintado Mate',
            'descripcion': '''
            ¿Buscas un estilo elegante para tu auto? Prueba lo nuevo y elegante pintandolo Mate.
            (incluye colores rojo, verde oliva, negro, gris, plomo, gris perla, burdeo y amarillo.)
            ''',
            'precio': 120000,
            'imagen': 'productos/CardMate.jpg'
        },
        {
            # 'categoria': Categoria.objects.get(id=3),
            'id':5,
            'nombre': 'Lamina de seguridad.',
            'descripcion': '''
            Material 100% internacional de calidad.
            (Resiste entre 8 y 10 golpes con objetos contundentes como martillo, piedra, bate, etc.)
            ''',
            'precio': 60000,
            'imagen': 'productos/Lamseg.jpg'
        },  
    ]

    print('Crear productos')
    for servicio in servicios:
        Servicio.objects.create(**servicio)
    print('Productos creados correctamente')
