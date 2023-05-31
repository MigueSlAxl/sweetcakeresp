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


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'username':user.username,'tipo':user.profile.tipo,'correo':user.username})
    
# @api_view(['GET'])
# # Requiere autenticación mediante token
# def user_user_list_rest(request, format=None):
#     if request.method == 'GET':
#         user_list = User.objects.all()
#         serializers = UserCreation (user_list, many = True)
#         return JsonResponse({'List' : serializers.data} , safe=False)
#     else:
#         return Response({'Msj':"Error método no soportado"})



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
                                'rut' : profile.rut , 
                                'direccion' : profile.direccion , 
                                'ntelefono' : profile.ntelefono,
                                'nemergencia' : profile.nemergencia , 
                                'local' : profile.local,
                                'imagen_user' : base64_image,
                                'tipo':profile.tipo
                                })
        return Response({'List': profile_list})
    else:
        return Response({'Msj': "Error método no soportado"})


#crear usuario como admin
@api_view(['POST'])
def user_user_add_rest(request, format=None):
    if request.method == 'POST':
        serializer = UserCreation(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create()
            return Response({
                'tipo' :user.tipo , 'rut' :user.rut
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data, status=status.HTTP_201_CREATED )


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
            username = request.data['username']
            tipo = request.data['tipo']
            rut = request.data['rut']
            ntelefono = request.data['ntelefono']
            nemergencia = request.data['nemergencia']
            local = request.data['local']
            direccion = request.data['direccion']
            email = request.data['email']
            imagen_user = request.data.get('imagen_user')

            user = User.objects.get(pk=id)
            user.username = username
            user.email = email
            user.save()
            profile = user.profile
            profile.tipo = tipo
            profile.rut = rut
            profile.ntelefono = ntelefono
            profile.nemergencia = nemergencia
            profile.local = local
            profile.direccion = direccion
            if imagen_user:
                profile.imagen_user.save(f'{id}.png', ContentFile(base64.b64decode(imagen_user)), save=True)
            profile.save()

            user_json = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'tipo': profile.tipo,
                'rut': profile.rut,
                'ntelefono': profile.ntelefono,
                'nemergencia': profile.nemergencia,
                'local': profile.local,
                'direccion': profile.direccion,
                
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