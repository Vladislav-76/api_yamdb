from rest_framework import viewsets


from reviews.models import Genre, Category, Titles
from reviews.serializers import GenreSerializer, CategorySerializer, TitlesSerializer


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
