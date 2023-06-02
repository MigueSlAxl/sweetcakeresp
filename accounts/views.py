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
from django.views import View
from rest_framework import status
from django.contrib.auth import login
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import re
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        image_data = user.profile.imagen_user.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        return Response({'token': token.key,'username':user.username,'tipo':user.profile.tipo,'email':user.email,'imagen':base64_image})


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
                                'password' : profile.user.password
                                })
        return Response({'List': profile_list})
    else:
        return Response({'Msj': "Error método no soportado"})


#crear usuario como admin
@api_view(['POST'])
def user_user_add_rest(request, format=None):
    if request.method == 'POST':
        first_name = request.data.get('first_name')
        first_name_pass=first_name [0].lower()
        last_name = request.data.get('last_name')
        last_name_pass = last_name[0].lower()
        email = request.data.get('email')
        tipo = request.data.get('tipo')
        rut = request.data.get('rut')
        ntelefono = request.data.get('ntelefono')
        nemergencia = request.data.get('nemergencia')
        local = request.data.get('local')
        direccion = request.data.get('direccion')
        imagen_base64 = request.data.get('imagen_user')
        rut_5= re.search (r'\d{5}' , rut).group()
        username = f'{first_name.capitalize()} {last_name.capitalize()}'
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
        if imagen_base64:
            # Decodificar la imagen base64 y guardarla en el modelo de base de datos
            format, imgstr = imagen_base64.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'{user.id}.{ext}')
            profile.imagen_user.save(f'{user.id}.{ext}', image_data, save=True)
        
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
def user_user_update_rest(request, format=None):
    if request.method == 'POST':
        try:
            id = request.data['id']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            tipo = request.data['tipo']
            rut = request.data['rut']
            ntelefono = request.data['ntelefono']
            nemergencia = request.data['nemergencia']
            local = request.data['local']
            direccion = request.data['direccion']
            email = request.data['email']
            imagen_user = request.data.get('imagen_user')
            username = f'{first_name.capitalize()} {last_name.capitalize()}'
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
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')
        rut = request.data.get('rut')
        ntelefono = request.data.get('ntelefono')
        nemergencia = request.data.get('nemergencia')
        local = request.data.get('local')
        direccion = request.data.get('direccion')
        imagen_base64 = request.data.get('imagen_user')
        username = f'{first_name.capitalize()} {last_name.capitalize()}'
        user = User.objects.create(
            username = username.strip(), 
            first_name = first_name , 
            last_name = last_name ,
            email = email, 
            password = password,
            is_staff = True,
            is_superuser = True,
        )
        user.set_password(password)
        user.save()
        
        profile = Profile.objects.create(
            user=user,
            tipo ="Admin",
            rut = rut,
            ntelefono = ntelefono, 
            nemergencia = nemergencia, 
            local = local, 
            direccion = direccion,

        )
        if imagen_base64:
            # Decodificar la imagen base64 y guardarla en el modelo de base de datos
            format, imgstr = imagen_base64.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'{user.id}.{ext}')
            profile.imagen_user.save(f'{user.id}.{ext}', image_data, save=True)
            token, created = Token.objects.get_or_create(user=user)
            image_data = user.profile.imagen_user.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            return Response({'token': token.key,'username':user.username,'tipo':user.profile.tipo,'correo':user.username,'imagen':base64_image})
        
        return Response({'Usuario creado exitosamente'}, status=status.HTTP_201_CREATED)

    return Response({ 'Error en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def logininfinito_rest(request):
    if request.method == 'POST':
        recuerdame = request.POST.get('recuerdame')
        session_key = request.session.session_key
        if recuerdame == 'true':
            
            request.session.set_expiry(None)

        SessionStore(session_key=session_key).save()

        return JsonResponse({'Msj': 'Recuerda la sesion habilitada'})

    return JsonResponse({'Msj': 'Error en la solicitud'}, status=400)
