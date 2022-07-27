from rest_framework import serializers
from django.db.models import Avg
from reviews.models import Genre, Category, Titles, Review, Comment


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
        )
    rates = serializers.SerializerMethodField()

    def get_rates(self, obj):
        reviews = Review.objects.filter(titles=obj.id)
        return reviews.aggregate(Avg('score'))['score__avg']


    class Meta:
        model = Titles
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        exclude = ['titles']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        exclude = ['review']

