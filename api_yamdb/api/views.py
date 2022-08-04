import random
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import status
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from reviews.models import Title, Review, User, Genre, Category, Title
from api.serializers import (AuthSignupSerializer, ReviewSerializer,
                             CommentSerializer, AuthTokenSerializer,
                             UserSerializer, GenreSerializer,
                             CategorySerializer, TitlesGetSerializer,
                             TitlesSerializer, UserMeSerializer)
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly)
from .permissions import (IsAdminOrReadOnly, AdminOrSUOnly,
                          IsAuthorModerAdminOrReadOnly)
from .filters import TitleFilter

CODES = {}


def generate_code():
    """Генерация числового кода для выдачи токена пользователю."""
    random.seed()
    return str(random.randint(10000, 99999))


class UserViewSet(viewsets.ModelViewSet):
    """Представление для эндпойнта /users/"""
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$username',)
    permission_classes = (AdminOrSUOnly,)
    lookup_field = 'username'


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_me(request):
    """Представление для эндпойнта /users/me/"""
    if request.method == 'PATCH':
        serializer = UserMeSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def user_create(request):
    """Представление для эндпойнта /auth/signup/"""
    serializer = AuthSignupSerializer(data=request.data)
    if serializer.is_valid():
        user_name = request.data['username']
        user_email = request.data['email']
        user_key = generate_code()
        CODES[user_name] = user_key
        mail = ('Код для завершения аутентификации',
                f'{user_name} получил confirmation_code:'
                + f'{user_key} для завершения регистрации',
                'yatube@example.com',
                [f'{user_email}'],)
        if User.objects.filter(
                username=user_name, email=user_email).exists():
            send_mail(*mail)
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
                send_mail(*mail)
                return Response(serializer.data, status=200)
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def token_create(request):
    """Представление для эндпойнта /auth/token/"""
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
                return Response('Не верный confirmation_code!', status=400)
        else:
            return Response('Пользователь не найден!', status=404)
    else:
        return Response(serializer.errors, status=400)


class GenreCategoryPreSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                          mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Общий класс для эндпойнтов жаров и категорий."""
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(GenreCategoryPreSet):
    """Представление для эндпойнта /genres/"""
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryPreSet):
    """Представление для эндпойнта /categories/"""
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """Представление для эндпойнта /titles/"""
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all().order_by('id')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesGetSerializer
        return TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для эндпойнта /reviews/"""
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorModerAdminOrReadOnly)
    http_method_names = ['head', 'get', 'post', 'patch', 'delete']

    def title_from_url(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        new_queryset = self.title_from_url().reviews.all().order_by('id')
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.title_from_url())


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для эндпойнта /comments/"""
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorModerAdminOrReadOnly)
    http_method_names = ['head', 'get', 'post', 'patch', 'delete']

    def review_from_url(self):
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        new_queryset = self.review_from_url().comments.all().order_by('id')
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.review_from_url()
        )
