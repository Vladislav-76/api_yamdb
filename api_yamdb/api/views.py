from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import filters
from reviews.models import Title, Review, User, Genre, Category, Title
from api.serializers import (ReviewSerializer, CommentSerializer,
                             UserSerializer, GenreSerializer,
                             CategorySerializer, TitlesSerializer)
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from .permissions import IsAuthorModerAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_fields = ['username']


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
