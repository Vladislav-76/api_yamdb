from django.http import Http404
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, action
from django.core.mail import send_mail
from reviews.models import Title, Review, Genre, Category, Title
from api.v1.serializers import (AuthSignupSerializer, ReviewSerializer,
                                CommentSerializer, AuthTokenSerializer,
                                UserSerializer, GenreSerializer,
                                CategorySerializer, TitlesGetSerializer,
                                TitlesSerializer)
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly)
from .permissions import (IsAdminOrReadOnly, AdminOrSUOnly,
                          IsAuthorModerAdminOrReadOnly)
from .filters import TitleFilter

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Представление для эндпойнта /users/"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$username',)
    permission_classes = [AdminOrSUOnly]
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        """Представление для эндпойнта /users/me/"""
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_create(request):
    """Представление для эндпойнта /auth/signup/"""
    serializer = AuthSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user_name = request.data['username']
    user_email = request.data['email']
    user = User.objects.get_or_create(
        username=user_name, email=user_email)[0]
    token = default_token_generator.make_token(user)
    mail = ('Код для завершения аутентификации',
            f'{user_name} получил confirmation_code:'
            + f'{token} для завершения регистрации',
            'yatube@example.com',
            [f'{user_email}'],)
    send_mail(*mail)
    return Response(serializer.data, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_create(request):
    """Представление для эндпойнта /auth/token/"""
    serializer = AuthTokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    user = get_object_or_404(User, username=request.data['username'])
    token = request.data['confirmation_code']
    if default_token_generator.check_token(user, token):
        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)}, status=200)
    else:
        return Response('Неверный confirmation_code!', status=400)


class GenreCategoryPreSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                          mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Общий класс для эндпойнтов жаров и категорий."""
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(GenreCategoryPreSet):
    """Представление для эндпойнта /genres/"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryPreSet):
    """Представление для эндпойнта /categories/"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """Представление для эндпойнта /titles/"""
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
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

    def title_from_url(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        new_queryset = self.title_from_url().reviews.all()
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

    def review_from_url(self):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        if review.title.id == int(title_id):
            return review
        raise Http404("Неверно указано произведение!")

    def get_queryset(self):
        new_queryset = self.review_from_url().comments.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.review_from_url())
