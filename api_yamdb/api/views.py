import random
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, action
from django.core.mail import send_mail
from reviews.models import Title, Review, User, Genre, Category, Title
from api.serializers import (AuthSignupSerializer, ReviewSerializer,
                             CommentSerializer, AuthTokenSerializer,
                             UserSerializer, GenreSerializer,
                             CategorySerializer, TitlesSerializer)
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from .permissions import AdminOnly, IsAuthorModerAdminOrReadOnly
from rest_framework.exceptions import ValidationError

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
    lookup_field = 'username'


@api_view(['GET', 'PATCH'])
def url_me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=200)


"""class MeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    @action(methods=['get'], detail=True)
    def byhello(self, request):
        serializer = UserSerializer(data=request.data)
        self.object = self.get_object()
        return Response(serializer.data, status=200)"""



# class UsernameViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (AdminOnly,)
#     lookup_field = 'username'

#     def get_queryset(self):
#        new_queryset =get_object_or_404(
#            User, username=self.kwargs.get('username'))
#         print(self.kwargs.get('username'))
#         return new_queryset


class AuthViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all()
    # serializer_class = UserSerializer

    @api_view(['POST'])
    def user_create(request):
        serializer = AuthSignupSerializer(data=request.data)
        if serializer.is_valid():
            user_name = request.data['username']
            user_email = request.data['email']
            user_key = generate_code()
            CODES[user_name] = user_key
            if User.objects.filter(
                    username=user_name, email=user_email).exists():
                send_mail(
                    'Код для завершения аутентификации',
                    f'{user_name} получили confirmation_code:'
                    + f'{user_key} для завершения регистрации',
                    'yatube@example.com',  # Это поле "От кого"
                    [f'{user_email}'],  # Это поле "Кому"
                )
                return Response(serializer.data, status=200)
            else:
                if User.objects.filter(email=user_email).exists():
                    return Response(
                        'Пользователь с таким email уже существует!',
                        status=400)
                elif User.objects.filter(username=user_name).exists():
                    return Response(
                        'Пользователь с таким username уже существует!',
                        status=400)
                else:
                    serializer.save()
                    send_mail(
                        'Код для завершения аутентификации',
                        f'{user_name} получили confirmation_code:'
                        + f'{user_key} для завершения регистрации',
                        'yatube@example.com',  # Это поле "От кого"
                        [f'{user_email}'],  # Это поле "Кому"
                    )
                    return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    @api_view(['POST'])
    def token_create(request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(username=request.data['username']).exists():
                confirmation_code = request.data['confirmation_code']
                username = CODES[request.data['username']]
                if confirmation_code == username:
                    user = User.objects.get(username=request.data['username'])
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {'token': str(refresh.access_token)}, status=200)
                else:
                    return Response(
                        'Не верный confirmation_code!',
                        status=400)
            else:
                return Response(
                    'Пользователь не найден!',
                    status=404)
        else:
            return Response(serializer.errors, status=400)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # http_method_names = ['head', 'get']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # http_method_names = ['head', 'get']


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorModerAdminOrReadOnly)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def title_from_url(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        new_queryset = self.title_from_url().reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.title_from_url()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorModerAdminOrReadOnly)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def review_from_url(self):
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        new_queryset = self.review_from_url().comments.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.review_from_url()
        )