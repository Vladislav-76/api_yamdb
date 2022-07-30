import random
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from reviews.models import Title, Review, User, Genre, Category, Title
from api.serializers import (AuthSignupSerializer, ReviewSerializer,
                             CommentSerializer,
                             UserSerializer, GenreSerializer,
                             CategorySerializer, TitlesSerializer)
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from .permissions import AdminOnly, IsAuthorModerAdminOrReadOnly

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
                    f'{user_name} получили confirmation_code:'
                    + f'{user_key} для завершения регистрации',
                    'yatube@example.com',  # Это поле "От кого"
                    [f'{user_email}'],  # Это поле "Кому"
                )
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

    @api_view(['POST'])
    def token_create(request):
        confirmation_code = request.data['confirmation_code']
        username = CODES[request.data['username']]
        if confirmation_code == username:
            user = User.objects.get(username=request.data['username'])
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)}, status=201)


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
