from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Correo no registrado en la aplicacion.')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    reset_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        reset_code = attrs.get('reset_code')
        new_password = attrs.get('new_password')

        # Validar el código de restablecimiento de contraseña y obtener el usuario
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Email no valido.')
        if user.profile.reset_code != reset_code:
            raise serializers.ValidationError('Codigo no valido.')

        # Asignar el usuario y la nueva contraseña a los atributos validados
        attrs['user'] = user
        attrs['new_password'] = new_password

        return attrs



