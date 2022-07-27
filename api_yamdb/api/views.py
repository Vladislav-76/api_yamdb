from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from reviews.models import Genre, Category, Titles, Review
from reviews.serializers import GenreSerializer, CategorySerializer, TitlesSerializer, ReviewSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

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
