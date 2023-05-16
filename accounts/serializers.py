from django.contrib.auth.models import User
from .models import User, UserStandard
from drf_extra_fields.fields import Base64ImageField
import base64
from django.http import JsonResponse
from rest_framework import generics, viewsets, serializers,status, validators
from rest_framework.response import Response
import re





def correo_valido(email):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, email) is not None


#####validador de imagen aun no lo uso
def valid_extension(value):
    if (not value.name.endswith('.png') and
        not value.name.endswith('.jpeg') and
        not value.name.endswith('.bmp') and
            not value.name.endswith('.jpg')) and value.name is not None:
            return Response({'Msj': 'Error, formato no permitido'})


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        imagen=Base64ImageField(required=False)
        model = User
        fields = ('username', 'password', 'confirm_password', 'email', 'first_name', 'last_name',
                    'is_client', 'is_admin',  'imagen' )

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True,"validators": [validators.UniqueValidator(
            User.objects.all(), "Ya hay un usuario con el email ingresado"
                    )
                ]
            }
        }
        def validate(self, attrs):
            if attrs.get('password') != attrs.get('confirm_password'):
                raise serializers.ValidationError("Las contraseñas no coinciden")
            return attrs
        

    def create(self, validated_data):
        user = User.objects.first()  # Accediendo al Manager desde una instancia del modelo
        username = validated_data.get('username')    
        password = validated_data.get('password')
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        user = User.objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_client=False,
            is_admin=True
        )
        user.save()
        print('guardaooo')




class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserStandard
        fields = (  'cargo' , 'rut' , 'local' , 'direccion' , 'ntelefono' , 'nemergencia' )
        
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "validators": [
                    validators.UniqueValidator(
                        UserStandard.objects.all(), "Ya hay un usuario con el email ingresado"
                    )
                ]
            }
        }
        def create(self, validated_data):
            
            cargo= validated_data.get('cargo')
            rut= validated_data.get('rut')
            local = validated_data.get('local')
            direccion=validated_data.get('direccion')
            ntelefono=validated_data.get('ntelefono')
            nemergencia=validated_data.get('nemergencia')
                    

            userstandard = UserStandard.objects.create(
                local=local,      
                cargo=cargo,
                rut=rut,
                direccion=direccion,
                ntelefono=ntelefono,
                nemergencia=nemergencia,
            )
            
            print('guardaooo')
            return userstandard

    def get_imagen_base64(self, obj):
        return obj.imagen_base64()










