from rest_framework import viewsets, permissions
from reviews.models import User
from .serializers import AuthSignupSerializer, AuthTokenSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import filters
from django.core.mail import send_mail


confirmation_code = "1234567890"

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
            user_email = request.data['email']
            send_mail(
                'Код для завершения аутентификации',
                f'  вы получили confirmation_code: {confirmation_code}',
                'yatube@example.com',  # Это поле "От кого"
                [f'{user_email}'],  # Это поле "Кому"
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


def token_create(request):
    serializer = AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        print(request.data['confirmation_code'])
