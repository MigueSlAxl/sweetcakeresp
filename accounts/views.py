from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.permissions import IsAuthenticated
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'username':user.username,'tipo':user.profile.tipo,'correo':user.username})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Requiere autenticación mediante token
def user_user_list_rest(request, format=None):
    if request.method == 'GET':
        user_list = User.objects.all()
        user_json = []
        for es in user_list:
            user_json.append({'id': es.id, 'username': es.username})
        return Response({'List': user_json})
    else:
        return Response({'Msj': "Error método no soportado"})