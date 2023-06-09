import random
import string
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.permissions import IsAuthenticated
from accounts.forms import * 
from django.http import JsonResponse
from django.conf import settings
from PIL import Image
from django.core.files.base import ContentFile
import base64
import os
from accounts.serializers import PasswordResetConfirmSerializer, PasswordResetSerializer
from .models import Profile
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views import View
from rest_framework import status
from django.contrib.auth import login
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import re
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email)
                auth_user = authenticate(username=user.username, password=password , email = user.email)
                if auth_user is not None:
                    token, created = Token.objects.get_or_create(user=user)
                    imagen_user = user.profile.imagen_user.read()
                    base64_image = base64.b64encode(imagen_user).decode('utf-8')
                    return Response({'token': token.key, 'email': user.email,  'username' : user.username ,
                                    'id' : user.id,
                                    'tipo':user.profile.tipo ,
                                    'direccion' : user.profile.direccion ,
                                    'local' : user.profile.local , 'ntelefono' : user.profile.ntelefono,
                                    'imagen_user': base64_image })
                else:
                    return Response({'Msj': 'Contraseña incorrecta'})
            except User.DoesNotExist:
                return Response({'Msj': 'Correo equivocado'})
        else:
            return Response({'Msj': 'Se requiere el email y la contraseña'})

@api_view(['GET'])
def user_user_list_rest(request, format=None):
    if request.method == 'GET':
        profiles = Profile.objects.select_related('user').all()
        profile_list = []
        for profile in profiles:
            image_data = profile.imagen_user.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            profile_list.append({'id': profile.user.id, 'username': profile.user.username ,
                                'first_name' : profile.user.first_name,
                                'last_name' : profile.user.last_name,
                                'email' : profile.user.email ,
                                'tipo':profile.tipo, 
                                'rut' : profile.rut , 
                                'direccion' : profile.direccion , 
                                'ntelefono' : profile.ntelefono,
                                'nemergencia' : profile.nemergencia , 
                                'local' : profile.local,
                                'imagen_user' : base64_image,
                                })
        return Response({'List': profile_list})
    else:
        return Response({'Msj': "Error método no soportado"})


#crear usuario como admin
@api_view(['POST'])
def user_user_add_rest(request, format=None):
    if request.method == 'POST':
        first_name = request.data.get('first_name')
        if re.search(r'\d', first_name):
            return Response({'Msj': 'Error, el nombre debe contener letras, no números'})
        first_name_pass=first_name [0].lower()
        last_name = request.data.get('last_name')
        if re.search(r'\d', last_name):
            return Response({'Msj': 'Error, el apellido debe contener letras, no números'})
        last_name_pass = last_name[0].lower()
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'Msj': 'Error, el Correo ya existe'})
        tipo = request.data.get('tipo')
        rut = request.data.get('rut')
        if len(rut) > 12:
            return Response ({'Msj': 'Error, RUT  no debe superar los 12 caracteres'})
        ntelefono = request.data.get('ntelefono')
        nemergencia = request.data.get('nemergencia')
        local = request.data.get('local')
        direccion = request.data.get('direccion')
        imagen_user = request.data.get('imagen_user')
        if tipo == '' or ntelefono == '' or nemergencia == '' or local == '' or direccion == '' or first_name == '' or last_name == '':
            return Response({'ERROR': 'Cargo , Numero Telefono , Numero emergencia, Dirección, Nombre y Apellido son campos obligatorios, porfavor rellenelos'})
        rut_5= re.search (r'\d{5}' , rut).group()
        username = f'{first_name.capitalize()} {last_name.capitalize()}'
        if User.objects.filter(username=username).exists():
                return Response({'Msj': 'Error, el Nombre ya existe , favor ingrese sus nombres completos'})
        ##### LA CONTRASEÑA SIEMPRE SERA LOS PRIMEROS 5 DIGITOS DEL RUT MAS LA PRIMERA LETRA DEL NOMBRE Y APELLIDO EN MINISCULAS.
        #print(f'{rut_5}{first_name_pass}{last_name_pass}')
        default_password = f'{rut_5}{first_name_pass}{last_name_pass}'
        
        user = User.objects.create(
            username=username.strip(), 
            first_name = first_name , 
            last_name = last_name ,
            email = email, 
            password =make_password(default_password),
        )
        user.save()
        
        profile = Profile.objects.create(
            user=user,
            tipo=tipo,
            rut=rut,
            ntelefono=ntelefono,
            nemergencia=nemergencia,
            local=local,
            direccion=direccion,
        )
        if imagen_user:
                
                image_data = base64.b64decode(imagen_user)
                image = Image.open(ContentFile(image_data))
                profile.imagen_user.save(f'{id}.png', ContentFile(base64.b64decode(imagen_user)), save=True)
                
                image_data = profile.imagen_user.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
        profile.save()
                
        return Response({'message': 'Usuario creado exitosamente'}, status=status.HTTP_201_CREATED)

    return Response({'message': 'Error en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_user_delete_rest(request, format=None):
    if request.method != 'POST':
        return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
        id = int(request.data['id'])
    except (KeyError, ValueError):
        return Response({'error': 'Ingrese un número entero'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        userstandard_array = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response({'error': 'No existe el usuario'}, status=status.HTTP_404_NOT_FOUND)

    userstandard_array.delete()
    return Response({'detail': 'Usuario eliminado con éxito'})


@api_view(['POST'])
def user_user_update_rest(request, format=None , ):
    if request.method == 'POST':
        try:
            id = request.data['id']
            user=get_object_or_404(User,  pk = id)
            first_name = request.data['first_name']
            if re.search(r'\d', first_name):
                return Response({'Msj': 'Error, el nombre debe contener letras, no números'})
            last_name = request.data['last_name']
            if re.search(r'\d', last_name):
                return Response({'Msj': 'Error, el nombre debe contener letras, no números'})
            tipo = request.data['tipo']
            rut = request.data['rut']
            if len(rut) > 12:
                return Response ({'Msj': 'Error, RUT  no debe superar los 12 caracteres'})
            ntelefono = request.data['ntelefono']
            nemergencia = request.data['nemergencia']
            local = request.data['local']
            direccion = request.data['direccion']
            email = request.data['email']
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return Response({'Msj': 'Error, el Correo ya existe'})
            imagen_user = request.data.get('imagen_user')
            if tipo == '' or ntelefono == '' or nemergencia == '' or local == '' or direccion == '' or first_name == '' or last_name == '':
                return Response({'ERROR': 'Cargo , Numero Telefono , Numero emergencia, Dirección, Nombre y Apellido son campos obligatorios, porfavor rellenelos'})
            username = f'{first_name.capitalize()} {last_name.capitalize()}'
            if User.objects.filter(username=username).exclude(id=user.id).exists():
                return Response({'Msj': 'Error, el Nombre ya existe , favor ingrese sus nombres completos'})
            user = User.objects.get(pk=id)
            user.username = username.strip()
            user.email = email
            user.first_name= first_name
            user.last_name = last_name
            user.save()

            profile = user.profile
            profile.tipo = tipo
            profile.rut = rut
            profile.ntelefono = ntelefono
            profile.nemergencia = nemergencia
            profile.local = local
            profile.direccion = direccion

            if imagen_user:
                
                image_data = base64.b64decode(imagen_user)
                image = Image.open(ContentFile(image_data))
                profile.imagen_user.save(f'{id}.png', ContentFile(base64.b64decode(imagen_user)), save=True)
                
            image_data = profile.imagen_user.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            profile.save()

            user_json = {
                'id': user.id,
                'username': user.username,
                'first_name' : user.first_name, 
                'last_name' : user.last_name,
                'email': user.email,
                'tipo': profile.tipo,
                'rut': profile.rut,
                'ntelefono': profile.ntelefono,
                'nemergencia': profile.nemergencia,
                'local': profile.local,
                'direccion': profile.direccion,
                'imagen_user' : base64_image,
            }

            return Response({'Msj': "Datos Actualizados", 'List': user_json})
        except User.DoesNotExist:
            return Response({'Msj': "Error no hay coincidencias"})
        except ValueError:
            return Response({'Msj': "Valor no soportado"})
    else:
        return Response({'Msj': "Método no soportado"})



@api_view(['POST'])
def password_reset_email(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        profile = get_object_or_404(Profile, user__email=email)
        reset_code = ''.join(random.choices(string.digits, k=6))
        profile.reset_code = reset_code
        profile.save()
        send_mail(
            'Codigo para reestablecer contraseña',
            f'Tu codigo es: {reset_code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return Response({'detalle': 'Codigo para reestablecer contraseña enviado! Revisa tu correo.'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def password_reset_confirm(request):
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        reset_code = serializer.validated_data['reset_code']
        new_password = serializer.validated_data['new_password']

        profile = get_object_or_404(Profile, user__email=email)

        if profile.reset_code == reset_code:
            user = profile.user
            user.set_password(new_password)
            user.save()

            profile.reset_code = None
            profile.save()

            return Response({'detalle': 'Contraseña restablecida correctamente.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detalle': 'codigo no valido.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_admin_add_rest(request, format=None):
    if request.method == 'POST':
        if User.objects.filter(is_staff=True, is_superuser=True).count() >= 5:
            return Response({'Se ha alcanzado el número máximo de administradores'}, status=status.HTTP_400_BAD_REQUEST)
        
        first_name = request.data.get('first_name')
        if re.search(r'\d', first_name):
            return Response({'Msj': 'Error, el nombre debe contener letras, no números'})
        
        last_name = request.data.get('last_name')
        if re.search(r'\d', last_name):
            return Response({'Msj': 'Error, el nombre debe contener letras, no números'})
        
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'Msj': 'Error, el Correo ya existe'})
        
        password = request.data.get('password')
        rut = request.data.get('rut')
        if len(rut) > 12:
            return Response({'Msj': 'Error, RUT no debe superar los 12 caracteres'})
        
        ntelefono = request.data.get('ntelefono')
        nemergencia = request.data.get('nemergencia')
        local = request.data.get('local')
        direccion = request.data.get('direccion')
        imagen_user = request.FILES.get('imagen_user')
        
        if (
            ntelefono == '' or
            nemergencia == '' or
            local == '' or
            direccion == '' or
            first_name == '' or
            last_name == ''
        ):
            return Response({'ERROR': 'Cargo, Numero Telefono, Numero emergencia, Dirección, Nombre y Apellido son campos obligatorios, por favor rellénelos'})
        
        username = f'{first_name.capitalize()} {last_name.capitalize()}'
        
        if User.objects.filter(username=username).exists():
            return Response({'Msj': 'Error, el Nombre ya existe, favor ingrese sus nombres completos'})
        
        user = User.objects.create(
            username=username.strip(),
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(
            user=user,
            tipo="Admin",
            rut=rut,
            ntelefono=ntelefono,
            nemergencia=nemergencia,
            local=local,
            direccion=direccion,
        )

        if imagen_user:
                image_data = base64.b64decode(imagen_user)
                image = Image.open(ContentFile(image_data))
                profile.imagen_user.save(f'{id}.png', ContentFile(base64.b64decode(imagen_user)), save=True)
                
                image_data = profile.imagen_user.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
        
        profile.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'tipo': user.profile.tipo,
            'correo': user.username,
            'imagen_user': base64_image, 
        })

    return Response({'Error en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)



