from rest_framework import viewsets, permissions
from reviews.models import User
from .serializers import AuthSignupSerializer, UserSerializer
from .permissions import AdminOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import filters
from django.core.mail import send_mail
import random
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.tokens import RefreshToken

CODES = {}


def generate_code():
    random.seed()
    return str(random.randint(10000, 99999))


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$username',)
    permission_classes = (AdminOnly,)


class UsernameViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)

    def get_queryset(self):
        username = get_object_or_404(User, pk=self.kwargs.get('username'))
        print(self.kwargs.get('username'))
        return username.users


class MeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def user_create(request):
    if request.method == 'POST':
        serializer = AuthSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_name = request.data['username']
            user_key = generate_code()
            CODES[user_name] = user_key
            user_email = request.data['email']
            send_mail(
                'Код для завершения аутентификации',
                f'{user_name} получили confirmation_code: {user_key} для завершения регистрации',
                'yatube@example.com',  # Это поле "От кого"
                [f'{user_email}'],  # Это поле "Кому"
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def token_create(request):
    if request.data['confirmation_code'] == CODES[request.data['username']]:
        user = User.objects.get(username=request.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)}, status=201)
