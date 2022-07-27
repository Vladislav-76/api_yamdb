from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from reviews.models import Genre, Category, Titles, Review, Comment
from reviews.serializers import GenreSerializer, CategorySerializer, TitlesSerializer, ReviewSerializer, CommentSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # http_method_names = ['head', 'get']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # http_method_names = ['head', 'get']


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        titles_id = self.kwargs.get("titles_id")
        titles = get_object_or_404(Titles, id=titles_id)
        serializer.save(
            author=self.request.user,
            titles=titles
        )

    def get_queryset(self):
        titles_id = self.kwargs.get("titles_id")
        titles = get_object_or_404(Titles, id=titles_id)
        new_queryset = Review.objects.filter(
            titles=titles
        )
        return new_queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(
            author=self.request.user,
            review=review
        )

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        new_queryset = Comment.objects.filter(
            review=review
        )
        return new_queryset