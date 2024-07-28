from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


User = get_user_model()


@api_view(['POST'])
def login(request):
    """ login to created user """
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({'Error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serialize = UserSerializer(user)
    return Response({'user': serialize.data, 'token': token.key})


@api_view(['POST'])
def signup(request):
    """ Create New User account"""
    try:
        serialize = UserSerializer(data=request.data)
    except Exception as e:
        return Response({'error': e})
    if serialize.is_valid():
        serialize.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'Token': token.key, 'user': serialize.data})
    return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)