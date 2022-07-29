from rest_framework import viewsets, permissions
from reviews.models import User
from .serializers import AuthSignupSerializer, AuthTokenSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import filters
from django.core.mail import send_mail
import random


CODES = {}


def generate_code():
    random.seed()
    return str(random.randint(10000, 99999))


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (permissions.IsAdminUser, )


@api_view(['POST'])
def user_create(request):
    if request.method == 'POST':
        serializer = AuthSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_name = request.data['username']
            user_key = generate_code()
            CODES[user_name] = user_key
            print(CODES)
            user_email = request.data['email']
            send_mail(
                'Код для завершения аутентификации',
                f'Вы получили confirmation_code: {user_key} для завершения регистрации',
                'yatube@example.com',  # Это поле "От кого"
                [f'{user_email}'],  # Это поле "Кому"
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def token_create(request):
    serializer = AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
